from plugin.xai.data_explorer.numeric_analyzer import NumericAnalyzer
from collections import defaultdict
from plugin.xai import constants


class SequenceLengthAnalyzer(NumericAnalyzer):
    def __init__(self, feature_list):
        super(SequenceLengthAnalyzer, self).__init__(feature_list=feature_list)
        self.summary_info = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    def analyze_sample(self, sample, label_value):
        for feature_key in self.feature_list:
            if feature_key in sample:
                feature_value = sample[feature_key]
                if type(feature_value) == list:
                    length = len(feature_value)
                    self.summary_info["%s_length" % feature_key][label_value][length] += 1
                else:
                    raise Exception('Error in analyze length: The feature %s is not a sequence feature.' % feature_key)

    def aggregate(self):
        for fea in self.summary_info.keys():
            if 'all' not in self.summary_info[fea]:
                overall_dist = defaultdict(int)
                for individual_dist in self.summary_info[fea].values():
                    for k, v in individual_dist.items():
                        overall_dist[k] += v
                self.summary_info[fea]['all'] = overall_dist
            for label in self.summary_info[fea].keys():
                self.summary_info[fea][label] = self._get_numeric_curve_from_data(dict(self.summary_info[fea][label]), fea,
                                                                                  label)

    def summarize_info(self):
        return {constants.KEY_LENGTH_FEATURE_DISTRIBUTION: self.summary_info}
