from abc import abstractmethod, ABC
from typing import Iterator, Dict


class AbstractLabelledDataAnalyzer(ABC):

    def __init__(self):
        self.labelled_stats = dict()

    @abstractmethod
    def feed(self, value, label):
        """
        The function feeds one value into analyzer and update the stats object.

        Args:
            value: the value fed into the analyzer for one sample
            label: label for the value
        """
        raise NotImplementedError('The derived helper needs to implement it.')

    @abstractmethod
    def feed_all(self, values: Iterator, labels: Iterator):
        """
        The function takes one iterator of values and one iterator of labels into analyzer and update the stats object
        for each value according to its label.
        Args:
            values: values fed into the analyzer in sequence
            labels: labels for values
        """
        raise NotImplementedError('The derived helper needs to implement it.')

    @abstractmethod
    def get_statistics(self) -> Dict:
        """
        The function returns the up-to-date statistics that the analyzer keeps track
        Returns:
            A dictionary maps label to its stats json object extends AbstractStats based on data type.
        """
        raise NotImplementedError('The derived helper needs to implement it.')
