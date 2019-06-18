from abc import ABC, abstractmethod
from typing import Iterator
from collections import defaultdict


class AbstractValidator(ABC):
    def __init__(self, schema_meta: dict):
        self.schema_meta = schema_meta
        self.info_summary = defaultdict(dict)
    @abstractmethod
    def validate_sample(self, sample: dict):
        raise NotImplementedError('The derived class needs to implement it.')

    @abstractmethod
    def validate_set(self, sample_list: Iterator[dict]):
        raise NotImplementedError('The derived class needs to implement it.')

    @abstractmethod
    def summarize_info(self):
        raise NotImplementedError('The derived class needs to implement it.')
