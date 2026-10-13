from dotenv import load_dotenv

load_dotenv()

from app import create_app  # noqa: E402
from app.config import default_config_name  # noqa: E402

# Vercel loads this module as the WSGI entrypoint; the config then resolves to
# "prod", while local runs stay on "dev".
app = create_app(default_config_name())
