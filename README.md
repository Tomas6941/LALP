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

1. Importá el repo en Vercel.
2. Configurá las variables de entorno: `SECRET_KEY`, `DATABASE_URL` (Vercel Postgres /
   Neon), `SITE_URL`, `ADMIN_USER`, `ADMIN_PASSWORD_HASH`, `SMTP_*`, `MAIL_TO`.
3. Deploy. La función está en `api/index.py`; los estáticos se sirven desde `app/static`.
4. Aplicá migraciones contra Postgres: `FLASK_APP=api/index.py flask db upgrade`
   (o desde un job con `DATABASE_URL` de prod).

## Seguridad

CSRF global, honeypot, rate limit DB-backed (5/IP/15min contacto, 10/IP/15min login),
headers CSP/X-Frame-Options, cookies Secure/HttpOnly/SameSite, secretos por entorno.