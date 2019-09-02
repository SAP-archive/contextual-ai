from typing import Dict

from xai.data.abstract_stats import AbstractStats
from xai.data.constants import STATSKEY


class CategoricalStats(AbstractStats):
    """
    CategoricalStats contains following basic information:
        - _total_count: total count of values
        - _frequency_count: a dictionary maps categorical value to its frequency count
    """

    def __init__(self):
        self._total_count = 0
        self._frequency_count = dict()

    def update_count_by_value(self, value: str or int, count: int) -> Dict[str or int, int]:
        """
        update the frequency by value and count pair

        Args:
            value: value that is tracked
            count: frequency count for the value
        Returns:
            a dictionary maps value to its up-to-date frequency count
        """
        self._frequency_count[value] = count
        return self._frequency_count

    def get_total_count(self) -> int:
        """
        return the total count of values for the stats object

        Returns:
            total count of values
        """
        self._total_count = sum(list(self._frequency_count.items()))
        return self._total_count

    def to_json(self) -> Dict:
        """
        map stats information into a json object

        Returns:
            a json that represent frequency count and total count
        """

        json_obj = dict()
        json_obj[STATSKEY.TOTAL_COUNT] = self._total_count
        json_obj[STATSKEY.DISTRIBUTION] = []

        for attribute_name, attribute_count in self._frequency_count.items():
            json_obj[STATSKEY.DISTRIBUTION].append({STATSKEY.DISTRIBUTION_KEY.ATTRIBUTE_NAME: attribute_name,
                                                    STATSKEY.DISTRIBUTION_KEY.ATTRIBUTE_COUNT: attribute_count})

        return json_obj
