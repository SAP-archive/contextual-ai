from abc import abstractmethod, ABC
from typing import Dict


class AbstractStats(ABC):
    """
    Abstract class for data statistics for all types data analyzer
    """

    def __init__(self):
        self._total_count = 0

    @property
    def total_count(self):
        return self._total_count

    @abstractmethod
    def to_json(self) -> Dict:
        """
        Map the stats to json object

        Returns:
            A dictionary contains key statistical attribute
        """
        raise NotImplementedError('The derived helper needs to implement it.')
