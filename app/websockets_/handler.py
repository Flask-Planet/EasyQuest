import json

import websockets
from app.websockets_ import CONNECTIONS, CONNECTION_LOOKUP, AUTHENTICATED
from .authenticate import authenticate
from .broadcast import broadcast
from .close_wsid_connection import close_wsid_connection


async def handler(websocket):
    if websocket not in CONNECTIONS:
        CONNECTIONS.add(websocket)
        print(f"Connection established: {websocket.remote_address[0]} - {websocket}")

    try:
        inbound = await websocket.recv()

        this_wsid = [k for k, v in CONNECTION_LOOKUP.items() if v == websocket]

        # parse inbound message
        payload = json.loads(inbound)
        # split payload
        token = payload.get("token")
        action = payload.get("action")
        data = payload.get("data")

        # disconnect
        if action == "disconnect":
            await websocket.close()

        if websocket.path == "/system":
            if websocket.remote_address[0] == "127.0.0.1":
                AUTHENTICATED.add(websocket)

        # Connection is already authenticated
        if websocket in AUTHENTICATED:
            print("Authenticated connection")

            if action == "disconnect":
                to_wsid = data.get("to_wsid")
                if to_wsid in CONNECTION_LOOKUP:
                    await CONNECTION_LOOKUP[to_wsid].send(
                        json.dumps({
                            "action": "disconnect",
                            "data": None,
                        }))
                    await close_wsid_connection(to_wsid)

            # broadcast to all connected clients
            if action == "broadcast":
                await broadcast(websocket, handler, data)

            if action == "direct_message":
                to_wsid = data.get("to_wsid")
                if to_wsid in CONNECTION_LOOKUP:
                    await CONNECTION_LOOKUP[to_wsid].send(
                        json.dumps(
                            {
                                "action": "direct_message",
                                "data": {
                                    "from_wsid": this_wsid[0]
                                    if this_wsid
                                    else "server"
                                    if websocket.remote_address[0] == "::1"
                                    else "unknown",
                                    "message": data.get("message"),
                                },
                            }
                        )
                    )

            if action == "alert":
                to_wsid = data.get("to_wsid")
                if to_wsid in CONNECTION_LOOKUP:
                    await CONNECTION_LOOKUP[to_wsid].send(
                        json.dumps(
                            {
                                "action": "alert",
                                "data": {
                                    "from_wsid": this_wsid[0]
                                    if this_wsid
                                    else "server"
                                    if websocket.remote_address[0] == "::1"
                                    else "unknown",
                                    "message": data.get("message"),
                                },
                            }
                        )
                    )

            return handler(websocket)

        # authenticate connection
        if action == "authenticate":
            await authenticate(websocket, handler, token, data.get("wsid"))

        await websocket.close()

    except websockets.exceptions.ConnectionClosedError:
        print(f"Connection closed: {websocket}")
        pass

    except websockets.exceptions.ConnectionClosedOK:
        print(f"Connection closed: {websocket}")
        pass

    finally:
        if websocket in CONNECTIONS:
            CONNECTIONS.remove(websocket)
        if websocket in AUTHENTICATED:
            AUTHENTICATED.remove(websocket)

        # remove wsid from lookup
        this_wsid = [k for k, v in CONNECTION_LOOKUP.items() if v == websocket]
        if this_wsid:
            del CONNECTION_LOOKUP[this_wsid[0]]
