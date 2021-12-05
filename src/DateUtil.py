from datetime import date, datetime
from pytz import timezone


class DateUtil:

    DATE_FORMAT = "%Y%m%d"
    DATETIME_FORMAT = "%Y%m%d%H%M%S"
    TIME_FORMAT = "%H_%M_%S"
    TIME_FORMAT_NO_UNDERSCORE = "%H:%M:%S"
    DATETIME_FORMAT_WITH_UNDERSCORE = "%Y_%m_%d_%H_%M_%S"

    @staticmethod
    def getCurrentDateTime():
        return datetime.now()

    @staticmethod
    def utc_time_to_zone(utc_datetime: datetime, zone: str) -> datetime:
        tz = timezone(zone)
        utc_datetime = (utc_datetime + tz.utcoffset(utc_datetime, is_dst=True))
        return utc_datetime
