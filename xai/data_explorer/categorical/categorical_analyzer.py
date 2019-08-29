from collections import defaultdict
from typing import Iterator, List

from xai.data_explorer.abstract_analyzer import AbstractDataAnalyzer
from xai.data_explorer.categorical.categorical_stats import CategoricalStats
from xai.data_explorer.config import DICT_ANALYZER_TO_SUPPORTED_ITEM_DATA_TYPE
from xai.data_explorer.data_exceptions import ItemDataTypeNotSupported


class CategoricalDataAnalyzer(AbstractDataAnalyzer):
    """
    CategoricalDataAnalyzer accumulate frequency count for all values fed into the analyzer.
    """

    def __init__(self):
        super(CategoricalDataAnalyzer, self).__init__()
        self._frequency_count = defaultdict(int)
        self.stats = None

    def feed(self, value: List or int or str):
        """
        accumulate count for value
        Args:
           value: value that fed for frequency count update

        """
        if type(value) != list:
            value = [value]

        for v in value:
            if type(v) not in DICT_ANALYZER_TO_SUPPORTED_ITEM_DATA_TYPE[type(self)]:
                raise ItemDataTypeNotSupported(type(v), type(self))
            self._frequency_count[v] += 1

    def feed_all(self, values: Iterator):
        """
        accumulate count for each value in value list
        Args:
            values: values that fed for frequency count update

        """
        for value in values:
            self.feed(value)

    def get_statistics(self) -> CategoricalStats:
        """
        return stats for the analyzer
        Returns:
            a CategoricalStats object that keeps track of frequency count
        """
        self.stats = CategoricalStats()
        for value, count in self._frequency_count.items():
            self.stats.update_count_by_value(value, count)
        return self.stats
