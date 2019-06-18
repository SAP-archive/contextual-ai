from xai.data_explorer.abstract_analyzer import AbstractAnalyzer
from xai import constants
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class NumericAnalyzer(AbstractAnalyzer):

    def __init__(self, feature_list):
        super(NumericAnalyzer, self).__init__(feature_list=feature_list)
        self.summary_info = defaultdict(lambda: defaultdict(list))

    def analyze_sample(self, sample, label_value):
        for feature_key in self.feature_list:
            if feature_key in sample:
                feature_value = sample[feature_key]
                if type(feature_value) == list:
                    for feature_list_value in feature_value:
                        self.summary_info[feature_key][label_value].append(feature_list_value)
                else:
                    self.summary_info[feature_key][label_value].append(feature_value)

    def aggregate(self):
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

    def summarize_info(self):
        return {constants.KEY_NUMERIC_FEATURE_DISTRIBUTION: self.summary_info}

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
        numeric_dist['perc_10'] = float(np.percentile(raw_data, 10))
        numeric_dist['perc_90'] = float(np.percentile(raw_data, 90))

        return numeric_dist
