from abc import ABC
from typing import Iterator, Dict

from xai.data.exceptions import InconsistentIteratorSize


class LabelledDataAnalyzer(ABC):

    def __init__(self, data_analyzer_cls):
        self.labelled_stats = dict()
        self.analyzer_cls = data_analyzer_cls

    def feed(self, value: str or int, label: str or int):
        """
        update the analyzer with value and its corresponding label

        Args:
            value: categorical value
            label: corresponding label for the categorical value
        """
        if label not in self._label_analyzer:
            self._label_analyzer[label] = self.analyzer_cls()
        self._label_analyzer[label].feed(value)

    def feed_all(self, values: Iterator, labels: Iterator):
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

    def get_statistics(self) -> Dict[str or int:Dict]:
        """
        get stats based on labels
        Returns:
            a dictionary maps label to the aggregated stats json obj
        """
        self._stats = dict()
        for label, analyzer in self._label_analyzer.items():
            self._stats[label] = analyzer.get_statistics()
        return self._stats
