#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Evaluation """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

import numpy as np

from xai.compiler.base import Dict2Obj
from xai.constants import METRIC_CM
from xai.formatter import Report
from xai.model.evaluation.result_compiler import ResultCompiler


################################################################################
### Classification Evaluation Result
################################################################################
class ClassificationEvaluationResult(Dict2Obj):
    """
    Compiler for Feature Importance Ranking

    Param:
        package (str, Optional): component package name
        module (str, Optional): component module name
        class (str): component class name

    Attr:
        y_true_file (str): path to test ground-true sample data
        y_pred_file (str): path to test predict sample data
        labels_file (str): path to a label json file

    Example:
        "component": {
            "package": "xai",
            "module": "compiler",
            "class": "ClassificationEvaluationResult",
            "attr": {
                "y_true_file": "./sample_input/y_true.csv",
                "y_pred_file": "./sample_input/y_pred.csv",
                "labels_file": "./sample_input/labels.json",
            }
        }
    """
    schema = {
        "type": "object",
        "properties": {
            "y_true_file": {"type": ["string", "object"]},
            "y_pred_file": {"type": ["string", "object"]},
            "labels_file": {"type": "string"}
        },
        "required": ["y_true_file", "y_pred_file", "labels_file"]
    }

    def __init__(self, dictionary):
        """
        Init

        Args:
            dictionary (dict): attribute to set
        """
        super(ClassificationEvaluationResult, self).__init__(dictionary,
                                                             schema=self.schema)

    def __call__(self, report: Report, level: int):
        """
        Execution

        Args:
            report (Report): report object
            level (int): content level
        """
        super(ClassificationEvaluationResult, self).__call__(report=report,
                                                             level=level)
        # -- Load Result Filepath --
        y_true_var = self.assert_attr(key='y_true_file')
        y_pred_var = self.assert_attr(key='y_pred_file')
        labels_file = self.assert_attr(key='labels_file')

        # -- Load Data --
        y_true = None
        if y_true_var is not None:
            y_true = self.load_data(y_true_var)
            y_true = y_true.values.flatten()

        y_pred = None
        y_conf = None
        if y_pred_var is not None:
            y = self.load_data(y_pred_var)
            y = y.values
            if len(y.shape) == 1 or y.shape[1] == 1:
                y = y.flattern()
                if len(y.unique()) > 2:
                    y_conf = np.ones((y_true.shape[0], 2))
                    y_conf[:, 1] = y
                    y_conf[:, 0] = y_conf[:, 0] - y
                    y_pred = np.argmax(y_conf, axis=1)
                else:
                    y_pred = y
            else:
                y_conf = y
                y_pred = np.argmax(y_conf, axis=1)

        labels = None
        if labels_file is not None and isinstance(labels_file, str):
            with open(labels_file, 'r') as f:
                labels = json.load(f)

        # -- Create Result Object --
        result_complier = ResultCompiler(labels=labels)

        if y_conf is None:
            result_complier.load_results_from_raw_labels(y_true=y_true, y_pred=y_pred)
        else:
            result_complier.load_results_from_raw_prediction(y_true=y_true, y_prob=y_conf)

        if len(labels) <= 2:
            report.detail.add_header_level_2('Metric Scores')
            report.detail.add_binary_class_evaluation_metric_results(('Testing', result_complier.metric_scores_))

            report.detail.add_header_level_2('Confusion Matrix')
            report.detail.add_confusion_matrix_results(('', result_complier.metric_scores_[METRIC_CM]))

            result_pkg = {'gt': y_true, 'probability': y_conf}

            report.detail.add_header_level_2('Confidence Distribution')
            report.detail.add_binary_class_confidence_distribution(('Testing', result_pkg))

            report.detail.add_header_level_2('Reliability Diagram')
            report.detail.add_binary_class_reliability_diagram(('Testing', result_pkg))

        else:
            report.detail.add_header_level_2('Metric Scores')

            report.detail.add_multi_class_evaluation_metric_results(('Testing', result_complier.metric_scores_))

            report.detail.add_header_level_2('Confusion Matrix')
            report.detail.add_confusion_matrix_results(('', result_complier.metric_scores_[METRIC_CM]))
            result_pkg = dict()
            if y_conf is not None:
                for idx, label in enumerate(labels):
                    result_pkg[label] = dict()
                    result_pkg[label]['probability'] = y_conf[y_pred == idx, idx]
                    result_pkg[label]['gt'] = y_true[y_pred == idx]

                report.detail.add_header_level_2('Confidence Distribution')
                report.detail.add_multi_class_confidence_distribution(('Testing', result_pkg))
