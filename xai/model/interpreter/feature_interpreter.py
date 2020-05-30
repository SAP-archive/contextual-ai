#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import operator
import warnings

import numpy
import pandas as pd
from scipy import stats
from typing import List, Dict, Tuple

import shap
from xai import ALG, MODE
from xai.data.constants import DATATYPE
from xai.data.explorer.data_analyzer_suite import DataAnalyzerSuite
from xai.model.interpreter.exceptions import (
    InconsistentSize,
    TrainingDataNotProvided
)
from xai.model.interpreter.exceptions import UnsupportedMethodType


################################################################################
### Feature Interpreter
################################################################################
class FeatureInterpreter:
    """
    Class Feature Interpreter.

    The class is used to generate the following information:
        - feature distribution
        - feature correlation
        - feature importance ranking for a trained model

    """
    SUPPORTED_FEATURE_IMPORTANCE_TYPES = [ALG.SHAP]

    def __init__(self, feature_names: List[str]):
        """
        Initialize feature interpreter with feature names

        Args:
            feature_names: list, the list of feature names
        """
        self._feature_names = feature_names

    def get_feature_distribution(self, feature_types: List[str], train_x: numpy.ndarray, labels: List = None) -> Dict:
        """
        Get feature distribution analysis based on feature types

        Args:
            feature_types: list, a list of pre-defined data type for feature
            train_x: numpy.ndarray, training data of which each row is a training sample.
                     A training data set with M samples of each of which has N features should have a shape (M,N).
            labels: list,

        Returns:
            A dictionary maps each feature name to the stats object based on its data type.
            For stats class implement, details can be found in `xai.data.explorer`.

        """
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

    def get_feature_correlation(self, feature_types: List[str],
                                train_x: numpy.ndarray,
                                categorical_corr_type='lambda',
                                numerical_corr_type='pearson',
                                text_corr_type='tf',
                                categorical_vs_numerical_corr_type='anova') -> (pd.DataFrame, pd.DataFrame):
        """
        Get feature correlation

        Args:
            feature_types: list, the pre-defined data type for each feature
            train_x: numpy.ndarray, training data
            categorical_corr_type: str, pre-defined correlation type for correlation among categorical features.
            numerical_corr_type: str, pre-defined correlation type for correlation among numerical features.
            text_corr_type: str, pre-defined correlation type for correlation among text features.
            categorical_vs_numerical_corr_type: str, pre-defined correlation type for correlation between categorical
                                                features and numerical features.

        Returns:
            Dataframe of correlation type mask,
            Dataframe of correlation values

        """
        if len(feature_types) != len(self._feature_names):
            raise InconsistentSize('feature_types', 'feature_names', len(feature_types),
                                   len(self._feature_names))

        if train_x.shape[1] != len(self._feature_names):
            raise InconsistentSize('train_x.shape[1]', 'feature_types', train_x.shape[1],
                                   len(self._feature_names))

        df = pd.DataFrame(data=train_x, columns=self._feature_names)

        feature_name_to_type = {key: value for key, value in list(zip(self._feature_names, feature_types))}
        categorical_feature = [name for name, type in feature_name_to_type.items() if type == DATATYPE.CATEGORY]
        numeric_feature = [name for name, type in feature_name_to_type.items() if type == DATATYPE.NUMBER]
        text_feature = [name for name, type in feature_name_to_type.items() if type == DATATYPE.FREETEXT]

        overall_corr = dict()

        corr = self._get_categorical_correlation(df, categorical_feature, correlation_type=categorical_corr_type)
        overall_corr.update(corr)

        corr = self._get_numerical_correlation(df, numeric_feature, correlation_type=numerical_corr_type)
        overall_corr.update(corr)

        corr = self._get_text_correlation(df, text_feature, correlation_type=text_corr_type)
        overall_corr.update(corr)

        corr = self._get_categorical_vs_numerical_correlation(df, categorical_feature, numeric_feature,
                                                              correlation_type=categorical_vs_numerical_corr_type)
        overall_corr.update(corr)

        correlation_values = pd.DataFrame(numpy.zeros((len(feature_types), len(feature_types))),
                                          columns=self._feature_names,
                                          index=self._feature_names)
        correlation_types = pd.DataFrame(numpy.zeros((len(feature_types), len(feature_types))),
                                         columns=self._feature_names,
                                         index=self._feature_names)
        for (col1, col2), (method, value) in overall_corr.items():
            correlation_values[col1][col2] = value
            correlation_types[col1][col2] = method

        return correlation_types, correlation_values

    def _get_categorical_correlation(self, df, categorical_cols, correlation_type) -> Dict[
        Tuple[str, str], Tuple[str, float]]:
        """
        Internal function to calculate correlation among categorical features

        Args:
            df: Dataframe
            categorical_cols: list, list of categorical columns
            correlation_type: str, pre-defined correlation type

        Returns:
            A dictionary maps two column names to correlation type and value

        """
        corr = dict()
        return corr

    def _get_numerical_correlation(self, df, numerical_cols, correlation_type) -> Dict[
        Tuple[str, str], Tuple[str, float]]:
        """
        Internal function to calculate correlation among numerical features

        Args:
            df: Dataframe
            numerical_cols: list, list of numerical columns
            correlation_type: str, pre-defined correlation type

        Returns:
            A dictionary maps two column names to correlation type and value

        """
        if correlation_type not in ['pearson', 'kendall', 'spearman']:
            raise UnsupportedMethodType(correlation_type)
        corr = df[numerical_cols].corr(method=correlation_type)
        correlations = dict()
        for col_a in numerical_cols:
            for col_b in numerical_cols:
                correlations[(col_a, col_b)] = (correlation_type, corr[col_a][col_b])
        return correlations

    def _get_text_correlation(self, df, text_cols, correlation_type) -> Dict[Tuple[str, str], Tuple[str, float]]:
        """
        Internal function to calculate correlation among text features

        Args:
            df: Dataframe
            text_cols: list, list of text columns
            correlation_type: str, pre-defined correlation type

        Returns:
            A dictionary maps two column names to correlation type and value

        """
        corr = dict()
        return corr

    def _get_categorical_vs_numerical_correlation(self, df, categorical_cols, numerical_cols, correlation_type) -> Dict[
        Tuple[str, str], Tuple[str, float]]:
        """
        Internal function to calculate correlation between categorical feature and numerical feature

        Args:
            df: Dataframe
            categorical_cols: list, list of categorical columns
            numerical_cols: list of numerical columns
            correlation_type:

        Returns:
            A dictionary maps two column names to correlation type and value

        """

        def cat_vs_num(df, cat_col_name, num_col_name):
            if correlation_type == 'anova':
                group_series = []
                enums = df[cat_col_name].unique()
                for enum in enums:
                    group_series.append(df[df[cat_col_name] == enum][num_col_name])
                f_score, _ = stats.f_oneway(*group_series)
            return f_score

        correlations = dict()

        for categorical_col in categorical_cols:
            for numerical_col in numerical_cols:
                correlations[(categorical_col, numerical_col)] = (correlation_type,
                                                                  cat_vs_num(df, categorical_col, numerical_col,
                                                                             correlation_type))
                correlations[(numerical_col, categorical_col)] = correlations[(categorical_col, numerical_col)]
        return correlations

    def get_feature_importance_ranking(self, trained_model, train_x: numpy.ndarray = None, method='default',
                                       mode: str = MODE.CLASSIFICATION) -> List[
        Tuple[str, float]]:
        """
        Get feature importance ranking

        Args:
            trained_model: model obj, the trained model object
            train_x: numpy.dnarray, training data
            method: str, pre-defined method for feature importance

        Returns:
            A list of tuple (feature name, feature importance score) in descending order

        """
        if method == 'default':
            scores = trained_model.feature_importances_
            if len(scores) != len(self._feature_names):
                raise InconsistentSize('scores', 'feature_names', len(scores),
                                       len(self._feature_names))
            else:
                feature_importance = {key: value for key, value in list(zip(self._feature_names, scores))}
                feature_importance = sorted(feature_importance.items(), key=operator.itemgetter(1), reverse=True)
                return feature_importance

        else:
            if method not in FeatureInterpreter.SUPPORTED_FEATURE_IMPORTANCE_TYPES:
                raise UnsupportedMethodType(method)
            if train_x is None:
                raise TrainingDataNotProvided

            if method == ALG.SHAP:
                return self._get_ranking_by_shap(trained_model, train_x, mode)

    def get_feature_shap_values(self, trained_model, train_x: numpy.ndarray, mode: str = MODE.CLASSIFICATION) -> List[
        Tuple[str, List[float]]]:
        """
        Get shap values for all samples group by features

        Args:
            trained_model: model obj, the trained model object
            train_x: numpy.dnarray, training data
            mode: str, regression or classification (default)

        Returns:
            A list of tuple (feature name, shap values for each sample) if aggregation is False

        """
        enable_kernel_explainer = False
        try:
            explainer = shap.TreeExplainer(trained_model)
        except Exception as e:
            if 'Model type not yet supported by TreeExplainer' in str(e):
                enable_kernel_explainer = True
                warnings.warn(
                    message='Warning: the current model type (%s) is not supported by TreeExplainer in shap. ' \
                            'Will call KernelExplainer and may take longer to generate the feature importance.' % type(
                        trained_model))
            else:
                raise e
        if enable_kernel_explainer:
            predict_call = getattr(trained_model, "predict_proba", None)
            if predict_call is None or not callable(predict_call):
                if not callable(getattr(trained_model, 'predict', None)):
                    raise Exception(
                        'Fail to initialize explainer as model does not have the function call <predict_proba> and <predict>')
                explainer = shap.KernelExplainer(model=trained_model.predict, data=train_x)
            else:
                explainer = shap.KernelExplainer(model=trained_model.predict_proba, data=train_x)

        shap_values = explainer.shap_values(train_x)
        feature_values = list(zip(self._feature_names, numpy.array(shap_values).transpose().tolist()))
        if mode == MODE.REGRESSION:
            feature_values = [(feature_name, [[x] for x in feature_value]) for feature_name, feature_value in
                              feature_values]
        return feature_values

    def _get_ranking_by_shap(self, trained_model, train_x, mode: str = MODE.CLASSIFICATION) -> List[Tuple[str, float]]:
        """
        Internal function to generate feature ranking using shap value

        Args:
            trained_model: model obj, the trained model object
            train_x: numpy.dnarray, training data
            mode: str, classification (default) or regression

        Returns:
            A list of tuple (feature name, feature importance score) in descending order
        """
        feature_values = self.get_feature_shap_values(trained_model=trained_model, train_x=train_x, mode=mode)
        sum_importance = numpy.zeros(len(self._feature_names))
        shap_values = numpy.array([v for _, v in feature_values]).transpose()
        for ind in range(len(shap_values)):
            global_shap_values = numpy.abs(shap_values[ind]).mean(axis=0)
            sum_importance += global_shap_values
        scores = sum_importance / len(shap_values)
        feature_importance = {key: value for key, value in list(zip(self._feature_names, scores.tolist()))}
        feature_importance = sorted(feature_importance.items(), key=operator.itemgetter(1), reverse=True)

        return feature_importance
