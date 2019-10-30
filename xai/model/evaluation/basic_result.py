#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from abc import ABC, abstractmethod
from typing import Tuple, List

from ordered_set import OrderedSet


################################################################################
### Classification Result
################################################################################
class ClassificationResult(ABC):
    """
    The base class for classification problem result.
    """

    def __init__(self):
        self.resultdict = dict()
        self.metric_set = OrderedSet()
        self.label_set = OrderedSet()
        self.confusion_matrices = dict()

    def update_result(self, metric: str, label: str, value: float):
        """
        update the result based on metric name and class label (for each class)
        Args:
            metric (str): metric name, e.g. `accuracy`, `recall`
            label (str): class label name
            value (float): metric value

        Returns:

        """
        if metric not in self.resultdict.keys():
            self.resultdict[metric] = dict()
            self.metric_set.add(metric)
        self.resultdict[metric][label] = value
        self.label_set.add(label)

    @abstractmethod
    def load_results_from_meta(self, evaluation_result: dict, labels: List[str] = None):
        raise NotImplementedError('The derived class should implement it.')

    @abstractmethod
    def convert_metrics_to_table(self) -> List[Tuple[str, List[str], List[List[float]]]]:
        """
        converts the metrics saved in the object to a table that is ready to render in the report.
        Returns: a set of tables (title, header, values)
        """
        raise NotImplementedError('The derived class should implement it.')

    def get_metric_list(self):
        """
        returns all the metric names
        Returns: a list of metric names

        """
        return list(self.metric_set)

    def get_label_list(self):
        """
        returns all the class names
        Returns: a list of class label names

        """
        return list(self.label_set)
