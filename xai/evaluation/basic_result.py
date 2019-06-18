from abc import ABC, abstractmethod
from typing import Tuple, List
from collections import defaultdict
from ordered_set import OrderedSet

from xai.evaluation.confusion_matrix import ConfusionMatrix


class ClassificationResult(ABC):
    def __init__(self):
        self.resultdict = dict()
        self.metric_set = OrderedSet()
        self.split_set = OrderedSet()
        self.label_set = OrderedSet()
        self.confusion_matrices = dict()

    def update_result(self, split: str, metric: str, label: str, value: float):
        '''
        format: [- split: - metric:  - label: - value:]
        '''
        if split not in self.resultdict.keys():
            self.resultdict[split] = dict()
            self.split_set.add(split)
        if metric not in self.resultdict[split].keys():
            self.resultdict[split][metric] = dict()
            self.metric_set.add(metric)
        self.resultdict[split][metric][label] = value
        self.label_set.add(label)

    @abstractmethod
    def load_results_from_meta(self, metadata: dict, labels: List[str] = None):
        raise NotImplementedError('The derived class should implement it.')

    @abstractmethod
    def convert_metrics_to_table(self) -> List[Tuple[str, List[str], List[List[float]]]]:
        '''

        :return: a set of tables (title, header, values)
        '''
        raise NotImplementedError('The derived class should implement it.')

    def get_split_list(self):
        return list(self.split_set)

    def get_metric_list(self):
        return list(self.metric_set)

    def get_label_list(self):
        return list(self.label_set)
