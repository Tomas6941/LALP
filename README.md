# Web MLE — Movimiento Liberal Estudiantil

Sitio de campaña de la Lista Liberal (MLE) con formulario de contacto y panel admin.

## Stack

Flask 3 · SQLAlchemy 2 · Flask-Login · Flask-WTF · Jinja2 · CSS nativo (sin framework) · SQLite (dev) / Postgres (prod) · Vercel.

## Desarrollo local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
FLASK_APP=wsgi.py flask db upgrade
FLASK_APP=wsgi.py flask run
```

Los estilos viven en `app/static/css/styles.css` (sin compilación).

## Tests

```bash
python -m pytest -v
```

## Contenido

Editá `content/mle.py` para cambiar propuestas, equipo, cronograma, indicadores y redes.

## Panel admin

- URL: `/admin`
- Credenciales por variables de entorno: `ADMIN_USER` y `ADMIN_PASSWORD_HASH`
  (generá el hash con `werkzeug.security.generate_password_hash`).

## Deploy en Vercel

Guía completa paso a paso: **[DEPLOY_VERCEL.md](DEPLOY_VERCEL.md)**.

Resumen:

1. Provisionar Postgres (Neon/Supabase) → `DATABASE_URL`.
2. Importar el repo en Vercel y cargar las variables de entorno: `SECRET_KEY`,
   `DATABASE_URL`, `ADMIN_USER`, `ADMIN_PASSWORD_HASH`, `SITE_URL`.
3. Aplicar migraciones contra esa base: `python -m flask --app wsgi:app db upgrade`.
4. Deploy.

⚠️ SQLite no funciona en Vercel (filesystem de sólo lectura) y los estáticos deben
vivir en `public/`. Ver el documento para los detalles.

## Seguridad

CSRF global, honeypot, rate limit DB-backed (5/IP/15min contacto, 10/IP/15min login),
headers CSP/X-Frame-Options, cookies Secure/HttpOnly/SameSite, secretos por entorno.