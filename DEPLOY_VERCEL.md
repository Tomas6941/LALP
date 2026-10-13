# Migración a Vercel — LALP / MLE

Guía paso a paso para desplegar este proyecto (Flask + Jinja2 + SQLAlchemy) en Vercel.

> **Contexto:** el repo venía preparado para el **modelo viejo** de Vercel (`builds` + `@vercel/python` + carpeta `/api`). Desde octubre de 2025 Vercel detecta Flask de forma automática (*zero-config*), así que esa configuración se reemplaza. Además hay **3 cosas que hoy rompen** en producción: SQLite, los estáticos en `app/static/` y la config de desarrollo en `wsgi.py`.

---

## Índice

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Lo que ya está listo](#2-lo-que-ya-está-listo)
3. [Paso 1 — Corregir la config de producción (`wsgi.py`)](#paso-1--corregir-la-config-de-producción-wsgipy)
4. [Paso 2 — Mover los estáticos a `public/`](#paso-2--mover-los-estáticos-a-public)
5. [Paso 3 — Reemplazar `vercel.json` y borrar `api/`](#paso-3--reemplazar-verceljson-y-borrar-api)
6. [Paso 4 — Fijar la versión de Python y limpiar dependencias](#paso-4--fijar-la-versión-de-python-y-limpiar-dependencias)
7. [Paso 5 — Provisionar Postgres](#paso-5--provisionar-postgres)
8. [Paso 6 — Correr las migraciones](#paso-6--correr-las-migraciones)
9. [Paso 7 — Variables de entorno en Vercel](#paso-7--variables-de-entorno-en-vercel)
10. [Paso 8 — Deploy](#paso-8--deploy)
11. [Paso 9 — Verificación post-deploy](#paso-9--verificación-post-deploy)
12. [Emails: SMTP vs API HTTP](#emails-smtp-vs-api-http)
13. [Solución de problemas](#solución-de-problemas)
14. [Checklist final](#checklist-final)

---

## 1. Resumen ejecutivo

| # | Problema | Impacto | Solución |
|---|---|---|---|
| 🔴 1 | `DATABASE_URL` por defecto es SQLite | El formulario y el login devuelven **500** (FS de sólo lectura) | Usar Postgres |
| 🔴 2 | Assets en `app/static/` | **404** en CSS/JS/imágenes (Vercel ignora `app.static_folder`) | Mover a `public/static/` |
| 🔴 3 | `wsgi.py` usa `create_app("dev")` | Deploy con **`DEBUG=True`** y SQLite | Selección de config por entorno |
| 🟡 4 | `vercel.json` legacy + `api/index.py` | Config obsoleta, entrypoint ambiguo | Reemplazar / borrar |
| 🟡 5 | Falta `SECRET_KEY` | `ProdConfig` **aborta** el arranque (correcto) | Setear la env var |
| 🟡 6 | SMTP síncrono con errores silenciados | Podés no recibir avisos de nuevos mensajes | API HTTP de email |

**Resultado:** los mensajes del formulario se guardan igual en Postgres y se ven en `/admin`. Si el email falla, sólo se pierde la *notificación*, no el mensaje.

---

## 2. Lo que ya está listo

No hay que tocar nada de esto:

- ✅ `_database_url()` en `app/config.py` ya normaliza `postgres://` → `postgresql+psycopg://`.
- ✅ `psycopg[binary]` ya está en `requirements.txt`.
- ✅ `_client_ip()` ya lee `X-Forwarded-For` → el rate limit funciona detrás del proxy de Vercel.
- ✅ La sesión es una cookie firmada y **sin estado** → escala sin cambios.
- ✅ Existen las migraciones Alembic (`submission` + `rate_limit_hit`).
- ✅ `ProdConfig` falla fuerte si falta `SECRET_KEY` (mejor fallar el build que arrancar inseguro).
- ✅ Ninguna plantilla necesita cambios: todas usan `url_for('static', ...)`, que sigue resolviendo a `/static/...`.

---

## Paso 1 — Corregir la config de producción (`wsgi.py`)

**El problema:** Vercel busca tu app de Flask en `app.py`, `index.py`, `server.py`, `main.py`, **`wsgi.py`**, `asgi.py` (en la raíz o dentro de `src/`, `app/` o `api/`). Tu `wsgi.py` de la raíz hace `create_app("dev")` → si Vercel lo elige, el sitio sale con `DEBUG=True` y SQLite.

### 1.1 Agregar el helper en `app/config.py`

Al final del archivo, después de las clases de config:

```python
def default_config_name() -> str:
    """'dev' en local, 'prod' cuando corre en Vercel (VERCEL=1)."""
    return os.environ.get("APP_CONFIG") or ("prod" if os.environ.get("VERCEL") else "dev")
```

### 1.2 Usarlo en `wsgi.py`

```python
from dotenv import load_dotenv

load_dotenv()

from app import create_app  # noqa: E402
from app.config import default_config_name  # noqa: E402

app = create_app(default_config_name())
```

> **Por qué así:** usa la variable `VERCEL` que la plataforma setea sola, en vez de depender de una env var que alguien puede olvidar. Si falta `SECRET_KEY` en prod, `ProdConfig` revienta en el build — **falla ruidoso, no inseguro**.

---

## Paso 2 — Mover los estáticos a `public/`

**El problema:** la doc de Vercel es explícita:

> *"Flask's `app.static_folder` should not be used for static files on Vercel. Use the `public/**` directory instead."*

Todo lo que esté en `public/**` se sirve desde el CDN en la **raíz del dominio**: `public/static/css/styles.css` → `https://tu-sitio/static/css/styles.css`. Es exactamente la URL que ya genera `url_for('static', ...)`, así que **las plantillas no cambian**.

### 2.1 Mover los archivos

```powershell
git mv app/static public/static
```

> El CSS referencia `../img/bandera4-cropped.jpg`: al mover la carpeta completa, la ruta relativa sigue resolviendo igual.

### 2.2 Apuntar Flask a la carpeta nueva (para desarrollo local)

En `app/__init__.py`:

```python
from pathlib import Path

from flask import Flask, render_template
...

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app(config_name: str = "dev") -> Flask:
    app = Flask(
        __name__,
        static_folder=str(BASE_DIR / "public" / "static"),
        static_url_path="/static",
    )
    ...
```

Con esto:
- **Local:** Flask sirve `/static/...` desde `public/static/` (mismo comportamiento que antes).
- **Vercel:** el CDN intercepta `/static/...` y sirve los archivos sin tocar la función.

**Resultado:** una sola copia de los assets, sin duplicar nada.

---

## Paso 3 — Reemplazar `vercel.json` y borrar `api/`

### 3.1 Borrar el entrypoint viejo

```powershell
git rm api/index.py
Remove-Item api -Recurse -Force -ErrorAction SilentlyContinue
```

Así `wsgi.py` queda como **único** entrypoint posible y no hay ambigüedad.

### 3.2 Reemplazar `vercel.json`

El actual usa `builds` + `@vercel/python` + `@vercel/static` + `routes`: es el formato legacy. El changelog de Vercel dice que la detección automática *"removes the need for redirects in `vercel.json` or using the `/api` folder"*.

```json
{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "functions": {
    "wsgi.py": {
      "maxDuration": 30,
      "excludeFiles": "{tests/**,docs/**,**/test_*.py,**/__pycache__/**,.pytest_cache/**,*.db,instance/**}"
    }
  }
}
```

- `maxDuration: 30` — el envío de email es **sincrónico** con timeout de 10 s; el default en Hobby es corto. Verificá el tope de tu plan.
- `excludeFiles` — Python **no hace tree-shaking**: sin esto, `tests/` y `docs/` viajan dentro del bundle del function.

---

## Paso 4 — Fijar la versión de Python y limpiar dependencias

### 4.1 Crear `.python-version` (raíz)

```text
3.12
```

Vercel usa 3.12 por defecto y soporta 3.12 / 3.13 / 3.14. Tu entorno local es 3.12.x: fijarlo evita sorpresas.

### 4.2 Separar dependencias de desarrollo

Todo lo listado en `requirements.txt` se **instala dentro del bundle** del function. `pytest` no tiene nada que hacer ahí.

**`requirements.txt`** (runtime):

```
Flask>=3.0
Flask-SQLAlchemy>=3.1
Flask-Login>=0.6
Flask-WTF>=1.2
Flask-Migrate>=4.0
SQLAlchemy>=2.0
python-dotenv>=1.0
psycopg[binary]>=3.1
```

**`requirements-dev.txt`** (nuevo):

```
-r requirements.txt
pytest>=8
gunicorn>=21
```

> `gunicorn` no se usa en Vercel (la plataforma envuelve tu WSGI app sola) ni en local (`flask run`). Se saca del runtime.

### 4.3 Crear `.vercelignore`

Sólo importa para deploys por CLI (en deploys por Git únicamente se suben los archivos commiteados):

```
.venv/
venv/
node_modules/
.pytest_cache/
__pycache__/
*.py[cod]
*.db
instance/
tests/
.env
```

---

## Paso 5 — Provisionar Postgres

El filesystem de las Functions es **de sólo lectura** (sólo `/tmp` es escribible, y es efímero). SQLite no es una opción: el guardado del formulario fallaría con 500.

**Opciones** (todas tienen free tier suficiente):

| Proveedor | Nota |
|---|---|
| **Neon** (recomendado) | Integración nativa en el Marketplace de Vercel, serverless-friendly |
| Supabase | Más features, un poco más de setup |
| Railway / Render | Cualquier Postgres sirve |

1. Creá el proyecto y copiá el **connection string**. Suele venir como `postgresql://usuario:pass@host/db?sslmode=require`.
2. Vas a usarlo como `DATABASE_URL`. **No hace falta transformarlo**: `_database_url()` se encarga de convertir `postgresql://` → `postgresql+psycopg://`.

> Si el proveedor exige SSL (Neon/Supabase sí), conservá `?sslmode=require` en la URL.

---

## Paso 6 — Correr las migraciones

Vercel **no tiene shell**, así que las migraciones se corren **una vez desde tu máquina** contra la base remota:

```powershell
# 1. Instalar el driver de Postgres (hoy no está en tu entorno local)
pip install "psycopg[binary]"

# 2. Apuntar a la base remota y migrar
$env:DATABASE_URL = "postgresql://usuario:pass@host/db?sslmode=require"
python -m flask --app wsgi:app db upgrade
```

Verificá que las 2 migraciones se aplicaron:

```powershell
python -m flask --app wsgi:app db current
# Debería mostrar: e22eb18fb84b (head)
```

> ⚠️ Si tenés un `.env` local, `load_dotenv()` **no pisa** variables ya definidas en el shell (`override=False`), así que el `$env:DATABASE_URL` de arriba gana. Aun así, podés comentar la línea del `.env` para estar seguro.
>
> ⚠️ Sin este paso, el primer request que toque la base explota con `relation "submission" does not exist`.

---

## Paso 7 — Variables de entorno en Vercel

En **Project → Settings → Environment Variables** (marcá Production **y** Preview):

| Variable | Obligatoria | Cómo generarla |
|---|---|---|
| `SECRET_KEY` | ✅ | `python -c "import secrets;print(secrets.token_hex(32))"` |
| `DATABASE_URL` | ✅ | Connection string de Neon/Supabase |
| `ADMIN_USER` | ✅ | Tu nombre de usuario, ej. `tomas` |
| `ADMIN_PASSWORD_HASH` | ✅ | `python -c "from werkzeug.security import generate_password_hash as g;print(g('TU_CLAVE'))"` |
| `SITE_URL` | ✅ | `https://tu-proyecto.vercel.app` (lo usa `/sitemap.xml`) |
| `MAIL_TO` | opcional | Casilla que recibe los avisos |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASS` | opcional | Ver sección de emails |

> ⚠️ **El hash lleva `$`** (`pbkdf2:sha256:600000$salt$hash`). En el dashboard se pega literal y no hay problema. Si lo cargás por CLI, **entrecomillalo** o el shell lo va a interpolar.
>
> ⚠️ **Previews comparten `DATABASE_URL`** con producción salvo que definas variables distintas por entorno. Si no querés que un preview escriba en la base real, creá una base aparte para Preview.

---

## Paso 8 — Deploy

### Opción A — Por Git (recomendado)

```powershell
git add -A
git commit -m "chore: preparar deploy en Vercel (Postgres, estáticos en public/, config por entorno)"
git push
```

Luego importá el repo en [vercel.com/new](https://vercel.com/new). Vercel detecta Flask solo (leyendo `requirements.txt`); **no hay que configurar build command ni output directory**.

### Opción B — Por CLI

```powershell
npm i -g vercel
vercel link
vercel env pull          # trae las env vars para desarrollo local
vercel                   # crea un Preview
vercel --prod            # a producción
```

> Para desarrollar local con el mismo entrypoint que producción: `vercel dev`.

---

## Paso 9 — Verificación post-deploy

Con el dominio de producción:

```powershell
# 1. Health check
curl https://tu-proyecto.vercel.app/healthz
# → {"status":"ok"}

# 2. Los estáticos se sirven desde el CDN
curl -I https://tu-proyecto.vercel.app/static/css/styles.css
# → 200 OK

# 3. La home carga
curl -I https://tu-proyecto.vercel.app/
# → 200 OK
```

Checklist manual:

- [ ] La home se ve **idéntica** a local (fuentes, hero, imágenes).
- [ ] `/static/css/styles.css` y `/static/js/main.js` → **200**, no 404.
- [ ] `/admin` redirige a `/admin/login`; podés entrar con `ADMIN_USER` + tu clave.
- [ ] Enviás el formulario de `#sumate` y el mensaje **aparece en `/admin`** (esto prueba que Postgres está escribiendo).
- [ ] `/robots.txt` y `/sitemap.xml` responden y el sitemap muestra tu dominio real (no `localhost`).
- [ ] En Vercel → **Deployments → Functions**, el bundle pesa poco (no debería rondar los cientos de MB).
- [ ] **No** aparece `DEBUG` activo en ninguna respuesta de error.

---

## Emails: SMTP vs API HTTP

Funciona **parcialmente**, y conviene saber por qué.

**Lo que pasa hoy:** `app/services/mailer.py` usa `smtplib` de forma **sincrónica** dentro del request, y atrapa todo con `except Exception: return False`.

Consecuencias en Vercel:
- Las Functions corren sobre AWS Lambda, que **bloquea el puerto 25** de salida. Los puertos **587/465 normalmente sí funcionan**, pero el envío puede ser lento o fallar de forma intermitente.
- Si falla, **no te enterás nunca**: el error se descarta silenciosamente y el usuario ve "Mensaje recibido" igual.
- Suma hasta 10 s (el timeout del `smtplib`) a la request del usuario.

**Lo tranquilizador:** el mensaje se guarda en Postgres **antes** de intentar el email, así que siempre lo vas a ver en `/admin`. Se pierde la notificación, no el mensaje.

**Recomendación:** migrar a una API HTTP (Resend, Brevo, SendGrid). Son ~15 líneas en un solo archivo, porque la interfaz ya está aislada en `send_submission_notification(submission)`:

```python
# app/services/mailer.py — reemplazo del cuerpo de la función
import requests

def send_submission_notification(submission) -> bool:
    app = current_app
    if app.config.get("MAIL_SUPPRESS_SEND"):
        return True
    api_key = app.config.get("RESEND_API_KEY")
    mail_to = app.config.get("MAIL_TO")
    if not api_key or not mail_to:
        return False

    try:
        resp = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "from": app.config.get("MAIL_FROM", "onboarding@resend.dev"),
                "to": [mail_to],
                "subject": f"Nuevo mensaje LALP — {submission.puesto}",
                "text": (
                    f"Nombre: {submission.nombre}\n"
                    f"Contacto: {submission.contacto}\n"
                    f"Puesto: {submission.puesto}\n\n"
                    f"Mensaje:\n{submission.mensaje}\n"
                ),
            },
            timeout=10,
        )
        resp.raise_for_status()
        return True
    except Exception:
        app.logger.exception("Fallo al enviar notificación")
        return False
```

Agregar `requests` a `requirements.txt` y `RESEND_API_KEY` a las env vars.

> Como mínimo, si se mantiene SMTP: cambiá el `except Exception` para que **loguee el error** (así aparece en Vercel → Logs) en vez de tragárselo.

---

## Solución de problemas

| Síntoma | Causa probable | Fix |
|---|---|---|
| `500` en `/` al arrancar | Falta `SECRET_KEY` | Setearla en Vercel (el build debería haber fallado antes) |
| `500` al enviar el formulario | `DATABASE_URL` sigue siendo SQLite | Setear Postgres y **redeployar** |
| `relation "submission" does not exist` | Migraciones no corridas | Paso 6 |
| CSS/JS/imágenes en 404 | Assets todavía en `app/static/` | Paso 2 |
| La app se ve sin estilos pero responde 200 | `static_url_path` mal configurado | Debe ser `/static` |
| Errores muestran trazas / `DEBUG` | Vercel tomó `wsgi.py` con config dev | Paso 1 |
| Vercel no detecta la app | Quedó `api/index.py` o falta `requirements.txt` | Paso 3.1 |
| `sitemap.xml` con `localhost` | Falta `SITE_URL` | Paso 7 |
| No llegan los emails | SMTP bloqueado/lento | Sección de emails |
| `ModuleNotFoundError: psycopg` | No instalaste el driver para migrar | `pip install "psycopg[binary]"` |

---

## Checklist final

- [ ] `app/config.py`: agregado `default_config_name()`
- [ ] `wsgi.py`: usa `default_config_name()`
- [ ] `app/__init__.py`: `static_folder` apunta a `public/static`
- [ ] `git mv app/static public/static`
- [ ] `api/index.py` **borrado**
- [ ] `vercel.json` reemplazado por el formato moderno
- [ ] `.python-version` = `3.12`
- [ ] `.vercelignore` creado
- [ ] `requirements.txt` sin `pytest`/`gunicorn` (movidos a `requirements-dev.txt`)
- [ ] Base Postgres creada
- [ ] `python -m flask --app wsgi:app db upgrade` ejecutado contra la base remota
- [ ] `SECRET_KEY`, `DATABASE_URL`, `ADMIN_USER`, `ADMIN_PASSWORD_HASH`, `SITE_URL` cargadas
- [ ] Deploy hecho y verificado con el checklist del Paso 9
- [ ] (Opcional) Mailer migrado a API HTTP

---

## Notas

- **Plan de Vercel:** Hobby es sólo para uso **no comercial**. Si esto se considera parte de una organización, corresponde Pro.
- **`/tmp`:** existe y es escribible, pero es **efímero y por instancia** — nunca sirve como almacenamiento persistente.
- **`migrations/`** se versiona igual (la necesitás para correr `db upgrade` desde tu máquina).
- **Cold starts:** con Fluid compute, varias requests comparten instancia. La primera invocación tras un rato de inactividad puede tardar un poco más.
- **Rollback:** `vercel rollback` (CLI) o *Promote to Production* sobre un deployment anterior desde el dashboard. Las migraciones **no** se revierten solas.
