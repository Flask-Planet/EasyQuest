import json
import pprint

from loguru import logger

from app.websockets_ import CONNECTION_LOOKUP


async def send_to_user_in_quest(quest_code, data, ip_address):
    """
    Send a payload to a user by user_id
    """

    user_id = data.get("user_id")

    if quest_code in CONNECTION_LOOKUP:

        try:
            logger.info(
                f"{ip_address}: Sending to User [{user_id}] in Quest [{quest_code}] ↩︎ \n {pprint.pformat(data)}"
            )

            connection = CONNECTION_LOOKUP[quest_code][str(user_id)]
            if connection:
                await connection.send(
                    json.dumps(data.get("payload", {}))
                )

        except KeyError:
            logger.error(f"{ip_address}: User [{user_id}] not found found in Quest [{user_id}]")
