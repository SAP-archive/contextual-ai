#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from abc import ABC, abstractmethod

from typing import List, Dict, Union, Tuple

from xai.data.abstract_stats import AbstractStats
from xai.data.exceptions import InconsistentSize


class AbstractLabelledDataAnalyzer(ABC):

    def __init__(self, data_analyzer_cls):
        self._label_analyzer = dict()
        self._analyzer_cls = data_analyzer_cls
        self._all_analyzer = data_analyzer_cls()

    def feed(self, value: Union[str, int], label: Union[str, int]):
        """
        Update the analyzer with value and its corresponding label

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
        Update the analyzer with a list of values and their corresponding labels

        Args:
            values: categorical values
            labels: corresponding labels for each categorical value
        """
        if len(values) != len(labels):
            raise InconsistentSize('values', 'labels', len(values), len(labels))

        value_label = zip(values, labels)
        for value, label in value_label:
            self.feed(value, label)

    @abstractmethod
    def get_statistics(self) -> Tuple[Dict[Union[str, int], AbstractStats], AbstractStats]:
        """
        Get stats based on labels

        Returns:
            A dictionary maps label to the aggregated stats json object
        """
        raise NotImplementedError('The derived class should implement this class')
