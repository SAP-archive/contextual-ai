#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Components """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path
import numpy as np

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
                "enum": ["default", "shap"],
                "default": "default"
            },
            "threshold": {
                "type": "number",
                "default": 0.005
            }
        },
        "anyOf": [
            {
                "properties": {
                    "method": {"const": "shap"}
                },
                "required": ["train_data"]
            }
        ],
        "required": ["trained_model"]
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
        threshold = self.assert_attr(key='threshold', default=0.005)
        method = self.assert_attr(key='method', default='default')

        model_path = self.assert_attr(key='trained_model')
        model = self.load_data(Path(model_path))

        header = True
        fn_path = self.assert_attr(key='feature_names', optional=True)
        feature_names = None
        if not (fn_path is None):
            feature_names = self.load_data(Path(fn_path))
            header = False
        # -- Load Training Data for default method --
        data_path = self.assert_attr(key='train_data',
                                     optional=(method=='default'))
        train_data = None
        if not (data_path is None):
            train_data = self.load_data(Path(data_path), header=header)
            if  header:
                feature_names = train_data.columns

        fi = FeatureInterpreter(feature_names=feature_names)
        rank = fi.get_feature_importance_ranking(trained_model=model,
                                                 train_x=train_data,
                                                 method=method)
        report.detail.add_feature_importance(
            importance_ranking=rank, importance_threshold=threshold)
