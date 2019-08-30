from typing import Iterator, List

from xai.data.exceptions import ItemDataTypeNotSupported
from xai.data.explorer.abstract_analyzer import AbstractDataAnalyzer
from xai.data.explorer.numerical.numerical_stats import NumericalStats


class NumericDataAnalyzer(AbstractDataAnalyzer):
    """
    NumericalDataAnalyzer generates key stats for numerical values fed into the analyzer.
    """
    SUPPORTED_TYPES = [int, float]

    def __init__(self):
        super(NumericDataAnalyzer, self).__init__()
        self._values = []
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
            if type(v) not in NumericDataAnalyzer.SUPPORTED_TYPES:
                raise ItemDataTypeNotSupported(type(v), type(self), NumericDataAnalyzer.SUPPORTED_TYPES)
            self._values.append(value)

    def feed_all(self, values: Iterator):
        """
        accumulate count for each value in value list
        Args:
            values: values that fed for frequency count update

        """
        for value in values:
            self.feed(value)

    def get_statistics(self) -> NumericalStats:
        """
        return stats for the analyzer
        Returns:
            a NumericalStats object that stores key stats for numerical data
        """
        self.stats = NumericalStats()
        self.stats.updates_stats_from_values(self.values)
        return self.stats
