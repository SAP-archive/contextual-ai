from typing import List, Optional

import dateutil
from pandas import DataFrame

from xai.data.exceptions import ItemDataTypeNotSupported, InconsistentSize
from xai.data.explorer.abstract_analyzer import AbstractDataAnalyzer
from xai.data.explorer.datetime.datetime_stats import DatetimeStats


class DatetimeDataAnalyzer(AbstractDataAnalyzer):
    """
    This analyzer class analyzes datetime data and generates key stats for values fed into it
    """

    SUPPORTED_TYPES = [str]
    YEAR = 0
    MONTH = 1
    DAY = 2
    WEEKDAY = 3
    HOUR = 4
    MINUTE = 5
    SECOND = 6

    DICT_MAP_NUMBER_TO_RESOLUTION = {
        YEAR: 'year',
        MONTH: 'month',
        DAY: 'day',
        WEEKDAY: 'weekday',
        HOUR: 'hour',
        MINUTE: 'minute',
        SECOND: 'second'
    }

    def __init__(self):
        super(DatetimeDataAnalyzer, self).__init__()
        self._time_df = DataFrame(
            columns=[DatetimeDataAnalyzer.YEAR, DatetimeDataAnalyzer.MONTH, DatetimeDataAnalyzer.DAY,
                     DatetimeDataAnalyzer.WEEKDAY, DatetimeDataAnalyzer.HOUR, DatetimeDataAnalyzer.MINUTE,
                     DatetimeDataAnalyzer.SECOND])
        self._frequency = dict()
        self.stats = DatetimeStats()

    def feed(self, value: str):
        """
        Feed the datetime str into analyzer and aggregate count based on resolution

        Args:
           value: datetime str

        """

        def __parse_date(date):
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

        if type(value) not in DatetimeDataAnalyzer.SUPPORTED_TYPES:
            raise ItemDataTypeNotSupported(type(value), type(self), DatetimeDataAnalyzer.SUPPORTED_TYPES)
        date_obj = __parse_date(value)
        if date_obj is not None:
            self._time_df.append(DataFrame().from_records(date_obj))

    def get_statistics(self, resolution_list: Optional[List[str]] = None) -> DatetimeStats:
        if resolution_list is None:
            resolution_list = [DatetimeDataAnalyzer.YEAR, DatetimeDataAnalyzer.MONTH]
        resolution_list = sorted(resolution_list)
        group_count_dict = self._time_df.groupby(by=resolution_list).groups

        frequency_count = dict()
        group_dict = frequency_count
        for groups, index in group_count_dict.items():
            if len(groups) != len(resolution_list):
                raise InconsistentSize(column_A='group title', column_B='time resolution',
                                       length_A=len(groups), length_B=len(resolution_list))
            for group in groups[:-1]:
                if group not in group_dict.keys():
                    group_dict[group] = dict()
                group_dict = group_dict[group]
            group_dict[groups[-1]] = len(index)

        self.stats = DatetimeStats(frequency_count=frequency_count,
                                   resolution_list=resolution_list)
        return self.stats
