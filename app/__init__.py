from flask import Flask
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

    # Flask-Login injects `current_user` into every template context and
    # raises when no loader is configured. The admin auth module registers the
    # real loader in a later task; until then provide a no-op loader so public
    # pages render. Registering the real loader later overrides this one.
    if login_manager.user_callback is None:
        login_manager.user_loader(lambda user_id: None)

    from app.models import Submission, RateLimitHit  # noqa: F401

    from app.routes.main import main_bp

    app.register_blueprint(main_bp)

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

    return app
