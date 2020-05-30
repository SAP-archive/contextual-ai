#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import Tuple, Dict, Union, Optional

from xai.data.explorer.abstract_labelled_analyzer import AbstractLabelledDataAnalyzer
from xai.data.explorer.numerical.numerical_analyzer import NumericDataAnalyzer
from xai.data.explorer.numerical.numerical_stats import NumericalStats


class LabelledNumericalDataAnalyzer(AbstractLabelledDataAnalyzer):
    def __init__(self):
        super().__init__(data_analyzer_cls=NumericDataAnalyzer)

    def get_statistics(self, extreme_value_percentile: Optional[Tuple[int, int]] = [0, 100],
                       num_of_bins: Optional[int] = 20) -> Tuple[Dict[Union[str, int], NumericalStats], NumericalStats]:
        """
        Get stats based on labels

        Returns:
            A dictionary maps label to the aggregated stats obj
        """
        _stats = dict()
        _all_stats = self._all_analyzer.get_statistics(extreme_value_percentile=extreme_value_percentile,
                                                       num_of_bins=num_of_bins)
        bin_edges = [bin[0] for bin in _all_stats.histogram]
        bin_edges.append(_all_stats.histogram[-1][1])

        for label, analyzer in self._label_analyzer.items():
            _stats[label] = analyzer.get_statistics(bin_edges=bin_edges)

        return _stats, _all_stats
