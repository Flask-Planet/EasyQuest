import json

import websockets
from app.websockets_ import CONNECTIONS


async def broadcast(websocket, handler_, data):
    websockets.broadcast(CONNECTIONS, json.dumps(data))
    await handler_(websocket)
