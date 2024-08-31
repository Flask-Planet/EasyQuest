from app.websockets_ import CONNECTION_LOOKUP


async def close_wsid_connection(wsid):
    CONNECTION_LOOKUP[wsid].close()
