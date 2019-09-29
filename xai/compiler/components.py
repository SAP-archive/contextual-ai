#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Components """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import dill as pickle

from xai.compiler.base import Dict2Obj
from xai.model.interpreter.feature_interpreter import FeatureInterpreter
from xai.formatter import Report


################################################################################
### Feature Importance Ranking
################################################################################
class FeatureImportanceRanking(Dict2Obj):
    """
    Compiler for Feature Importance Ranking

    Param:
        package (str, Optional): component package name
        module (str, Optional): component module name
        class (str): component class name

    Attr:
        trained_model: path to trained model pickle
        train_data: path to training sample data
        feature_names: path to feature names list (csv)
        method: interpreter method (default/shap)
        threshold: importance threshold

    Example:
        "component": {
            "package": "xai.compiler",
            "module": "components",
            "class": "FeatureImportanceRanking",
            "attr": {
                "trained_model": "./sample_input/model.pkl",
                "train_data": "./sample_input/train.csv",
                "feature_names": "./sample_input/feature_name.csv",
                "method": "default"
                "threshold": 0.005
            }
        }
    """
    schema = {
        "type": "object",
        "properties": {
            "trained_model": {"type": "string"},
            "train_data": {" type": "string"},
            "feature_names": {"type": "string"},
            "method": {
                "enum": ["default", "shap"]
            },
            "threshold": {"type": "number"}
        },
        "required": ["trained_model", "train_data", "feature_names"]
    }

    def __init__(self, dictionary):
        """
        Init

        Args:
            dictionary (dict): attribute to set
        """
        super(FeatureImportanceRanking, self).__init__(dictionary,
                                                       schema=self.schema)

    def __call__(self, report: Report):
        """
        Execution

        Args:
            report (Report): report object
        """
        path = self.assert_attr(key='feature_names')
        with open(path, 'rb') as file:
            feature_names = np.load(file)

        path = self.assert_attr(key='train_data')
        with open(path, 'rb') as file:
            train_data = np.load(file)

        path = self.assert_attr(key='trained_model')
        with open(path, 'rb') as file:
            model = pickle.load(file)

        method = self.assert_attr(key='method', default='default')
        threshold = self.assert_attr(key='threshold', default=0.005)

        fi = FeatureInterpreter(feature_names=feature_names)
        rank = fi.get_feature_importance_ranking(trained_model=model,
                                                 train_x=train_data,
                                                 method=method)
        report.detail.add_feature_importance(
            importance_ranking=rank, importance_threshold=threshold)
