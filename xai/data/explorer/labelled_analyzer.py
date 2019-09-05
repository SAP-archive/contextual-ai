from abc import ABC
from typing import List, Dict, Union, Tuple

from xai.data.abstract_stats import AbstractStats
from xai.data.exceptions import InconsistentIteratorSize


class LabelledDataAnalyzer(ABC):

    def __init__(self, data_analyzer_cls):
        self._label_analyzer = dict()
        self._analyzer_cls = data_analyzer_cls
        self._all_analyzer = data_analyzer_cls()

    def feed(self, value: Union[str, int], label: Union[str, int]):
        """
        update the analyzer with value and its corresponding label

        Args:
            value: categorical value
            label: corresponding label for the categorical value
        """
        if label not in self._label_analyzer:
            self._label_analyzer[label] = self._analyzer_cls()
        self._label_analyzer[label].feed(value)
        self._all_analyzer.feed(value)

    def feed_all(self, values: List, labels: List):
        """
        update the analyzer with a list of values and their corresponding labels

        Args:
            values: categorical values
            labels: corresponding labels for each categorical value
        """
        if len(values) != len(labels):
            raise InconsistentIteratorSize(len(values), len(labels))

        value_label = zip(values, labels)
        for value, label in value_label:
            self.feed(value, label)

    def get_statistics(self) -> Tuple[Dict[Union[str, int], AbstractStats], AbstractStats]:
        """
        get stats based on labels
        Returns:
            a dictionary maps label to the aggregated stats json obj
        """
        _stats = dict()
        for label, analyzer in self._label_analyzer.items():
            _stats[label] = analyzer.get_statistics()
        _all_stats = self._all_analyzer.get_statistics()
        return _stats, _all_stats
