from typing import List, Iterator, Dict

from xai.data_explorer.abstract_labelled_analyzer import AbstractLabelledDataAnalyzer
from xai.data_explorer.categorical.categorical_analyzer import CategoricalDataAnalyzer
from xai.data_explorer.categorical.categorical_stats import CategoricalStats
from xai.data_explorer.data_exceptions import InconsistentIteratorSize


class LabelledCategoricalDataAnalyzer(AbstractLabelledDataAnalyzer):
    """
    LablledCategoricalDataAnalyzer aggregates categorical stats based on labels.
    """

    def __init__(self):
        super(LabelledCategoricalDataAnalyzer, self).__init__()
        self._label_analyzer = dict()
        self._stats = None

    def feed(self, value: str or int or List, label: str or int):
        """
        update the analyzer with value and its corresponding label

        Args:
            value: categorical value
            label: corresponding label for the categorical value
        """
        if label not in self._label_analyzer:
            self._label_analyzer[label] = CategoricalDataAnalyzer()
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

    def get_statistics(self) -> Dict[str or int:CategoricalStats]:
        """
        get stats based on labels
        Returns:
            a dictionary maps label to the aggregated stats obj
        """
        self._stats = dict()
        for label, analyzer in self._label_analyzer.items():
            self._stats[label] = analyzer.get_statistics()
        return self._stats
