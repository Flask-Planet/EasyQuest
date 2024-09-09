import json

import websockets
from loguru import logger

from app.websockets_ import CONNECTIONS, AUTHENTICATED, CONNECTION_LOOKUP
from .actions import disconnect_user, send_to_user_in_quest, broadcast_to_quest, authenticate, get_data
from .utilities import get_quest_code_from_path

"""
Inbound message format:

{
    'user_id': int, <- inbound user_id
    'token': str, <- inbound token (skipped if system)
    'action': str, <- action to take
    'data': {} <- data to process
}

An example of the system sending a message to a user:

{
    'user_id': 1,
    'token': None,
    'action': 'send_to_user_id',
    'data': {
        'user_id': 2,
        'payload': {
            'from_user_id': 1,
            'action': 'run_function',
            'function': 'refreshInventory',
        }
    }
}

"""


async def handler(connection):
    if connection not in CONNECTIONS:
        CONNECTIONS.add(connection)

        if "system" in connection.path:
            if connection.remote_address[0] in ["127.0.0.1", "::1"]:
                logger.opt(colors=True).info("<green>System Connection >>> Auto Authenticate</green>")
                AUTHENTICATED.add(connection)
        else:
            logger.info(f"{connection.remote_address[0]}: Connection established - [{connection.path}]")

    try:

        ip_address = connection.remote_address[0]
        path = connection.path

        inbound = await connection.recv()
        quest_code = get_quest_code_from_path(path)

        # parse inbound message
        payload = json.loads(inbound)

        # split payload
        user_id = payload.get("user_id", 0)
        private_key = payload.get("private_key")
        action = payload.get("action", "disconnect")
        data = payload.get("data")

        # disconnect
        if action == "disconnect":
            logger.info(f"Disconnecting: {connection}")
            await connection.close()

        # authenticate connection
        if action == "authenticate":
            await authenticate(connection, private_key, quest_code, user_id, ip_address)

        # Connection is already authenticated
        if connection in AUTHENTICATED:

            logger.info(f"{ip_address}: User [{user_id}] is authenticated")

            logger.info(f"Connection lookup: {CONNECTION_LOOKUP}")

            # broadcast to everyone in the quest
            if action == "broadcast_to_quest":
                await broadcast_to_quest(user_id, quest_code, data, ip_address)

            # send to user
            if action == "send_to_user_in_quest":
                await send_to_user_in_quest(quest_code, data, ip_address)

            if action == "set_data":
                await send_to_user_in_quest(quest_code, data, ip_address)

            if action == "get_data":
                await get_data(quest_code, user_id, data, ip_address, handler, connection)

            # disconnect user
            if action == "disconnect_user":
                await disconnect_user(quest_code, data, ip_address)

            # wait for another action
            return await handler(connection)

        # if connection is not authenticated
        await connection.close()

    except websockets.exceptions.ConnectionClosedError:
        logger.info(f"{connection.remote_address[0]}: Connection closed by error")
        pass

    except websockets.exceptions.ConnectionClosedOK:
        if "system" in connection.path:
            logger.opt(colors=True).info("<red>System Connection >>> Connection Closed</red>")
        else:
            logger.info(f"{connection.remote_address[0]}: Connection closed")
        pass

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON: {connection.recv()}")
        await connection.close()

    finally:
        if connection in CONNECTIONS:
            CONNECTIONS.remove(connection)
        if connection in AUTHENTICATED:
            AUTHENTICATED.remove(connection)
