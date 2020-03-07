#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Model """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from xai.compiler.base import Dict2Obj
from xai.formatter import Report
from xai.model.interpreter import ModelInterpreter
from xai import (
 ALG,
 MODE
)


################################################################################
### Model Interpreter By Class
################################################################################
class ModelInterpreterByClass(Dict2Obj):
    """
    Compiler for Model Interpreter by Class

    Param:
        package (str, Optional): component package name
        module (str, Optional): component module name
        class (str): component class name

    Attr:
        domain (str): User-provided domain
        method: (str, Optional) interpreter method, default (lime) = 'default'
        mode: (str, Optional) classification/regression model,
                default = 'classification'
        train_data: numpy.dnarray - Training data
                Each row is a training sample, each column is a feature
        labels: a list of str/int, the class label for each training sample
        predict_func: model object or path to predict function call pickle
        feature_names: array-list of feature names
        target_names: array-list of target names
        stats_type: str, default = 'top_k'
                The pre-defined stats_type for statistical analysis.
                For details see `xai.model_interpreter.explanation_aggregator.get_statistics()`
        k: int, the k value for `top_k` method and `average_ranking`.
                It will be ignored if the stats type are not `top_k` or `average_ranking`.
                Default value of k is 5.
        num_of_top_explanation: int, the number of top explanation to display
                Default value is 15

    Example:
        "component": {
            "package": "xai",
            "module": "compiler",
            "class": "ModelInterpreterByClass",
            "attr": {
                "domain": "tabular",
                "method": "lime",
                "mode": "classification",
                "train_data": "var:X_train",
                "labels": "var:y_train",
                "predict_func": "var:clf",
                "feature_names": "var:feature_names",
                "target_names": "var:target_names_list",
                "stats_type": "top_k",
                "k": 5,
                "num_of_top_explanation": 15
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
            "state_type": {
                "enum": ["top_k", "average_score", "average_ranking"],
                "default": "top_k"
            },
            "k": {
                "type": "number",
                "default": 5
            },
            "num_of_top_explanation": {
                "type": "number",
                "default": 15
            }
        },
        "required": ["domain", "train_data", "labels", "predict_func",
                     "feature_names", "target_names"]
    }

    def __init__(self, dictionary):
        """
        Init

        Args:
            dictionary (dict): attribute to set
        """
        super(ModelInterpreterByClass, self).__init__(dictionary,
                                               schema=self.schema)

    def __call__(self, report: Report, level: int):
        """
        Execution

        Args:
            report (Report): report object
            level (int): content level
        """
        super(ModelInterpreterByClass, self).__call__(report=report,
                                               level=level)
        domain = self.assert_attr(key='domain')
        method = self.assert_attr(key='method', default=ALG.LIME)
        mode = self.assert_attr(key='mode', default=MODE.CLASSIFICATION)

        # -- Load Training Data --
        data_var = self.assert_attr(key='train_data')
        train_data = None
        if not (data_var is None):
            train_data = self.load_data(data_var, header=True)
        # -- Load Labels --
        labels_var = self.assert_attr(key='labels')
        labels = None
        if labels_var is not None and isinstance(labels_var, str):
            with open(labels_var, 'r') as f:
                labels = json.load(f)
        # -- Load Predict Function --
        predict_fn_var = self.assert_attr(key='predict_func')
        predict_cls = self.load_data(predict_fn_var)
        predict_fn = predict_cls.predict_proba
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
        stats_type = self.assert_attr(key='state_type', default='top_k')
        k_value = self.assert_attr(key='k', default=5)
        top = self.assert_attr(key="num_of_top_explanation", default=15)

        # -- Define the domain and algorithm for interpreter --
        mi = ModelInterpreter(domain=domain, algorithm=method)

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
        # -- Add Feature Importance for class --
        report.detail.add_model_interpreter_by_class(class_stats=class_stats,
                                                     total_count=total_count,
                                                     top=top)
