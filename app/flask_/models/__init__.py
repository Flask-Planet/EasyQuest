from datetime import datetime
from datetime import timedelta

from pytz import timezone

from .__mixins__ import CrudMixin
from .character import Character
from .genre import Genre
from .quest import Quest
from .user import User
from .system import System


def dater(ltz: str = "Europe/London", mask: str = "%Y-%m-%d %H:%M:%S", days_delta: int = 0) -> datetime:
    local_tz = timezone(ltz)
    if days_delta < 0:
        apply_delta = (datetime.now(local_tz) - timedelta(days=abs(days_delta))).strftime(mask)
        return datetime.strptime(apply_delta, mask)
    if days_delta > 0:
        apply_delta = (datetime.now(local_tz) + timedelta(days=days_delta)).strftime(mask)
        return datetime.strptime(apply_delta, mask)
    return datetime.strptime(datetime.now(local_tz).strftime(mask), mask)


__all__ = [
    "dater",
    "CrudMixin",
    "Character",
    "Genre",
    "Quest",
    "User",
    "System",
]
