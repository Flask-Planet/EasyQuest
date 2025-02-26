import os

from dotenv import load_dotenv
from flask_imp.config import FlaskConfig, ImpConfig, SQLiteDatabaseConfig

from app.flask_.services.zepto import ZeptoEmailServiceSettings

load_dotenv()

flask_config = FlaskConfig(
    secret_key=os.getenv("SECRET_KEY", "development"),
    additional={
        "WS": os.getenv("WS_URI", "http://127.0.0.1:5001"),
    }
)

imp_config = ImpConfig(
    init_session={
        "user_id": 0,
        "authenticated": False,
        "permission_level": 0,
        "temp": {}
    },
    database_main=SQLiteDatabaseConfig(
        name=os.getenv("DB_NAME", "database"),
    )
)

zepto_settings = ZeptoEmailServiceSettings(
    False,
    os.getenv("ZEPTO_SENDER"),
    os.getenv("ZEPTO_API_URL"),
    os.getenv("ZEPTO_TOKEN"),
)
