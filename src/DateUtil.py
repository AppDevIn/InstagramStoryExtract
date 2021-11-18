from datetime import date, datetime
from pytz import timezone


class DateUtil:

    DATE_FORMAT = "%Y%m%d"
    DATETIME_FORMAT = "%Y%m%d%H%M%S"

    @staticmethod
    def getCurrentDate() -> str:
        today = date.today()
        return today.strftime("%Y%m%d")

    @staticmethod
    def utc_time_to_zone(utc_datetime: datetime, zone: str) -> datetime:
        tz = timezone(zone)
        utc_datetime = (utc_datetime + tz.utcoffset(utc_datetime, is_dst=True))
        return utc_datetime
