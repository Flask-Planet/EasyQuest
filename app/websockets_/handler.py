import json

import websockets

from app.websockets_ import CONNECTIONS, CONNECTION_LOOKUP, AUTHENTICATED
from .actions import disconnect_user_id, send_to_user_id
from .authenticate import authenticate
from .broadcast import broadcast

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
        'to_user_id': 2,
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
        print(f"Connection established: {connection.remote_address[0]} - {connection}")

        print(connection.path)

    try:

        inbound = await connection.recv()

        # parse inbound message
        payload = json.loads(inbound)

        # split payload
        user_id = payload.get("user_id")
        token = payload.get("token")
        action = payload.get("action", "disconnect")
        data = payload.get("data")

        if connection.path == "/--ws--/system":
            if connection.remote_address[0] in ["127.0.0.1", "::1"]:
                AUTHENTICATED.add(connection)

        # disconnect
        if action == "disconnect":
            await connection.close()

        # authenticate connection
        if action == "authenticate":
            await authenticate(connection, handler, token, user_id)

        # Connection is already authenticated
        if connection in AUTHENTICATED:

            # disconnect user_id
            if action == "disconnect_user_id":
                await disconnect_user_id(data)

            # broadcast to all connected clients
            if action == "broadcast":
                await broadcast(connection, handler, data)

            # send to user_id
            if action == "send_to_user_id":
                await send_to_user_id(data)

            return handler(connection)

        await connection.close()

    except websockets.exceptions.ConnectionClosedError:
        print(f"Connection closed: {connection}")
        pass

    except websockets.exceptions.ConnectionClosedOK:
        print(f"Connection closed: {connection}")
        pass

    except json.JSONDecodeError:
        print(f"Invalid JSON: {connection}")
        await connection.close()

    finally:
        if connection in CONNECTIONS:
            CONNECTIONS.remove(connection)
        if connection in AUTHENTICATED:
            AUTHENTICATED.remove(connection)

        # remove user_id from lookup
        this_user_id = [k for k, v in CONNECTION_LOOKUP.items() if v == connection]
        if this_user_id:
            del CONNECTION_LOOKUP[this_user_id[0]]
