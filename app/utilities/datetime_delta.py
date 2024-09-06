import random
import timeit
from datetime import datetime
from datetime import timedelta

from pytz import timezone

"""
pip install pytz
"""


class DateTimeIsNoneError(Exception):
    pass


class DatetimeDeltaRI:
    """
    Produces timezone-aware dates
    Returns a new instance of the class when a method is called

    RI = Return Instance

    https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
    """

    _local_tz: str
    _format: str
    _timezone: timezone
    _datetime: datetime

    def __init__(
        self,
        ltz: str = "Europe/London",
        format_: str = "%Y-%m-%d %H:%M:%S",
        datetime_: datetime = None,
    ):
        self._local_tz = ltz
        self._format = format_
        self._timezone = timezone(ltz)
        if datetime_:
            self._datetime = datetime_.replace(tzinfo=self._timezone)
        else:
            self._datetime = datetime.now(self._timezone)

    def set_format(self, format_: str = "%Y-%m-%d %H:%M:%S") -> "DatetimeDeltaRI":
        return DatetimeDeltaRI(
            ltz=self._local_tz, format_=format_, datetime_=self._datetime
        )

    def days(self, days_delta: int) -> "DatetimeDeltaRI":
        return DatetimeDeltaRI(
            ltz=self._local_tz,
            format_=self._format,
            datetime_=self._datetime + timedelta(days=days_delta),
        )

    def hours(self, hours_delta: int) -> "DatetimeDeltaRI":
        return DatetimeDeltaRI(
            ltz=self._local_tz,
            format_=self._format,
            datetime_=self._datetime + timedelta(hours=hours_delta),
        )

    def minutes(self, minuets_delta: int) -> "DatetimeDeltaRI":
        return DatetimeDeltaRI(
            ltz=self._local_tz,
            format_=self._format,
            datetime_=self._datetime + timedelta(minutes=minuets_delta),
        )

    def __str__(self) -> str:
        return self._datetime.strftime(self._format)

    @property
    def datetime(self) -> datetime:
        return self._datetime

    @property
    def timestamp(self) -> int:
        return int(self._datetime.timestamp())

    @property
    def timezone(self) -> timezone:
        return self._timezone


class DatetimeDeltaMC:
    """
    Produces timezone-aware dates
    Returns self when a method is called

    MC = Method Chaining

    https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List
    """

    _local_tz: str
    _format: str
    _timezone: timezone
    _datetime: datetime

    def __init__(
        self,
        ltz: str = "Europe/London",
        format_: str = "%Y-%m-%d %H:%M:%S",
        datetime_: datetime = None,
    ):
        self._local_tz = ltz
        self._format = format_
        self._timezone = timezone(ltz)
        if datetime_:
            self._datetime = datetime_.replace(tzinfo=self._timezone)
        else:
            self._datetime = datetime.now(self._timezone)

    def set_format(self, format_: str = "%Y-%m-%d %H:%M:%S") -> "DatetimeDeltaMC":
        self._format = format_
        return self

    def days(self, days_delta: int) -> "DatetimeDeltaMC":
        self._datetime = self._datetime + timedelta(days=days_delta)
        return self

    def hours(self, hours_delta: int) -> "DatetimeDeltaMC":
        self._datetime = self._datetime + timedelta(hours=hours_delta)
        return self

    def minutes(self, minuets_delta: int) -> "DatetimeDeltaMC":
        self._datetime = self._datetime + timedelta(minutes=minuets_delta)
        return self

    def __str__(self) -> str:
        return self._datetime.strftime(self._format)

    @property
    def datetime(self) -> datetime:
        return self._datetime

    @property
    def timestamp(self) -> int:
        return int(self._datetime.timestamp())

    @property
    def timezone(self) -> timezone:
        return self._timezone


class DatetimeDeltaMCTZU:
    """
    Produces timezone-unaware dates
    Returns self when a method is called

    MCTZU = Method Chaining Time Zone Unaware
    """

    _output_format: str
    _datetime: datetime

    def __init__(
        self,
        output_format: str = "%Y-%m-%dT%H:%M:%S",
        datetime_: datetime = None,
    ):
        """
        Output format defaults to ISO
        """
        self._output_format = output_format
        if datetime_:
            self._datetime = datetime_

    def _error_if_datetime_none(self):
        if not self._datetime:
            raise DateTimeIsNoneError("datetime attribute cannot be none.")

    def set_output_format(
        self, format_: str = "%Y-%m-%dT%H:%M:%S"
    ) -> "DatetimeDeltaMCTZU":
        self._output_format = format_
        return self

    def set_datetime_now(self) -> "DatetimeDeltaMCTZU":
        self._datetime = datetime.now()
        return self

    def set_datetime(
        self, datetime_str: str, format_: str = "%Y-%m-%dT%H:%M:%S"
    ) -> "DatetimeDeltaMCTZU":
        self._datetime = datetime.strptime(datetime_str, format_)
        return self

    def days(self, days_delta: int) -> "DatetimeDeltaMCTZU":
        self._error_if_datetime_none()
        self._datetime = self._datetime + timedelta(days=days_delta)
        return self

    def hours(self, hours_delta: int) -> "DatetimeDeltaMCTZU":
        self._error_if_datetime_none()
        self._datetime = self._datetime + timedelta(hours=hours_delta)
        return self

    def minutes(self, minuets_delta: int) -> "DatetimeDeltaMCTZU":
        self._error_if_datetime_none()
        self._datetime = self._datetime + timedelta(minutes=minuets_delta)
        return self

    def __str__(self) -> str:
        self._error_if_datetime_none()
        return self._datetime.strftime(self._output_format)

    @property
    def as_str(self) -> str:
        self._error_if_datetime_none()
        return self._datetime.strftime(self._output_format)

    @property
    def datetime(self) -> datetime:
        self._error_if_datetime_none()
        return self._datetime

    @property
    def timestamp(self) -> int:
        self._error_if_datetime_none()
        return int(self._datetime.timestamp())


if __name__ == "__main__":
    """
    Small test to compare the performance of returning a new instance of the class
    """

    def returning_new_inst():
        today = DatetimeDeltaRI().set_format("%Y-%m-%d %H:%M:%S")
        today.days(random.randint(-10, 10)).hours(random.randint(-10, 10)).minutes(
            random.randint(-10, 10)
        )

    def returning_self():
        today = DatetimeDeltaMC().set_format("%Y-%m-%d %H:%M:%S")
        today.days(random.randint(-10, 10)).hours(random.randint(-10, 10)).minutes(
            random.randint(-10, 10)
        )

    def returning_self_timezone_unaware():
        today = (
            DatetimeDeltaMCTZU()
            .set_output_format("%Y-%m-%d %H:%M:%S")
            .set_datetime_now()
        )
        today.days(random.randint(-10, 10)).hours(random.randint(-10, 10)).minutes(
            random.randint(-10, 10)
        )

    print(timeit.timeit(stmt=returning_new_inst, number=10000))

    print(timeit.timeit(stmt=returning_self, number=10000))

    print(timeit.timeit(stmt=returning_self_timezone_unaware, number=10000))
