from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Iterator


class AbstractValidator(ABC):
    """
    abstract class for validator.
    """
    def __init__(self, schema_meta: dict):
        self.schema_meta = schema_meta
        self.info_summary = defaultdict(dict)
    @abstractmethod
    def validate_sample(self, sample: dict):
        raise NotImplementedError('The derived class needs to implement it.')

    @abstractmethod
    def validate_all(self, samples: Iterator[dict]):
        raise NotImplementedError('The derived class needs to implement it.')

    @abstractmethod
    def get_statistics(self):
        """
        Returns:

        """
        raise NotImplementedError('The derived class needs to implement it.')
