from loguru import logger
import sys
from .web_ import create_app as forward_create_app

logger.remove()

# logger.add(
#     "logs/app.log",
#     rotation="1 day",
#     retention="7 days",
#     level="DEBUG",
#     backtrace=True,
#     diagnose=True,
# )
logger.add(
    sys.stderr,
    colorize=True,
    format=("<green>{time:YYYY-MM-DD HH:mm:ss}</green> |"
            " <level>{level: <8}</level> |"
            " <cyan>{name}</cyan>:"
            " - <level>{message}</level>"),
)

__all__ = ["create_app"]


def create_app():
    return forward_create_app()


def flask():
    from app.web_ import create_app
    create_app().run(debug=True)


def websockets():
    import asyncio
    from app.websockets_.run import run
    asyncio.run(run())
