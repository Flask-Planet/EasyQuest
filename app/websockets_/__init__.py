from dotenv import load_dotenv
from loguru import logger

from app.flask_ import create_app
from app.flask_ import sql as flask_sql


logger.info("Starting websockets...")

load_dotenv()

# (connection, ...)
CONNECTIONS = set()

# (connection, ...)
AUTHENTICATED = set()

# {quest_code: {user_id: connection}, ...}
CONNECTION_LOOKUP = dict()

FLASK_APP = create_app()

__all__ = [
    "CONNECTIONS",
    "AUTHENTICATED",
    "CONNECTION_LOOKUP",
    "FLASK_APP",
    "flask_sql",
]
