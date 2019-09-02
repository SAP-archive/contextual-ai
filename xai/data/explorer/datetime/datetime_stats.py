from typing import Dict

from xai.data.constants import STATSKEY
from xai.data.exceptions import InconsistentSize
from xai.data.abstract_stats import AbstractStats


class DatetimeStats(AbstractStats):
    DICT_MAP_NUMBER_TO_RESOLUTION = {
        0: 'year',
        1: 'month',
        2: 'day',
        3: 'weekday',
        4: 'hour',
        5: 'minute',
        6: 'second'
    }

    def __init__(self):
        self._total_count = 0
        self._frequency_count = dict()
        self.resolution_list = []

    def updates_stats_from_group_count_dict(self, group_count_dict, resolution_list):
        self.resolution_list = resolution_list
        group_dict = self._frequency_count
        for groups, index in group_count_dict.items():
            if len(groups) != len(resolution_list):
                raise InconsistentSize(column_A='Group title', column_B='Time resolution',
                                       length_A=len(groups), length_B=len(resolution_list))
            for group in groups[:-1]:
                if group not in group_dict.keys():
                    group_dict[group] = dict()
                group_dict = group_dict[group]
            group_dict[groups[-1]] = len(index)

    def to_json(self) -> Dict:
        """
        map stats information into a json object

        Returns:
            a json that represents frequency count and total count
        """

        json_obj = dict()
        json_obj[STATSKEY.TOTAL_COUNT] = self._total_count
        json_obj[STATSKEY.DISTRIBUTION] = self._frequency_count
        json_obj[STATSKEY.FIELDS] = self.resolution_list
        return json_obj
