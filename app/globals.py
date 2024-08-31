import typing as t

VITALS = {
    'health': 100,
    'sleeping': False,
    'confused': False,
    'poisoned': False,
}

STATS = {
    'strength': 1,
    'agility': 1,
    'intelligence': 1,
    'luck': 1,
    'perception': 1,
    'persuasion': 1,
}


class APIResponse:
    @staticmethod
    def success(
            message: str,
            data: t.Optional[
                str
                | int
                | float
                | bool
                | t.Dict[str, t.Any]
                | t.List[t.Dict[str, t.Any] | str | int | float | bool]
                ] = None,
    ) -> t.Dict[str, t.Any]:
        return {"ok": True, "message": message, "data": data}

    @staticmethod
    def fail(
            message: str,
            data: t.Optional[
                str
                | int
                | float
                | bool
                | t.Dict[str, t.Any]
                | t.List[t.Dict[str, t.Any] | str | int | float | bool]
                ] = None,
    ) -> t.Dict[str, t.Any]:
        return {"ok": False, "message": message, "data": data}
