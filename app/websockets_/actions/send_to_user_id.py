import json

from app.websockets_ import CONNECTION_LOOKUP


async def send_to_user_id(data):
    """
    Send a payload to a user by user_id
    """
    to_user_id = data.get("to_user_id")
    if to_user_id in CONNECTION_LOOKUP:
        await CONNECTION_LOOKUP[to_user_id].send(
            json.dumps(data.get("payload", {}))
        )
