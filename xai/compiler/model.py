#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Model """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
from pandas import DataFrame

from scipy.sparse.csr import csr_matrix

from xai.compiler.base import Dict2Obj
from xai.formatter import Report
from xai.model.interpreter import ModelInterpreter as MI
from xai import (
 ALG,
 MODE
)


################################################################################
### Model Interpreter
################################################################################
class ModelInterpreter(Dict2Obj):
    """
    Compiler for Model Interpreter

    Param:
        package (str, Optional): component package name
        module (str, Optional): component module name
        class (str): component class name

    Attr:
        domain (str): User-provided domain
        method: (str, Optional) interpreter method, default (lime) = 'default'

        ** For Model Interpretation **
        mode: (str, Optional) classification/regression model,
                default = 'classification'
        train_data: numpy.dnarray - Training data
                Each row is a training sample, each column is a feature
        labels: a list of str/int, the class label for each training sample
        predict_func: model object or path to predict function call pickle
        feature_names: array-list of feature names
        target_names: array-list of target names
        model_interpret_stats_type: str, default = 'top_k'
                The pre-defined stats_type for statistical analysis.
                - top_k: how often a feature appears in the top K features in the explanation
                - average_score: average score for each feature in the explanation
                - average_ranking: average ranking for each feature in the explanation
        model_interpret_k_value: int, the k value for `top_k` method and `average_ranking`
                It will be ignored if the stats type are not `top_k` or `average_ranking`
                Default value of k is 5
        model_interpret_top_value: int, the number of top explanation to display
                Default value is 15

        ** For Error Analysis **
        enable_error_analysis: bool set to True to enable error analysis else False to disable
                Default value is False - error analysis disabled
        num_of_class: int, number of classes
        valid_x: A list of 1D ndarray. Validation data
        valid_y: A list of int or a list of str. Validation ground truth class label (str) or (index)
                The type should be consistent to the classes label passed in when building the model interpreter
        error_analysis_stats_type: str, pre-defined types. For now, it supports 3 types:
                - top_k: how often a feature appears in the top K features in the explanation
                - average_score: average score for each feature in the explanation
                - average_ranking: average ranking for each feature in the explanation
                Default type is `top_k`
        error_analysis_k_value:  int, not None. the k value for `top_k` method and `average_ranking`
                It will be ignored if the stats type are not `top_k` or `average_ranking`
                Default value of k is 5
        error_analysis_top_value: int, the number of top error analysis explanation to display
                Default value is 15

    Example:
        "component": {
            "package": "xai",
            "module": "compiler",
            "class": "ModelInterpreter",
            "attr": {
                "domain": "tabular",
                "method": "lime",
                "mode": "classification",
                "train_data": "var:X_train",
                "labels": "var:y_train",
                "predict_func": "var:clf",
                "feature_names": "var:feature_names",
                "target_names": "var:target_names_list",
                "model_interpret_stats_type": "top_k",
                "model_interpret_k_value": 5,
                "model_interpret_top_value": 15,
                "num_of_class": 2,
                "valid_x": "var:X_test",
                "valid_y": "var:y_test",
                "error_analysis_stats_type": "average_score",
                "error_analysis_k_value": 5,
                "error_analysis_top_value": 15,
                "enable_error_analysis": true
            }
        }
    """
    schema = {
        "type": "object",
        "properties": {
            "domain": {
                "enum": ["tabular", "text"],
                "default": "tabular"
            },
            "method": {
                "enum": ["lime", "shap"],
                "default": "lime"
            },
            "mode": {
                "enum": ["classification", "regression"],
                "default": "classification"
            },
            "train_data": {"type": ["string", "object"]},
            "labels": {"type": ["string", "object"]},
            "predict_func": {"type": ["string", "object"]},
            "feature_names": {"type": ["string", "object"]},
            "target_names": {"type": ["string", "object"]},
            "model_interpret_stats_type": {
                "enum": ["top_k", "average_score", "average_ranking"],
                "default": "top_k"
            },
            "model_interpret_k_value": { "type": "number", "default": 5},
            "model_interpret_top_value": { "type": "number", "default": 15},
            "num_of_class": {"type": "number"},
            "valid_x":  {"type": ["string", "object"]},
            "valid_y":  {"type": ["string", "object"]},
            "error_analysis_stats_type": {
                "enum": ["top_k", "average_score", "average_ranking"],
                "default": "top_k"
            },
            "error_analysis_k_value": { "type": "number", "default": 5},
            "error_analysis_top_value": {"type": "number", "default": 15},
            "enable_error_analysis": {"type": "boolean", "default": False}
        },
        "required": ["domain", "train_data", "predict_func",
                     "feature_names", "target_names"],
        "if": {
            "properties": {
                "mode": {"const": "classification"}
            },
            "required": ["num_of_class", "labels"]
        },
        "if": {
            "properties": {
                "enable_error_analysis": {"const": True}
            },
            "required": ["valid_x", "valid_y"]
        }
    }

    def __init__(self, dictionary):
        """
        Init

        Args:
            dictionary (dict): attribute to set
        """
        super(ModelInterpreter, self).__init__(dictionary,
                                               schema=self.schema)

    def __call__(self, report: Report, level: int):
        """
        Execution

        Args:
            report (Report): report object
            level (int): content level
        """
        super(ModelInterpreter, self).__call__(report=report,
                                               level=level)
        domain = self.assert_attr(key='domain')
        method = self.assert_attr(key='method', default=ALG.LIME)
        mode = self.assert_attr(key='mode', default=MODE.CLASSIFICATION)

        # -- Load Training Data --
        data_var = self.assert_attr(key='train_data')
        train_data = None
        if data_var is not None:
            train_data = self.load_data(data_var, header=True)
        if isinstance(train_data, DataFrame):
            train_data = train_data.values
        if isinstance(train_data, csr_matrix):
            train_data = train_data.toarray()

        # -- Load Labels --
        labels = None
        if mode == MODE.CLASSIFICATION:
            labels_var = self.assert_attr(key='labels')
            if labels_var is not None and isinstance(labels_var, str):
                with open(labels_var, 'r') as f:
                    labels = json.load(f)
        # -- Load Predict Function --
        predict_fn_var = self.assert_attr(key='predict_func')
        predict_fn = self.load_data(predict_fn_var)
        # -- Check if feature names is set --
        fn_var = self.assert_attr(key='feature_names', optional=True)
        feature_names = None
        if fn_var is not None:
            feature_names = self.load_data(fn_var)
        # -- Check if target names is set --
        tn_var = self.assert_attr(key='target_names', optional=True)
        target_names = None
        if tn_var is not None:
            target_names = self.load_data(tn_var)
        stats_type = self.assert_attr(key='model_interpret_stats_type',
                                      default='top_k')
        k_value = self.assert_attr(key='model_interpret_k_value', default=5)
        top = self.assert_attr(key="model_interpret_top_value", default=15)

        # -- Error Analysis --
        classes = 0
        en_flag = self.assert_attr(key="enable_error_analysis", default=False)
        if en_flag:
            # -- Check Number of Class --
            if mode == MODE.CLASSIFICATION:
                classes = self.assert_attr(key="num_of_class")
            # -- Load Validation Data --
            valid_x_var = self.assert_attr(key='valid_x', optional=True)
            valid_x = None
            if valid_x_var is not None:
                valid_x = self.load_data(valid_x_var)
            if isinstance(valid_x, DataFrame):
                valid_x = valid_x.values
            # -- Load Validation ground truth class label --
            valid_y_var = self.assert_attr(key='valid_y', optional=True)
            valid_y = None
            if valid_y_var is not None:
                valid_y = self.load_data(valid_y_var)
            if isinstance(valid_y, DataFrame):
                valid_x = valid_y.values
            ea_stats_type = self.assert_attr(key='error_analysis_stats_type',
                                             default='top_k')
            ea_k_value = self.assert_attr(key='error_analysis_k_value',
                                          default=5)
            ea_top = self.assert_attr(key="error_analysis_top_value",
                                      default=15)

        # -- Define the domain and algorithm for interpreter --
        mi = MI(domain=domain, algorithm=method)

        # -- Build and initialize model interpreter --
        mi.build_interpreter(training_data=train_data,
                             training_labels=labels,
                             mode=mode,
                             predict_fn=predict_fn,
                             feature_names=feature_names,
                             class_names=target_names)

        # -- Interpreter the model with training data --
        class_stats, total_count = mi.interpret_model(samples=train_data,
                                                      stats_type=stats_type,
                                                      k=k_value)
        # -- Add Model Interpreter  --
        report.detail.add_model_interpreter(mode=mode, class_stats=class_stats,
                                            total_count=total_count,
                                            stats_type=stats_type,
                                            k=k_value, top=top)

        if en_flag:
            # -- Error Analysis with validation data --
            error_stats = mi.error_analysis(class_num=classes, valid_x=valid_x,
                                            valid_y=valid_y,
                                            stats_type=ea_stats_type,
                                            k=ea_k_value)
            # -- Add Error Analysis --
            report.detail.add_error_analysis(mode=mode, error_stats=error_stats,
                                             stats_type=ea_stats_type,
                                             k=ea_k_value, top=ea_top)
