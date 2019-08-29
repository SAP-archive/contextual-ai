from collections import defaultdict
from typing import Iterator, List

from xai.data_explorer.abstract_analyzer import AbstractDataAnalyzer
from xai.data_explorer.numerical.categorical_stats import CategoricalStats
from xai.data_explorer.config import DICT_ANALYZER_TO_SUPPORTED_ITEM_DATA_TYPE
from xai.data_explorer.data_exceptions import ItemDataTypeNotSupported
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class NumericDataAnalyzer(AbstractDataAnalyzer):

    def __init__(self, feature_list):
        super(NumericDataAnalyzer, self).__init__(feature_list=feature_list)
        self.summary_info = defaultdict(lambda: defaultdict(list))

    def feed(self, value):
        """
        add numerical value into temp buffer for further statistical analysis
        Args:
           value: numerical value

        """
        for feature_key in self.feature_list:
            if feature_key in sample:
                feature_value = sample[feature_key]
                if type(feature_value) == list:
                    for feature_list_value in feature_value:
                        self.summary_info[feature_key][label_value].append(feature_list_value)
                else:
                    self.summary_info[feature_key][label_value].append(feature_value)

    def feed_all(self):
        for fea in self.summary_info.keys():
            if 'all' not in self.summary_info.keys():
                overall_list = []
                for individual_list in self.summary_info[fea].values():
                    if overall_list is None:
                        overall_list = []
                    overall_list.extend(individual_list)

            self.summary_info[fea]['all'] = overall_list

            for label_name in self.summary_info[fea].keys():
                class_values = self.summary_info[fea][label_name]
                numeric_dist = self._get_numeric_curve_from_data(class_values, fea, label_name)
                self.summary_info[fea][label_name] = numeric_dist

    def get_statistics(self) -> CategoricalStats:
        """
        return stats for the analyzer
        Returns:
            a NumericalStats object that stores key stats for numerical data
        """
        self.stats = CategoricalStats()
        for value, count in self._frequency_count.items():
            self.stats.update_count_by_value(value, count)
        return self.stats

    def _get_numeric_curve_from_data(self, data, feature, label_name):
        if type(data) == list:
            raw_data = np.array(data)
        if type(data) == dict:
            raw_data = []
            for k, v in data.items():
                raw_data.extend([k] * v)
        f = plt.figure()
        try:
            ax = sns.distplot(raw_data, kde=True)
            # get kde line data
            kde_line_data = ax.get_lines()[0].get_xydata()
            kde_line_data = kde_line_data.tolist()
            # get histogram data
            xywh = [(p.get_x(), p.get_y(), p.get_width(), p.get_height()) for p in ax.patches]
        except:
            print(
                "Error generated in plotting distribution for %s for label (%s). Total number of values: %s " % (
                    feature, label_name, len(data)))
            kde_line_data = []
            xywh = []
        finally:
            plt.close(fig=f)

        numeric_dist = dict()
        numeric_dist['kde'] = kde_line_data
        numeric_dist['histogram'] = xywh
        numeric_dist['total_num'] = len(raw_data)
        numeric_dist['max'] = float(np.max(raw_data))
        numeric_dist['min'] = float(np.min(raw_data))
        numeric_dist['mean'] = float(np.mean(raw_data))
        numeric_dist['median'] = float(np.median(raw_data))
        numeric_dist['x_limit'] = [np.percentile(raw_data, 5),np.percentile(raw_data, 95)]
        numeric_dist['perc_10'] = float(np.percentile(raw_data, 10))
        numeric_dist['perc_90'] = float(np.percentile(raw_data, 90))

        return numeric_dist
