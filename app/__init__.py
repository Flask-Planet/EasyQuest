from .flask_ import create_app as forward_create_app

__all__ = ["create_app"]


def create_app():
    return forward_create_app()


def flask():
    from app.flask_ import create_app
    create_app().run(debug=True)


def websockets():
    import asyncio
    from app.websockets_.run import run
    asyncio.run(run())
