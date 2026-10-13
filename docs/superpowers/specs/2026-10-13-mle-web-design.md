# Diseño — Web Movimiento Liberal Estudiantil (MLE) / Lista Liberal

Fecha: 2026-10-13
Estado: aprobado para implementación

## 1. Objetivo

Sitio de campaña/marca para el **Movimiento Liberal Estudiantil (MLE) / Lista Liberal**,
candidatura a Centro de Estudiantes (Escuela Experimental con Énfasis en TIC, Córdoba
capital). Una sola página pública con secciones ancla, más un panel de administración
privado para gestionar los mensajes recibidos.

- Lema: «Nada de promesas, puros resultados»
- Colores: violeta (principal), blanco, negro
- Valores: liberalismo, mérito, transparencia, libertad individual
- Deploy: Vercel (serverless Python)

Fuente de contenido y estructura: `docs/PLAN_WEB_MLE.md`.

## 2. Stack técnico

| Capa | Tecnología |
|---|---|
| Backend | Flask 3, SQLAlchemy 2 (ORM), Flask-Login, Flask-WTF (CSRF + forms), Flask-Migrate (Alembic) |
| DB dev | SQLite |
| DB prod | Vercel Postgres (Neon) |
| Servidor WSGI prod | Gunicorn (no aplica en Vercel; la función llama al `app`) |
| Frontend | Jinja2 server-rendered + Tailwind CSS v4 (build local, CSS commiteado) |
| JS | Vanilla (`main.js`): menú mobile, smooth scroll, cards expandibles, validación cliente |
| Tests | pytest + Flask test client |
| Deploy | Vercel serverless (`@vercel/python`) + Vercel Postgres |

### 2.1 Tailwind

- Tailwind CSS v4 con `@tailwindcss/cli` (build por Node/npm).
- Tokens de diseño en el bloque `@theme` del CSS fuente.
- El CSS compilado se commitea (`app/static/css/tailwind.css`) para que Vercel solo
  sirva estáticos y no necesite ejecutar el build Python-adyacente.
- `package.json` con scripts `dev` (watch) y `build` (minificado).

## 3. Arquitectura

Aplicación Flask con patrón **application factory**. Jinja renderiza la landing completa
en cada request (contenido estático desde `content/mle.py`). El backend sólo persiste
envíos del formulario y responde al panel admin.

### 3.1 Estructura de carpetas

```
MLE/
  app/
    __init__.py          # create_app(): registra extensiones, blueprints, headers, filtros
    config.py            # Config base + Dev + Prod, lee de entorno
    extensions.py        # db, login_manager, csrf, migrate
    models.py            # Submission, RateLimitHit
    forms.py             # ContactForm, LoginForm
    auth.py              # AdminUser (objeto simple) + user_loader
    routes/
      __init__.py
      main.py            # /, /healthz, /robots.txt, /sitemap.xml
      contact.py         # POST /sumate
      admin.py           # /admin/login, /admin, /admin/submissions/<id>/read
    services/
      mailer.py          # send_submission_notification() best-effort
      ratelimit.py       # check_rate_limit(ip, scope)
    templates/
      base.html
      index.html
      partials/
        _nav.html
        _hero.html
        _nosotros.html
        _propuestas.html
        _equipo.html
        _plan.html
        _transparencia.html
        _sumate.html
        _footer.html
      admin/
        login.html
        submissions.html
    static/
      css/tailwind.src.css   # fuente con @theme + @tailwind directives
      css/tailwind.css       # compilado y commiteado
      js/main.js
      img/logo-mle.svg
      img/favicon.svg
      img/og-image.png
  content/
    mle.py               # datos: propuestas, equipo, plan, indicadores, redes, contacto
  migrations/            # Alembic
  tests/
    conftest.py
    test_public.py
    test_contact.py
    test_admin.py
  api/
    index.py             # entrypoint Vercel: expone `app`
  wsgi.py                # `app = create_app()` para dev/gunicorn
  vercel.json
  requirements.txt
  package.json
  .env.example
  README.md
```

## 4. Modelos de datos

### Submission
| Campo | Tipo | Notas |
|---|---|---|
| id | Integer PK | |
| nombre | String(120) | requerido |
| contacto | String(200) | requerido (email o teléfono) |
| tipo | String(20) | `sugerencia` \| `reclamo` \| `idea` |
| mensaje | Text | requerido, máx 2000 |
| ip | String(45) | IPv4/IPv6, para auditoría/rate limit |
| created_at | DateTime | UTC, default now |
| leido | Boolean | default False |

### RateLimitHit
| Campo | Tipo | Notas |
|---|---|---|
| id | Integer PK | |
| ip | String(45) | |
| scope | String(20) | `contact` \| `login` |
| created_at | DateTime | UTC |

Índice compuesto `(ip, scope, created_at)`.

### Admin
No hay tabla. Un único administrador con credenciales por entorno:
`ADMIN_USER` y `ADMIN_PASSWORD_HASH` (hash `werkzeug.security.generate_password_hash`).
Flask-Login trabaja con un objeto `AdminUser` construido desde config.

## 5. Rutas y contratos

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/` | público | Landing con todas las secciones |
| POST | `/sumate` | público | Procesa el formulario de contacto |
| GET/POST | `/admin/login` | público | Login del admin |
| POST | `/admin/logout` | admin | Cierra sesión |
| GET | `/admin` | admin | Listado de envíos (filtro por tipo/leído) |
| POST | `/admin/submissions/<id>/read` | admin | Marca envío como leído |
| GET | `/healthz` | público | Healthcheck (`{"status":"ok"}`) |
| GET | `/robots.txt` | público | |
| GET | `/sitemap.xml` | público | |

### 5.1 Contrato POST `/sumate`

Request (form-urlencoded, con campo CSRF de Flask-WTF):

```
csrf_token, nombre, contacto, tipo, mensaje, website (honeypot, debe ir vacío)
```

Respuestas:
- `302` redirect a `/#sumate` con flash `success` si se guardó.
- `302` redirect con flash `error` si falla validación, honeypot o rate limit.
- Errores de validación se re-renderizan en la landing con mensajes por campo.

Validaciones servidor (Flask-WTF):
- `nombre`: 2–120 chars, requerido.
- `contacto`: 5–200 chars, requerido.
- `tipo`: uno de `sugerencia`, `reclamo`, `idea`.
- `mensaje`: 10–2000 chars, requerido.
- Los inputs se `strip()`ean. Longitudes capadas.

## 6. Seguridad

- **CSRF:** Flask-WTF en todos los formularios; protegido globalmente.
- **Honeypot:** campo `website` oculto vía CSS; si viene con valor → descartar silenciosamente
  (loguear IP, no guardar).
- **Rate limit DB-backed:** ventana deslizante. `contact`: máx 5 envíos por IP / 15 min.
  `login`: máx 10 intentos por IP / 15 min. Implementado en `services/ratelimit.py`
  consultando `RateLimitHit` (funciona en serverless, sin estado compartido en memoria).
- **Auth:** password hash con `werkzeug`; comparación constante. Sesión Flask-Login con
  cookie firmada.
- **Cookies:** `SESSION_COOKIE_SECURE=True` (prod), `HTTPONLY=True`, `SAMESITE=Lax`,
  `SESSION_COOKIE_NAME` propio.
- **Headers de respuesta** (hook `after_request`): `Content-Security-Policy`
  (`default-src 'self'`; sin fuentes/scripts externos), `X-Content-Type-Options: nosniff`,
  `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`,
  `Permissions-Policy` mínima.
- **Inputs:** cap de longitud, `strip`, autoescape de Jinja. No se renderiza HTML del usuario.
- **Secretos:** sólo por variables de entorno. `.env.example` sin valores reales.
  `SECRET_KEY` requerido en prod (la app falla si falta).
- **Privacidad/PII:** los envíos contienen datos personales; no se loguean en claro.
  El listado admin está detrás de login.
- **Errores:** páginas 400/403/404/500 personalizadas sin trazas en prod.

## 7. Content module (`content/mle.py`)

Estructuras Python editables sin tocar templates:

```python
MLE = {
    "nombre": "Movimiento Liberal Estudiantil",
    "lista": "Lista Liberal",
    "lema": "Nada de promesas, puros resultados",
    "contacto": {"email": "...", "whatsapp": "...", "instagram": "..."},
}
PROPUESTAS = [
    {"id": "centro-digital", "titulo": "...", "icono": "...",
     "objetivo": "...", "pasos": ["..."], "responsable": "...",
     "plazo": "...", "depende_escuela": "..."}, ...  # 10
]
EQUIPO = {"presidente": "...", "vicepresidente": "...",
          "secretarias": [...], "equipos": [...]}
PLAN_90 = [{"periodo": "...", "prioridades": ["..."]}, ...]
INDICADORES = [{"area": "...", "indicador": "..."}, ...]  # 10
REDES = [{"nombre": "...", "url": "..."}]
```

Redes sociales como placeholders `#` hasta que el usuario pase los links reales
(editable en `content/mle.py`).

## 8. Diseño visual (frontend)

- **Tokens (Tailwind `@theme`):**
  - `--color-violeta: #7C3AED`
  - `--color-violeta-oscuro: #5B21B6`
  - `--color-violeta-claro: #A78BFA`
  - `--color-negro: #0B0B0F`
  - `--color-blanco: #FFFFFF`
  - Escala de espaciado, radios y sombras.
- **Tipografía:** sans-serif grande, títulos muy bold (estilo LLA / Que Abuso).
  Stack de sistema o una fuente self-hosted (sin CDN externo, por CSP).
- **Secciones (ids ancla):** `#inicio`, `#nosotros`, `#propuestas`, `#equipo`, `#plan`,
  `#transparencia`, `#sumate`, footer.
- **Componentes:** hero full-height con emblema SVG y 2 CTAs; cards de propuesta
  expandibles (client-side, `<details>` o JS); timeline del plan 90 días; cards de equipo;
  form con estilos de estado; footer con lema + disclaimer + redes.
- **Nav:** sticky, links a anclas, smooth scroll, menú hamburguesa mobile.
- **Emblema:** SVG placeholder propio (isotipo MLE/"L", violeta dominante). Reemplazable.
- **OG:** título, descripción, imagen preview `og-image.png`.
- **A11y AA:** skip link, landmarks semánticos, `aria-*` en nav/hamburguesa, focus visible,
  contraste AA, `alt`, `prefers-reduced-motion`.
- **Performance:** CSS compilado, JS vanilla sin deps, imágenes optimizadas.

## 9. Deploy (Vercel)

- `api/index.py` importa `create_app()` y expone `app` (WSGI).
- `vercel.json`:
  - función Python para `api/index.py`.
  - `app/static/**` servido como estático por el CDN.
  - rewrite del resto de rutas hacia la función.
- Variables de entorno en el dashboard: `SECRET_KEY`, `DATABASE_URL`, `ADMIN_USER`,
  `ADMIN_PASSWORD_HASH`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `MAIL_TO`.
- DB Postgres (Neon) con `poolclass=NullPool` + `pool_pre_ping` para serverless.
- Migraciones Alembic aplicadas contra Postgres (`flask db upgrade`).

## 10. Email

`services/mailer.py` → `send_submission_notification(submission)`:
- Envía por SMTP (config por entorno) un aviso de nuevo mensaje a `MAIL_TO`.
- **Best-effort:** envuelto en `try/except`; si falla no rompe el request
  (el envío ya quedó guardado en DB). Se loguea el error de envío (sin PII).

## 11. Testing

pytest con fixtures (`conftest.py`):
- App con config de test (SQLite temp, `WTF_CSRF_ENABLED` configurable, mailer mockeado).
- Casos:
  - `GET /` responde 200 y contiene lema + las 10 propuestas.
  - `POST /sumate` válido → crea Submission y redirige con success.
  - Validación: campos faltantes/cortos → no crea, errores mostrados.
  - Honeypot con valor → no crea Submission.
  - Rate limit: superar umbral → bloquea.
  - `/admin` sin sesión → redirect a login.
  - Login correcto/incorrecto.
  - Marcar envío como leído cambia `leido`.
  - `mailer` invocado en envío válido (mock).

## 12. Fases de implementación

| Fase | Entregable |
|---|---|
| 0 | Setup proyecto, factory, config, extensiones, tokens Tailwind, `content/mle.py` |
| 1 | Modelos + migraciones + `vercel.json` + entrypoint |
| 2 | Blueprint main + `base.html` + nav + footer + landing (todas las secciones) |
| 3 | Formulario + CSRF + validación + honeypot + rate limit + mailer |
| 4 | Panel admin (login + listado + marcar leído) |
| 5 | Responsive, accesibilidad, OG/SEO, `robots`/`sitemap` |
| 6 | Tests + verificación end-to-end + README |

## 13. Fuera de alcance (YAGNI)

- Tabla de usuarios / multi-admin / roles.
- CRUD de contenido desde la UI (contenido editable en `content/mle.py`).
- i18n.
- Comentarios, blog, analytics de terceros.
- Redis/caché externa.
