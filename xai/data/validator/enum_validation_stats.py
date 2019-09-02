from typing import List, Dict
from xai.data.abstract_stats import AbstractStats
from xai.data.constants import STATSKEY


class EnumValidationStats(AbstractStats):
    def __init__(self):
        super(EnumValidationStats).__init__()
        self._column_stats = None
        self._total_count = 0

    def update_stats(self, column_stats, total_count):
        self._column_stats = column_stats
        self._total_count = total_count

    def to_json(self) -> List[Dict]:
        json_obj = dict()
        json_obj[STATSKEY.TOTAL_COUNT] = self._total_count
        json_obj[STATSKEY.DISTRIBUTION] = list()
        for feature_name, count in self._column_stats.items():
            json_column_obj = dict()
            json_column_obj['field'] = feature_name
            json_column_obj['valid_count'] = count
            json_obj[STATSKEY.DISTRIBUTION].append(json_column_obj)

        return json_obj
