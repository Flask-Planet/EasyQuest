import json

from app.websockets_ import CONNECTION_LOOKUP


async def disconnect_user_id(data):
    """
    Disconnect a websocket by user_id
    """
    to_user_id = data.get("to_user_id")
    if to_user_id in CONNECTION_LOOKUP:
        await CONNECTION_LOOKUP[to_user_id].send(
            json.dumps({
                "action": "disconnect",
                "data": None,
            }))
        await CONNECTION_LOOKUP[to_user_id].close()
