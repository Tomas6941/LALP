from flask import Flask, render_template
from sqlalchemy.pool import StaticPool

from app.config import CONFIG_MAP
from app.extensions import csrf, db, login_manager, migrate


def create_app(config_name: str = "dev") -> Flask:
    app = Flask(__name__)
    app.config.from_object(CONFIG_MAP[config_name])

    if config_name == "prod":
        CONFIG_MAP["prod"]()  # validate env

    # SQLite in-memory needs a single shared connection for tests
    if app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://":
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "poolclass": StaticPool,
            "connect_args": {"check_same_thread": False},
        }
    else:
        # File-based SQLite / other engines use the default pool. Only the
        # in-memory URI above needs StaticPool. For file SQLite keep the
        # default pool but allow cross-thread use (flask run is threaded).
        if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
            app.config.setdefault(
                "SQLALCHEMY_ENGINE_OPTIONS",
                {"pool_pre_ping": True, "connect_args": {"check_same_thread": False}},
            )
        else:
            app.config.setdefault(
                "SQLALCHEMY_ENGINE_OPTIONS",
                {"pool_pre_ping": True},
            )

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    from app import auth  # noqa: F401  registers login_manager.user_loader

    from app.models import Submission, RateLimitHit  # noqa: F401

    from app.routes.admin import admin_bp
    from app.routes.contact import contact_bp
    from app.routes.main import main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)

    from content import mle

    @app.context_processor
    def inject_content():
        return {
            "MLE": mle.MLE,
            "SECCIONES": mle.SECCIONES,
            "NOSOTROS": mle.NOSOTROS,
            "EQUIPO": mle.EQUIPO,
            "PLAN_90": mle.PLAN_90,
            "INDICADORES": mle.INDICADORES,
            "REDES": mle.REDES,
            "FOOTER_DISCLAIMER": mle.FOOTER_DISCLAIMER,
        }

    @app.after_request
    def set_security_headers(response):
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; img-src 'self' data:; "
            "style-src 'self'; script-src 'self'; form-action 'self'; base-uri 'self'"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        return response

    @app.errorhandler(403)
    def forbidden(_e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(_e):
        return render_template("errors/500.html"), 500

    return app
