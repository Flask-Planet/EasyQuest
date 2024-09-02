import json

from app.websockets_ import FLASK_APP, AUTHENTICATED, CONNECTION_LOOKUP, flask_sql


async def authenticate(websocket, handler, token, user_id):
    # TODO: Add a way to encode the user_id with the quest_id
    # authenticate connection with flask
    with FLASK_APP.app_context():
        user = flask_sql.user_sql.confirm_private_key(token)

    if user:
        AUTHENTICATED.add(websocket)

        if user_id:
            CONNECTION_LOOKUP[user_id] = websocket

        await websocket.send(
            json.dumps({"action": "authenticate", "data": f"success: user_id={user_id}"})
        )
        await handler(websocket)

    await websocket.send(json.dumps({"action": "authenticate", "data": "failed"}))
