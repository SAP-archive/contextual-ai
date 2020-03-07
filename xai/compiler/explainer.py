#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Explainer """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

import xai
from xai.compiler.base import Dict2Obj
from xai.explainer import ExplainerFactory
from xai.explainer.constants import OUTPUT
from xai.explainer.helper import parse_feature_meta_tabular
from xai.formatter import Report


################################################################################
### Model-agnostic Explainer
################################################################################
class ModelAgnosticExplainer(Dict2Obj):
    """
    Compiler for Feature Importance Ranking

    Param:
        package (str, Optional): component package name
        module (str, Optional): component module name
        class (str): component class name

    Attr:
        predict_func (str): path to predict function call pickle
        train_data (str): path to training sample data
        feature_meta (str): path to a meta json file
        method: (str, Optional) interpreter method, default = 'lime'
        num_features (integer, Optional): number of features to show in the explanation, default 10

    Example:
        "component": {
            "package": "xai",
            "module": "compiler",
            "class": "ModelAgnosticExplainer",
            "attr": {
                "predict_func": "./sample_input/func.pkl",
                "train_data": "./sample_input/feature.csv",
                "feature_meta": "./sample_input/feature_meta.json",
                "method": "lime"
                "num_features": 10
            }
        }
    """
    schema = {
        "type": "object",
        "properties": {
            "predict_func": {"type": ["string", "object"]},
            "train_data": {" type": ["string", "object"]},
            "feature_meta": {"type": "string"},
            "domain": {
                "enum": ["tabular", "text"]
            },
            "method": {
                "enum": ["lime", "shap"],
                "default": "lime"
            },
            "num_features": {
                "type": "integer",
                "default": 5
            }
        },
        "required": ["predict_func", "train_data", "domain", "feature_meta"]
    }

    def __init__(self, dictionary):
        """
        Init

        Args:
            dictionary (dict): attribute to set
        """
        super(ModelAgnosticExplainer, self).__init__(dictionary,
                                                     schema=self.schema)

    def __call__(self, report: Report, level: int):
        """
        Execution

        Args:
            report (Report): report object
            level (int): content level
        """
        super(ModelAgnosticExplainer, self).__call__(report=report,
                                                     level=level)
        # -- Load Parameters --
        num_features = self.assert_attr(key='num_features', default=10)
        method = self.assert_attr(key='method', default='lime')
        domain = self.assert_attr(key='domain')

        # -- Load Predict Function --
        predict_fn_var = self.assert_attr(key='predict_func')
        predict_fn = self.load_data(predict_fn_var)

        # -- Load Feature Meta--
        feature_meta_path = self.assert_attr(key='feature_meta', optional=True)
        if not (feature_meta_path is None) \
                and isinstance(feature_meta_path, str):
            with open(feature_meta_path, 'r') as f:
                meta_data = json.load(f)
        else:
            meta_data = {}

        class_names = meta_data.get("class_names", None)

        # -- Load Training Data --
        data_var = self.assert_attr(key='train_data')
        if not (data_var is None):
            train_data = self.load_data(data_var, header=True)
            train_data = train_data.as_matrix()

        kwargs = dict()

        algorithm = xai.ALG.LIME
        if method == 'shap':
            algorithm = xai.ALG.SHAP

        if domain == 'tabular':
            _domain = xai.DOMAIN.TABULAR
            if algorithm == xai.ALG.LIME:
                feature_names, categorical_index, categorical_mapping = parse_feature_meta_tabular(
                    meta_data)
                kwargs.update({"class_names": class_names,
                               "categorical_features": categorical_index,
                               "dict_categorical_mapping": categorical_mapping})
        elif domain == 'text':
            _domain = xai.DOMAIN.TEXT

        explainer_factory = ExplainerFactory.get_explainer(domain=_domain, algorithm=algorithm)

        if _domain == xai.DOMAIN.TABULAR:
            explainer_factory.build_explainer(
                training_data=train_data,
                predict_fn=predict_fn,
                feature_names=feature_names,
                **kwargs
            )
        elif _domain == xai.DOMAIN.TEXT:
            explainer_factory.build_explainer(predict_fn=predict_fn, class_names=class_names)

        explainer_factory.save_explainer('explainer.pkl')

        # -- Add Explainer Information in Report --
        report.detail.add_paragraph('The local explainer is generated as `explainer.pkl`')

        explainer_information = list()
        explainer_information.append(('Domain', domain))
        explainer_information.append(('Algorithm', algorithm))
        explainer_information.append(('Training data shape', train_data.shape))
        explainer_information.append(('Number of features in explanations', min(num_features,train_data.shape[1])))

        report.detail.add_model_info_summary(model_info=explainer_information, notes='Explainer Configuration')
        report.detail.add_header_level_3('Explanation Samples')

        for i in range(2):
            report.detail.add_paragraph_title('Example %s: ' % i)
            explainations = explainer_factory.explain_instance(train_data[i, :],
                                                               num_features=num_features)
            for key, value in explainations.items():
                details = [(item[OUTPUT.FEATURE], "%.3f" % item[OUTPUT.SCORE]) for item in value[OUTPUT.EXPLANATION]]
                report.detail.add_model_info_summary(model_info=details,
                                                     notes='Class %s - Confidence: %s' % (
                                                     class_names[key] if class_names else key, value[OUTPUT.PREDICTION]))
