from typing import Dict, List, Tuple

import numpy as np
from sklearn.neighbors import KernelDensity

from xai.data.constants import STATSKEY, STATSCONSTANTS
from xai.data.exceptions import NoItemsError
from xai.data.explorer.abstract_stats import AbstractStats


class NumericalStats(AbstractStats):
    """
    NumericalStats contains following basic information:
        - _total_count: total count of values
        - min: minimum of all values
        - max: maximum of all values
        - mean: mean of the values
        - median: median of the values
        - sd: standard deviation of the values
        - _histogram: a histogram of value distribution represented by a list of (x_left, x_right, count).
        - _kde: a kernel density estimation curve represented by a list of points
    """

    def __init__(self):
        self._total_count = 0
        self.min = None
        self.max = None
        self.mean = None
        self.median = None
        self.sd = None
        self._histogram = []
        self._kde = []

    def update_stats_from_values(self, values: List[float]):
        """
        update the key stats based on values
        Args:
            values: the list of all numerical values
        """
        if not values or len(values) == 0:
            raise NoItemsError(type(self))

        self._total_count = len(values)

        np_values = np.array(values)

        self.min = float(np.min(np_values))
        self.max = float(np.max(np_values))
        self.mean = float(np.mean(np_values))
        self.median = float(np.median(np_values))
        self.sd = float(np.std(np_values))

        # update histogram
        x_percentile_05 = np.percentile(np_values, 5)
        x_percentile_95 = np.percentile(np_values, 95)

        bin_edges = list()
        bin_edges.append(self.min)
        bin_size = (x_percentile_95 - x_percentile_05) / STATSCONSTANTS.DEFAULT_BIN_SIZE
        for bin_idx in range(STATSCONSTANTS.DEFAULT_BIN_SIZE):
            bin_edges.append(x_percentile_05 + bin_size * bin_idx)
        bin_edges.append(x_percentile_95)
        bin_edges.append(self.max)

        count, _ = np.histogram(np_values, bins=bin_edges)
        for bin_idx, bin_count in enumerate(count):
            self._histogram.append((bin_edges[bin_idx], bin_edges[bin_idx + 1], bin_count))

        # update kde curve
        kde_skl = KernelDensity(bandwidth=STATSCONSTANTS.KDE_BAND_WIDTH)
        kde_skl.fit(np_values[:, np.newaxis])
        x_grid = np.linspace(self.min, self.max, STATSCONSTANTS.KDE_XGRID_RESOLUTION)
        log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
        self._kde = list(zip(list(x_grid), list(np.exp(log_pdf))))

    def get_total_count(self) -> int:
        """
        return the total count of values for the stats object

        Returns:
            total count of values
        """
        return self._total_count

    def get_histogram(self) -> List[Tuple[float, float, int]]:
        """
        return a list of tuple to present histogram of the values

        Returns:
            a list of tuple, each tuple has 3 elements (bin_left_x, bin_right_x, count_within_the_bin)
        """
        return self._histogram

    def get_kde(self) -> List[Tuple[float, float]]:
        """
        return a list of points to present kernel density estimation curve

        Returns:
            a list of point, each point is represented by X,Y
        """
        return self._kde

    def to_json(self) -> Dict:
        """
        map stats information into a json object

        Returns:
            a json that represent frequency count and total count
        """

        json_obj = dict()
        json_obj[STATSKEY.TOTAL_COUNT] = self._total_count
        json_obj[STATSKEY.MAX] = self.max
        json_obj[STATSKEY.MIN] = self.min
        json_obj[STATSKEY.MEAN] = self.mean
        json_obj[STATSKEY.MEDIAN] = self.median
        json_obj[STATSKEY.STDDEV] = self.sd

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
