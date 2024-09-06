from loguru import logger

from app.websockets_ import CONNECTION_LOOKUP


async def disconnect_user(quest_code, data, ip_address):
    """
    Disconnect a websocket by user_id
    """
    to_user_id = data.get("to_user_id")
    if quest_code in CONNECTION_LOOKUP:

        connection = CONNECTION_LOOKUP[quest_code].get(to_user_id)

        if connection:
            logger.info(f"{ip_address}: Disconnecting User [{to_user_id}] in Quest [{quest_code}]")

            await connection.close()
