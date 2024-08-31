import json

from app.websockets_ import FLASK_APP, AUTHENTICATED, CONNECTION_LOOKUP, flask_sql


async def authenticate(websocket, handler, token, wsid):
    # authenticate connection with flask
    with FLASK_APP.app_context():
        user = flask_sql.user_sql.confirm_private_key(token)

    if user:
        AUTHENTICATED.add(websocket)

        if wsid:
            CONNECTION_LOOKUP[wsid] = websocket

        await websocket.send(
            json.dumps({"action": "authenticate", "data": f"success: wsid={wsid}"})
        )
        await handler(websocket)

    await websocket.send(json.dumps({"action": "authenticate", "data": "failed"}))
