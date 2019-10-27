#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import Tuple, Dict, Union

from xai.data.explorer.abstract_labelled_analyzer import AbstractLabelledDataAnalyzer
from xai.data.explorer.categorical.categorical_analyzer import CategoricalDataAnalyzer
from xai.data.explorer.categorical.categorical_stats import CategoricalStats


class LabelledCategoricalDataAnalyzer(AbstractLabelledDataAnalyzer):
    def __init__(self):
        super().__init__(data_analyzer_cls=CategoricalDataAnalyzer)

    def get_statistics(self) -> Tuple[Dict[Union[str, int], CategoricalStats], CategoricalStats]:
        """
        Get stats based on labels

        Returns:
            A dictionary maps label to the aggregated stats obj
        """
        _stats = dict()
        _all_stats = self._all_analyzer.get_statistics()
        _all_stats_keys = list(_all_stats.frequency_count.keys())
        for label, analyzer in self._label_analyzer.items():
            class_frequency = analyzer.get_statistics().frequency_count
            _stats[label] = dict()
            for key in _all_stats_keys:
                _stats[label][key] = class_frequency[key] if key in class_frequency else 0

            _stats[label] = CategoricalStats(_stats[label])
        return _stats, _all_stats
