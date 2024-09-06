import json
import pprint

from loguru import logger

from app.flask_.sql import character_join_request_sql
from app.websockets_ import FLASK_APP


async def get_data(quest_code, user_id, data, ip_address, handler, connection):
    """
    Send a payload to a user by user_id
    """

    quest_id = data.get("quest_id")
    function = data.get("function")

    with FLASK_APP.app_context():

        if function == "getJoinRequests":
            join_requests = character_join_request_sql.get_by_quest_id(quest_id)

            payload = {
                "function": function,
                "set_variables": {
                    "join_requests": [
                        {
                            "character_join_request_id": request.character_join_request_id,
                            "user_id": request.fk_user_id,
                            "character_id": request.fk_character_id,
                            "quest_id": request.fk_quest_id,
                            "__character__": {
                                "character_id": request.rel_character.character_id,
                                "full_name": request.rel_character.full_name,
                                "back_story": request.rel_character.back_story,
                                "display_picture": request.rel_character.display_picture,
                                "arc": request.rel_character.arc,
                            },
                        }
                        for request in join_requests
                    ],
                }
            }

            logger.info(
                f"{ip_address}: Sending to User [{user_id}] in Quest [{quest_code}] ↩︎ \n {pprint.pformat(payload)}"
            )
            await connection.send(json.dumps(payload))

    await handler(connection)
