import json

from loguru import logger

from app.websockets_ import FLASK_APP, AUTHENTICATED, CONNECTION_LOOKUP, flask_sql


async def authenticate(connection, private_key, quest_code, user_id, ip_address):
    logger.info(f"{ip_address}: User [{user_id}] Authenticating...")

    # authenticate connection with flask
    with FLASK_APP.app_context():
        user = flask_sql.user_sql.confirm_private_key(private_key)

    if user:
        logger.info(f"{ip_address}: User [{user_id}] Authenticated")

        AUTHENTICATED.add(connection)

        if quest_code not in CONNECTION_LOOKUP:
            CONNECTION_LOOKUP[quest_code] = {}

        CONNECTION_LOOKUP[quest_code][user_id] = connection

        await connection.send(
            json.dumps({"action": "authenticate", "data": "success"})
        )
    else:
        logger.error(f"{ip_address}: User [{user_id}] Failed to authenticate")

        await connection.send(json.dumps({"action": "authenticate", "data": "failed"}))
        await connection.close()
