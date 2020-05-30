#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================


from collections import defaultdict

from xai.data.exceptions import ItemDataTypeNotSupported
from xai.data.explorer.abstract_analyzer import AbstractDataAnalyzer
from xai.data.explorer.categorical.categorical_stats import CategoricalStats


class CategoricalDataAnalyzer(AbstractDataAnalyzer):
    """
    This analyzer class analyzes categorical data and accumulates frequency count for all values fed into it
    """

    SUPPORTED_TYPES = [str, int]

    def __init__(self):
        super(CategoricalDataAnalyzer, self).__init__()
        self._frequency_count = defaultdict(int)

    def feed(self, value: int or str):
        """
        Accumulate count for value

        Args:
           value: value that fed for frequency count update

        """
        if type(value) not in CategoricalDataAnalyzer.SUPPORTED_TYPES:
            raise ItemDataTypeNotSupported(type(value), type(self), CategoricalDataAnalyzer.SUPPORTED_TYPES)
        self._frequency_count[value] += 1

    def get_statistics(self) -> CategoricalStats:
        """
        Return stats for the analyzer

        Returns:
            A CategoricalStats object that keeps track of frequency count
        """
        stats = CategoricalStats(frequency_count=self._frequency_count)
        return stats
