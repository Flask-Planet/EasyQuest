import asyncio
import pathlib
import sys

import click

CWD = pathlib.Path(__file__).parent.parent

sys.path.append(str(CWD))


@click.group()
def cli():
    pass


@cli.command("flask")
def cli_flask():
    from app.flask_ import create_app
    create_app().run(debug=True)


@cli.command("websockets")
def cli_websockets():
    from app.websockets_.run import run
    asyncio.run(run())


if __name__ == "__main__":
    cli()
