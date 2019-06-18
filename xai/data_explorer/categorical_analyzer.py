from xai.data_explorer.abstract_analyzer import AbstractAnalyzer
from collections import defaultdict
from xai import constants

class CategoricalAnalyzer(AbstractAnalyzer):

    def __init__(self, feature_list):
        super(CategoricalAnalyzer,self).__init__(feature_list=feature_list)
        self.summary_info = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    def analyze_sample(self, sample, label_value):
        for feature_key in self.feature_list:
            if feature_key in sample:
                feature_value = sample[feature_key]
                if type(feature_value) == list:
                    for feature_list_value in feature_value:
                        self.summary_info[feature_key][label_value][feature_list_value] += 1
                else:
                    self.summary_info[feature_key][label_value][feature_value] += 1

    def aggregate(self):
        for fea in self.summary_info.keys():
            if 'all' not in self.summary_info[fea]:
                overall_dist = defaultdict(int)
                for individual_dist in self.summary_info[fea].values():
                    for k, v in individual_dist.items():
                        overall_dist[k] += v
                self.summary_info[fea]['all'] = overall_dist

    def summarize_info(self):
        return {constants.KEY_CATEGORICAL_FEATURE_DISTRIBUTION:self.summary_info}
