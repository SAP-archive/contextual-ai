from typing import Iterator, Dict

import dateutil
from pandas import DataFrame
from xai.data.exceptions import ItemDataTypeNotSupported
from xai.data.explorer.abstract_analyzer import AbstractDataAnalyzer
from xai.data.explorer.datetime.datetime_stats import DatetimeStats


class DatetimeDataAnalyzer(AbstractDataAnalyzer):
    """
    NumericalDataAnalyzer generates key stats for numerical values fed into the analyzer.
    """
    SUPPORTED_TYPES = [str]
    YEAR = 0
    MONTH = 1
    DAY = 2
    WEEKDAY = 3
    HOUR = 4
    MINUTE = 5
    SECOND = 6

    def __init__(self):
        super(DatetimeDataAnalyzer, self).__init__()
        self.time_df = DataFrame(
            columns=[DatetimeDataAnalyzer.YEAR, DatetimeDataAnalyzer.MONTH, DatetimeDataAnalyzer.DAY,
                     DatetimeDataAnalyzer.WEEKDAY, DatetimeDataAnalyzer.HOUR, DatetimeDataAnalyzer.MINUTE,
                     DatetimeDataAnalyzer.SECOND])
        self._frequency = dict()
        self.stats = DatetimeStats()

    def feed(self, value: str):
        """
        fed the datetime str into analyzer and aggregate count based on resolution
        Args:
           value: datetime str

        """
        if type(value) not in DatetimeDataAnalyzer.SUPPORTED_TYPES:
            raise ItemDataTypeNotSupported(type(value), type(self), DatetimeDataAnalyzer.SUPPORTED_TYPES)
        date_obj = self.__parse_date(value)
        if date_obj is not None:
            self.time_df.append(DataFrame().from_records(date_obj))

    def get_statistics(self, resolution_list=None) -> Dict:
        if resolution_list is None:
            resolution_list = [DatetimeDataAnalyzer.YEAR, DatetimeDataAnalyzer.MONTH]
        resolution_list = sorted(resolution_list)
        self.stats = DatetimeStats()
        group_count_dict = self.time_df.groupby(by=resolution_list).groups
        self.stats.updates_stats_from_datetime_frame(group_count_dict, resolution_list)
        return self.stats.to_json()

    def __parse_date(self, date):
        try:
            dt = dateutil.parser.parse(str(date))
            dt_obj = dict()
            dt_obj[DatetimeDataAnalyzer.YEAR] = dt.year
            dt_obj[DatetimeDataAnalyzer.MONTH] = dt.month
            dt_obj[DatetimeDataAnalyzer.DAY] = dt.day
            dt_obj[DatetimeDataAnalyzer.HOUR] = dt.hour
            dt_obj[DatetimeDataAnalyzer.MINUTE] = dt.minute
            dt_obj[DatetimeDataAnalyzer.SECOND] = dt.second
            dt_obj[DatetimeDataAnalyzer.WEEKDAY] = dt.weekday
            return dt_obj
        except ValueError:
            self.invalid_count += 1
            return None
