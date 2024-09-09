import json

import websockets
from loguru import logger

from app.websockets_ import CONNECTION_LOOKUP


async def broadcast_to_quest(user_id, quest_code, data, ip_address):
    quest_lookup = CONNECTION_LOOKUP.get(quest_code, {})
    print(quest_lookup)
    broadcast_group = set()

    if quest_lookup:
        for lookup_user_id, connection in quest_lookup.items():
            if lookup_user_id == user_id:
                continue

            broadcast_group.add(connection)

    logger.info(f"{ip_address}: Broadcasting to Quest [{quest_code}] ↩︎ \n {data}")
    websockets.broadcast(broadcast_group, json.dumps(data))
