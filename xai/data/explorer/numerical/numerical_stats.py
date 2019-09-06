from typing import Dict, List, Tuple, Optional

from xai.data.abstract_stats import AbstractStats
from xai.data.constants import STATSKEY
from xai.data.exceptions import InvalidTypeError, InvalidSizeError


class NumericalStats(AbstractStats):
    """
    NumericalStats contains following basic information:
        - _total_count: total count of values
        - _min: minimum of all values
        - _max: maximum of all values
        - _mean: mean of the values
        - _median: median of the values
        - _sd: standard deviation of the values
        - _histogram: a histogram of value distribution represented by a list of (x_left, x_right, count)
        - _kde: a kernel density estimation curve represented by a list of points
    """

    def __init__(self,
                 min: Optional[float or int] = None,
                 max: Optional[float or int] = None,
                 mean: Optional[float] = None,
                 median: Optional[float or int] = None,
                 sd: Optional[float or int] = None,
                 histogram: Optional[List[Tuple[float or int, float or int, int]]] = None,
                 kde: Optional[List[Tuple[float or int, float or int]]] = None,
                 total_count: Optional[float or int] = None):
        self.total_count = total_count
        self.min = min
        self.max = max
        self.mean = mean
        self.median = median
        self.sd = sd
        self.histogram = histogram
        self.kde = kde

    @property
    def min(self):
        return self._min

    @min.setter
    def min(self, value: int or float):
        if type(value) not in [float, int]:
            raise InvalidTypeError('min', type(value), '<int> or <float>')
        self._min = value

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, value: int or float):
        if type(value) not in [float, int]:
            raise InvalidTypeError('max', type(value), '<int> or <float>')
        self._max = value

    @property
    def mean(self):
        return self._mean

    @mean.setter
    def mean(self, value: int or float):
        if type(value) not in [float, int]:
            raise InvalidTypeError('mean', type(value), '<int> or <float>')
        self._mean = value

    @property
    def median(self):
        return self._median

    @median.setter
    def median(self, value: int or float):
        if type(value) not in [float, int]:
            raise InvalidTypeError('median', type(value), '<int> or <float>')
        self._median = value

    @property
    def sd(self):
        return self._sd

    @sd.setter
    def sd(self, value: int or float):
        if type(value) not in [float, int]:
            raise InvalidTypeError('sd', type(value), '<int> or <float>')
        self._sd = value

    @property
    def total_count(self):
        return self._total_count

    @total_count.setter
    def total_count(self, value: int):
        if type(value) == int:
            raise InvalidTypeError('total_count', type(value), '<int>')
        self._total_count = value

    @property
    def histogram(self):
        return self._histogram

    @histogram.setter
    def histogram(self, value: List[Tuple[float or int, float or int, int]]):
        if type(value) != list:
            raise InvalidTypeError('histogram', type(value), '<list>')

        for item in value:
            if type(item) != tuple:
                raise InvalidTypeError('histogram: bin', type(item), '<tuple>')
            if len(item) != 3:
                raise InvalidSizeError('histogram: bin', len(item), 3)
            if type(item[0]) not in [float, int]:
                raise InvalidTypeError('histogram: bin: bin_edge_left', type(item[0]), '<int> or <float>')
            if type(item[1]) not in [float, int]:
                raise InvalidTypeError('histogram: bin: bin_edge_right', type(item[1]), '<int> or <float>')
            if type(item[2]) != int:
                raise InvalidTypeError('histogram: bin: bin_edge_count', type(item[2]), '<int>')

        self._histogram = value
        self._total_count = sum([item[2] for item in self._histogram])

    @property
    def kde(self):
        return self._kde

    @kde.setter
    def kde(self, value: List[Tuple[float or int, float or int]]):
        if type(value) != list:
            raise InvalidTypeError('kde', type(value), '<list>')

        for item in value:
            if type(item) != tuple:
                raise InvalidTypeError('kde: point', type(item), '<tuple>')
            if len(item) != 2:
                raise InvalidSizeError('kde: point', len(item), 2)
            if type(item[0]) not in [float, int]:
                raise InvalidTypeError('kde: point: x', type(item[0]), '<int> or <float>')
            if type(item[1]) not in [float, int]:
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

        json_obj[STATSKEY.DISTRIBUTION] = []

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
