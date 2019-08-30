from collections import defaultdict
from typing import Iterator, List, Dict

from xai.data.exceptions import ItemDataTypeNotSupported
from xai.data.explorer.abstract_analyzer import AbstractDataAnalyzer
from xai.data.explorer.categorical.categorical_stats import CategoricalStats


class CategoricalDataAnalyzer(AbstractDataAnalyzer):
    """
    CategoricalDataAnalyzer accumulate frequency count for all values fed into the analyzer.
    """

    SUPPORTED_TYPES = [str, int]

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
            if type(v) not in CategoricalDataAnalyzer.SUPPORTED_TYPES:
                raise ItemDataTypeNotSupported(type(v), type(self), CategoricalDataAnalyzer.SUPPORTED_TYPES)
            self._frequency_count[v] += 1

    def feed_all(self, values: Iterator):
        """
        accumulate count for each value in value list
        Args:
            values: values that fed for frequency count update

        """
        for value in values:
            self.feed(value)

    def get_statistics(self) -> Dict:
        """
        return stats for the analyzer
        Returns:
            a CategoricalStats json object that keeps track of frequency count
        """
        self.stats = CategoricalStats()
        for value, count in self._frequency_count.items():
            self.stats.update_count_by_value(value, count)
        return self.stats.to_json()
