#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import dateutil
from pandas import DataFrame
from typing import List, Optional

from xai.data.constants import DatetimeResolution
from xai.data.exceptions import ItemDataTypeNotSupported, InconsistentSize
from xai.data.explorer.abstract_analyzer import AbstractDataAnalyzer
from xai.data.explorer.datetime.datetime_stats import DatetimeStats


class DatetimeDataAnalyzer(AbstractDataAnalyzer):
    """
    This analyzer class analyzes datetime data and generates key stats for values fed into it
    """

    SUPPORTED_TYPES = [str, int]

    DICT_MAP_NUMBER_TO_RESOLUTION = {
        DatetimeResolution.YEAR: 'year',
        DatetimeResolution.MONTH: 'month',
        DatetimeResolution.DAY: 'day',
        DatetimeResolution.WEEKDAY: 'weekday',
        DatetimeResolution.HOUR: 'hour',
        DatetimeResolution.MINUTE: 'minute',
        DatetimeResolution.SECOND: 'second'
    }

    def __init__(self):
        super(DatetimeDataAnalyzer, self).__init__()
        self._time_records = []
        self._frequency = dict()
        self.invalid_count =  0

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
                dt_obj[DatetimeResolution.YEAR] = dt.year
                dt_obj[DatetimeResolution.MONTH] = dt.month
                dt_obj[DatetimeResolution.DAY] = dt.day
                dt_obj[DatetimeResolution.HOUR] = dt.hour
                dt_obj[DatetimeResolution.MINUTE] = dt.minute
                dt_obj[DatetimeResolution.SECOND] = dt.second
                dt_obj[DatetimeResolution.WEEKDAY] = dt.weekday()
                return dt_obj
            except ValueError:
                self.invalid_count += 1
                return None

        if type(value) not in DatetimeDataAnalyzer.SUPPORTED_TYPES:
            raise ItemDataTypeNotSupported(type(value), type(self), DatetimeDataAnalyzer.SUPPORTED_TYPES)
        date_obj = __parse_date(value)
        if date_obj is not None:
            self._time_records.append(date_obj)

    def get_statistics(self, resolution_list: Optional[List[str]] = None) -> DatetimeStats:
        """

        Args:
            resolution_list:

        Returns:

        """
        if resolution_list is None:
            resolution_list = [DatetimeResolution.YEAR, DatetimeResolution.MONTH]
        resolution_list = sorted(resolution_list)
        _time_df = DataFrame.from_records(self._time_records)

        group_count_dict = _time_df.groupby(by=resolution_list).groups

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
            group_dict = frequency_count

        stats = DatetimeStats(frequency_count=frequency_count,
                              resolution_list=resolution_list)
        return stats
