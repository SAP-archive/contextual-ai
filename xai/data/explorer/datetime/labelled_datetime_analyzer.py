#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import Tuple, Dict, Union, Optional, List

from xai.data.explorer.abstract_labelled_analyzer import AbstractLabelledDataAnalyzer
from xai.data.explorer.datetime.datetime_analyzer import DatetimeDataAnalyzer
from xai.data.explorer.datetime.datetime_stats import DatetimeStats


class LabelledDatetimeDataAnalyzer(AbstractLabelledDataAnalyzer):
    def __init__(self):
        super().__init__(data_analyzer_cls=DatetimeDataAnalyzer)

    def get_statistics(self, resolution_list: Optional[List[str]] = None) -> Tuple[
        Dict[Union[str, int], DatetimeStats], DatetimeStats]:
        """
        Get stats based on labels

        Returns:
            A dictionary maps label to the aggregated stats obj
        """
        _stats = dict()
        _all_stats = self._all_analyzer.get_statistics(resolution_list=resolution_list)
        for label, analyzer in self._label_analyzer.items():
            _stats[label] = analyzer.get_statistics(resolution_list=resolution_list)
        return _stats, _all_stats
