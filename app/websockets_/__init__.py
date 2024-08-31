from app.flask_ import create_app
from app.flask_ import sql as flask_sql

from dotenv import load_dotenv

load_dotenv()

CONNECTIONS = set()
AUTHENTICATED = set()
CONNECTION_LOOKUP = dict()
FLASK_APP = create_app()

__all__ = [
    "CONNECTIONS",
    "AUTHENTICATED",
    "CONNECTION_LOOKUP",
    "FLASK_APP",
    "flask_sql"
]
