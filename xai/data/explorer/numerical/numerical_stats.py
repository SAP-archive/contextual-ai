#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import Dict, List, Tuple, Optional, Union

from xai.data.abstract_stats import AbstractStats
from xai.data.constants import STATSKEY
from xai.data.exceptions import InvalidTypeError, InvalidSizeError


class NumericalStats(AbstractStats):
    """
    NumericalStats contains following basic information:
        - _total_count: total count of values
        - _nan_count: total count of nan values
        - _min: minimum of all values
        - _max: maximum of all values
        - _mean: mean of the values
        - _median: median of the values
        - _sd: standard deviation of the values
        - _histogram: a histogram of value distribution represented by a list of (x_left, x_right, count)
        - _kde: a kernel density estimation curve represented by a list of points
    """

    def __init__(self,
                 min: Optional[Union[float, int, None]] = None,
                 max: Optional[Union[float, int, None]] = None,
                 mean: Optional[float] = None,
                 median: Optional[Union[float, int, None]] = None,
                 sd: Optional[Union[float, int, None]] = None,
                 histogram: Optional[List[Tuple[Union[float, int, None], Union[float, int, None], int]]] = [],
                 kde: Optional[List[Tuple[Union[float, int, None], Union[float, int, None]]]] = [],
                 total_count: Optional[Union[float, int, None]] = 0,
                 nan_count: Optional[Union[float, int, None]] = 0):
        super(NumericalStats).__init__()
        self.total_count = total_count
        self.min = min
        self.max = max
        self.mean = mean
        self.median = median
        self.sd = sd
        self.histogram = histogram
        self.kde = kde
        self.nan_count = nan_count

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value: Union[float, int, None]):
        if not isinstance(value, float) and not isinstance(value, int) and value is not None:
            raise InvalidTypeError('min', type(value), '<int> or <float> or None')
        self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value: Union[float, int, None]):
        if not isinstance(value, float) and not isinstance(value, int) and value is not None:
            raise InvalidTypeError('max', type(value), '<int> or <float> or None')
        self._max = value

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, value: Union[float, int, None]):
        if not isinstance(value, float) and not isinstance(value, int) and value is not None:
            raise InvalidTypeError('mean', type(value), '<int> or <float> or None')
        self._mean = value

    @property
    def median(self):
        return self._median

    @median.setter
    def median(self, value: Union[float, int, None]):
        if not isinstance(value, float) and not isinstance(value, int) and value is not None:
            raise InvalidTypeError('median', type(value), '<int> or <float> or None')
        self._median = value

    @property
    def sd(self):
        return self._sd

    @sd.setter
    def sd(self, value: Union[float, int, None]):
        if not isinstance(value, float) and not isinstance(value, int) and value is not None:
            raise InvalidTypeError('sd', type(value), '<int> or <float> or None')
        self._sd = value

    @property
    def nan_count(self):
        return self._nan_count

    @nan_count.setter
    def nan_count(self, value: int):
        if not isinstance(value, int):
            raise InvalidTypeError('nan_count', type(value), '<int>')
        self._nan_count = value

    @property
    def histogram(self):
        return self._histogram

    @histogram.setter
    def histogram(self, value: List[Tuple[Union[float, int, None], Union[float, int, None], int]]):
        if not isinstance(value, list):
            raise InvalidTypeError('histogram', type(value), '<list>')

        for item in value:
            if not isinstance(value, list):
                raise InvalidTypeError('histogram: bin', type(item), '<tuple>')
            if len(item) != 3:
                raise InvalidSizeError('histogram: bin', len(item), 3)
            if not isinstance(item[0], float) and not isinstance(item[0], int):
                raise InvalidTypeError('histogram: bin: bin_edge_left', type(item[0]), '<int> or <float>')
            if not isinstance(item[1], float) and not isinstance(item[1], int):
                raise InvalidTypeError('histogram: bin: bin_edge_right', type(item[1]), '<int> or <float>')
            if not isinstance(item[2], int):
                raise InvalidTypeError('histogram: bin: bin_edge_count', type(item[2]), '<int>')

        self._histogram = value
        self.total_count = sum([item[2] for item in self._histogram])

    @property
    def kde(self):
        return self._kde

    @kde.setter
    def kde(self, value: List[Tuple[Union[float, int, None], Union[float, int, None]]]):
        if not isinstance(value, list):
            raise InvalidTypeError('kde', type(value), '<list>')

        for item in value:
            if type(item) != tuple:
                raise InvalidTypeError('kde: point', type(item), '<tuple>')
            if len(item) != 2:
                raise InvalidSizeError('kde: point', len(item), 2)
            if not isinstance(item[0], float) and not isinstance(item[0], int):
                raise InvalidTypeError('kde: point: x', type(item[0]), '<int> or <float>')
            if not isinstance(item[0], float) and not isinstance(item[1], int):
                raise InvalidTypeError('kde: point: y', type(item[1]), '<int> or <float>')

        self._kde = value

    def to_json(self) -> Dict:
        """
        Map stats information into a json object

        Returns:
            A json that represent frequency count and total count
        """

        json_obj = dict()
        json_obj[STATSKEY.TOTAL_COUNT] = self._total_count
        json_obj[STATSKEY.MAX] = self._max
        json_obj[STATSKEY.MIN] = self._min
        json_obj[STATSKEY.MEAN] = self._mean
        json_obj[STATSKEY.MEDIAN] = self._median
        json_obj[STATSKEY.STDDEV] = self._sd
        json_obj[STATSKEY.NAN_COUNT] = self._nan_count

        json_obj[STATSKEY.DISTRIBUTION] = {}

        json_obj[STATSKEY.DISTRIBUTION][STATSKEY.HISTOGRAM] = []
        for bin_left, bin_right, bin_count in self._histogram:
            json_obj[STATSKEY.DISTRIBUTION][STATSKEY.HISTOGRAM].append(
                {STATSKEY.HISTOGRAM_KEY.X_LEFT: bin_left,
                 STATSKEY.HISTOGRAM_KEY.X_RIGHT: bin_right,
                 STATSKEY.HISTOGRAM_KEY.BIN_COUNT: bin_count})

        json_obj[STATSKEY.DISTRIBUTION][STATSKEY.KDE] = []
        for x, y in self._kde:
            json_obj[STATSKEY.DISTRIBUTION][STATSKEY.HISTOGRAM].append(
                {STATSKEY.KDE_KEY.X: x,
                 STATSKEY.KDE_KEY.Y: y})

        return json_obj
