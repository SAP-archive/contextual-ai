from xai.data_explorer.abstract_analyzer import AbstractAnalyzer
from xai.data_explorer.categorical_analyzer import CategoricalAnalyzer
from xai.data_explorer.numeric_analyzer import NumericAnalyzer
from xai import constants


class LabelAnalyzer(AbstractAnalyzer):
    def __init__(self, label, label_type):
        self.label_key = label
        label_type = label_type
        if label_type == constants.KEY_FEATURE_CATEGORICAL_TYPE:
            self.analyzer = CategoricalAnalyzer(feature_list=[self.label_key])
        elif label_type == constants.KEY_FEATURE_NUMERIC_TYPE:
            self.analyzer = NumericAnalyzer(feature_list=[self.label_key])

    def analyze_sample(self, sample, label_value):
        self.analyzer.analyze_sample(sample, label_value)

    def aggregate(self):
        self.analyzer.aggregate()

    def summarize_info(self):
        return {constants.KEY_DATA_DISTRIBUTION: self.analyzer.summary_info[self.label_key]['all']}
