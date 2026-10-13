import os
from datetime import timedelta
from werkzeug.security import generate_password_hash


def _database_url():
    url = os.environ.get("DATABASE_URL", "sqlite:///mle.db")
    # Vercel/Heroku style postgres:// -> postgresql+psycopg://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-change-me")
    SQLALCHEMY_DATABASE_URI = _database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_NAME = "mle_session"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
    ADMIN_PASSWORD_HASH = os.environ.get(
        "ADMIN_PASSWORD_HASH",
        generate_password_hash("admin"),  # dev default, override in prod
    )

    SMTP_HOST = os.environ.get("SMTP_HOST")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("SMTP_USER")
    SMTP_PASS = os.environ.get("SMTP_PASS")
    MAIL_TO = os.environ.get("MAIL_TO")
    MAIL_SUPPRESS_SEND = False
    SITE_URL = os.environ.get("SITE_URL", "http://localhost:5000")


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

    def __init__(self):
        if not os.environ.get("SECRET_KEY"):
            raise RuntimeError("SECRET_KEY is required in production")


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SECRET_KEY = "test-secret"
    ADMIN_USER = "admin"
    ADMIN_PASSWORD_HASH = generate_password_hash("testpass")
    MAIL_SUPPRESS_SEND = True


CONFIG_MAP = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "testing": TestingConfig,
}
