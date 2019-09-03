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

    def feed(self, value: int or str):
        """
        accumulate count for value
        Args:
           value: value that fed for frequency count update

        """
        if type(value) not in CategoricalDataAnalyzer.SUPPORTED_TYPES:
            raise ItemDataTypeNotSupported(type(value), type(self), CategoricalDataAnalyzer.SUPPORTED_TYPES)
        self._frequency_count[value] += 1

    def get_statistics(self) -> CategoricalStats:
        """
        return stats for the analyzer
        Returns:
            a CategoricalStats json object that keeps track of frequency count
        """
        self.stats = CategoricalStats(frequency_count=self._frequency_count)
        return self.stats
