import asyncio

import websockets
from .handler import handler


async def run():
    async with websockets.serve(handler, "127.0.0.1", 5001):
        await asyncio.Future()
