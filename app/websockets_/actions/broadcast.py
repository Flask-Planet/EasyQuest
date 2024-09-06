import json
from loguru import logger
import websockets

from app.websockets_ import CONNECTION_LOOKUP


async def broadcast_to_quest(quest_code, data, ip_address):
    quest_lookup = CONNECTION_LOOKUP.get(quest_code, {})
    broadcast_group = set()

    if quest_lookup:
        for user_id, connection in quest_lookup.items():
            broadcast_group.add(connection)

    logger.info(f"{ip_address}: Broadcasting to Quest [{quest_code}] ↩︎ \n {data}")
    websockets.broadcast(broadcast_group, json.dumps(data))
