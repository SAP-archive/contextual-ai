#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import math
from typing import Optional, List, Tuple

import numpy as np
from sklearn.neighbors import KernelDensity

from xai.data.constants import STATSCONSTANTS
from xai.data.exceptions import ItemDataTypeNotSupported, NoItemsError
from xai.data.explorer.abstract_analyzer import AbstractDataAnalyzer
from xai.data.explorer.numerical.numerical_stats import NumericalStats


class NumericDataAnalyzer(AbstractDataAnalyzer):
    """
    This analyzer class analyzes numerical data and generates key stats for numerical values fed into it
    """
    SUPPORTED_TYPES = [int, float]

    def __init__(self):
        super(NumericDataAnalyzer, self).__init__()
        self._values = []
        self._nan_counter = 0

    def feed(self, value: int or str):
        """
        Feed the value into analyzer

        Args:
           value: value that fed for frequency count update

        """
        if type(value) not in NumericDataAnalyzer.SUPPORTED_TYPES:
            raise ItemDataTypeNotSupported(type(value), type(self),
                                           NumericDataAnalyzer.SUPPORTED_TYPES)
        if np.isnan(value) or value is None or math.isnan(value):
            self._nan_counter += 1
            return
        self._values.append(value)

    def get_statistics(self, bin_edges: Optional[List[float]] = None,
                       extreme_value_percentile: Optional[Tuple[float, float]] = [5, 95],
                       num_of_bins: Optional[int] = STATSCONSTANTS.DEFAULT_BIN_SIZE) -> NumericalStats:
        """
        Return stats for the analyzer

        Returns:
            A NumericalStats object that stores key stats for numerical data
        """

        if not self._values or len(self._values) == 0:
            raise NoItemsError(type(self))

        total_count = len(self._values)

        np_values = np.array(self._values)

        min = float(np.min(np_values))
        max = float(np.max(np_values))
        mean = float(np.mean(np_values))
        median = float(np.median(np_values))
        sd = float(np.std(np_values))
        histogram = list()

        # update histogram
        if bin_edges is None:
            left_x_percentile = np.percentile(np_values, extreme_value_percentile[0])
            right_x_percentile = np.percentile(np_values, extreme_value_percentile[1])

            bin_edges = list()
            bin_edges.append(min)
            bin_size = (right_x_percentile - left_x_percentile) / num_of_bins
            for bin_idx in range(num_of_bins):
                bin_edges.append(left_x_percentile + bin_size * bin_idx)
            bin_edges.append(right_x_percentile)
            bin_edges.append(max)

        count, _ = np.histogram(np_values, bins=bin_edges)
        for bin_idx, bin_count in enumerate(count):
            histogram.append((float(bin_edges[bin_idx]), float(bin_edges[bin_idx + 1]), int(bin_count)))

        # update kde curve
        kde_skl = KernelDensity(bandwidth=STATSCONSTANTS.KDE_BAND_WIDTH)
        kde_skl.fit(np_values[:, np.newaxis])
        x_grid = np.linspace(min, max, STATSCONSTANTS.KDE_XGRID_RESOLUTION)
        log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
        kde = list(zip(list(x_grid), list(np.exp(log_pdf))))

        stats = NumericalStats(total_count=total_count,
                               min=min,
                               max=max,
                               mean=mean,
                               median=median,
                               sd=sd,
                               histogram=histogram,
                               kde=kde,
                               nan_count=self._nan_counter)
        return stats
