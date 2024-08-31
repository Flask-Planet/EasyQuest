import asyncio
import json

import requests
import websockets
from dotenv import load_dotenv

CONNECTIONS = set()
AUTHENTICATED = set()
CONNECTION_LOOKUP = dict()

load_dotenv()


async def authenticate(websocket, handler_, token, wsid):
    global CONNECTIONS, AUTHENTICATED, CONNECTION_LOOKUP

    # authenticate connection with flask
    # TODO: replace with proper database connection.
    res = requests.get((f"http://127.0.0.1:5000/auth/ws/{token}"))

    if res.status_code == 200:
        res_json = res.json()
        if res_json.get("ok") is True:
            AUTHENTICATED.add(websocket)

            if wsid:
                CONNECTION_LOOKUP[wsid] = websocket

            await websocket.send(
                json.dumps({"action": "authenticate", "data": f"success: wsid={wsid}"})
            )
            await handler_(websocket)

    await websocket.send(json.dumps({"action": "authenticate", "data": "failed"}))


async def broadcast(websocket, handler_, data):
    global CONNECTIONS
    websockets.broadcast(CONNECTIONS, json.dumps(data))
    await handler_(websocket)


async def close_wsid_connection(wsid):
    global CONNECTION_LOOKUP
    CONNECTION_LOOKUP[wsid].close()


async def handler(websocket):
    global CONNECTIONS, AUTHENTICATED, CONNECTION_LOOKUP

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


async def main():
    async with websockets.serve(handler, "127.0.0.1", 5001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
