import numpy
import operator
from typing import List
from xai.model_interpreter.exceptions import UnsupportedMethodType, InconsistentSize, TrainingDataNotProvided
from xai.data.explorer.data_analyzer_suite import DataAnalyzerSuite
import shap


class FeatureInterpreter:
    SUPPORTED_TYPES = ['shap']

    def __init__(self, feature_names: List[str]):
        self._feature_names = feature_names

    def get_feature_distribution(self, feature_types: List[str], train_x: numpy.ndarray, labels: List = None):
        if len(feature_types) != len(self._feature_names):
            raise InconsistentSize('feature_types', 'feature_names', len(feature_types),
                                   len(self._feature_names))

        data_analyzer_suite = DataAnalyzerSuite(data_type_list=feature_types, column_names=self._feature_names)
        if train_x.shape[1] != len(feature_types):
            raise InconsistentSize('train_x.shape[1]', 'feature_types', train_x.shape[1],
                                   len(feature_types))

        for col_idx, column in enumerate(self._feature_names):
            data_analyzer_suite.feed_column(column_name=column,
                                            column_data=numpy.transpose(train_x[:, col_idx]).tolist(),
                                            labels=labels)
        return data_analyzer_suite.get_statistics()

    def get_feature_importance_ranking(self, trained_model, train_x: numpy.ndarray = None, method='default'):
        if method == 'default':
            scores = trained_model.feature_importances_
            if len(scores) != len(self._feature_names):
                raise InconsistentSize('scores', 'feature_names', len(scores),
                                       len(self._feature_names))
            else:
                feature_importance = dict(self._feature_names, scores)
                feature_importance = sorted(feature_importance.values(), key=operator.itemgetter(1), reverse=True)
                return feature_importance

        else:
            if method not in FeatureInterpreter.SUPPORTED_TYPES:
                raise UnsupportedMethodType(method)
            if train_x is None:
                raise TrainingDataNotProvided

            if method == 'shap':
                self._get_ranking_by_shap(trained_model, train_x)

    def _get_ranking_by_shap(self, trained_model, train_x):
        explainer = shap.TreeExplainer(trained_model)
        shap_values = explainer.shap_values(train_x)
        pass
