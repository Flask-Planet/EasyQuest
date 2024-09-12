import json
import os
import typing as t

from websockets.sync.client import connect


class WebSocketService:
    base_url = "ws://localhost:5001/--ws--"

    def __init__(self, base_url=os.getenv("WS_URL")) -> None:
        if base_url:
            self.base_url = base_url

    def _build_url(self, quest_code: str) -> str:
        return f"{self.base_url}/quest/{quest_code}/system"

    def send(self, quest_code: str, payload: t.Dict[str, t.Any]) -> t.Any:
        if payload is None:
            payload = {}

        with connect(self._build_url(quest_code)) as websocket:
            websocket.send(json.dumps(payload))
