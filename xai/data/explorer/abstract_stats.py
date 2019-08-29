from abc import abstractmethod, ABC
from typing import Dict


class AbstractStats(ABC):
    """
    Abstract class for data statistics for all types data analyzer
    """

    def __init__(self):
        self._total_count = 0

    @abstractmethod
    def get_total_count(self)->int:
        """
        update the _total_count attribute
        Returns:
            total number of samples in the stats object
        """
        raise NotImplementedError('The derived helper needs to implement it.')

    @abstractmethod
    def to_json(self)-> Dict:
        """
        map the stats to json object
        Returns:
            a dictionary contains key statistical attribute
        """
        raise NotImplementedError('The derived helper needs to implement it.')
