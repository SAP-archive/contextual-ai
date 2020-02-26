#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import List, Dict, Optional, Any

import numpy as np
from lime.explanation import Explanation

from xai.explainer.constants import MODE, OUTPUT


def explanation_to_json(explanation: Explanation,
                        labels: List[int],
                        predictions: np.ndarray,
                        mode: str) -> Dict[int, Dict]:
    """
    Parses LIME explanation to produce JSON-parseable output format.

    ### Schema for classification:
    {
        class_idx: {OUTPUT.EXPLANATION: [
                    {
                    OUTPUT.FEATURE: str,
                    OUTPUT.SCORE: float
                    },
                      ...
                    ],
        OUTPUT.PREDICTION: float},
        ...
    }

    ### Schema for regression:
    {
        OUTPUT.EXPLANATION: [
            {
                OUTPUT.FEATURE: str,
                OUTPUT.SCORE: float
            }
            ...
        ],
        'predictions': float
    }

    Args:
        explanation (lime.explanation.Explanation): The explanation output from LIME
        labels (list): List of labels for which to get explanations
        predictions (np.ndarray): Model output for a particular instance, which should be a list
        of confidences that sum to one (if classification)
        mode (str): Regression or classification

    Returns:
        (dict) Explanations in JSON format
    """
    dict_explanation = {}

    if mode == MODE.CLASSIFICATION:
        for label in labels:
            list_explanations = explanation.as_list(label)
            tmp = []
            for exp in list_explanations:
                tmp.append({OUTPUT.FEATURE: str(exp[0]), OUTPUT.SCORE: float(exp[1])})
            dict_explanation[label] = {
                OUTPUT.PREDICTION: predictions[label],
                OUTPUT.EXPLANATION: sorted(tmp, key=lambda x: x[OUTPUT.SCORE], reverse=True)
            }
    else:
        list_explanations = explanation.as_list()
        tmp = []
        for exp in list_explanations:
            tmp.append({OUTPUT.FEATURE: str(exp[0]), OUTPUT.SCORE: float(exp[1])})
        dict_explanation = {
            OUTPUT.PREDICTION: predictions,
            OUTPUT.EXPLANATION: sorted(tmp, key=lambda x: x[OUTPUT.SCORE], reverse=True)
        }

    return dict_explanation


def parse_shap_values(shap_values: List[np.ndarray], confidences: List[float],
                      feature_names: Optional[List[str]] = None,
                      feature_values: Optional[List[Any]] = None) -> Dict[int, Dict]:
    """
    Parse SHAP values to fit XAI output format

    Args:
        shap_values (list): A list of shap values, a set for each class
        confidences (list): Confidences for each class
        feature_names (list): List of feature names
        feature_values (list): List of values corresponding to feature_names

    Returns:
        (dict) A mapping of class to explanations

    """
    assert len(shap_values) == len(confidences), 'Number of SHAP values should be equal to ' \
                                                 'number of classes!'

    dict_explanation = {}

    for label, confidence in enumerate(confidences):
        tmp = []

        shap_value_class = shap_values[label][0]
        for feature_idx, shap_value in enumerate(shap_value_class):
            # We ignore features which SHAP values are 0, which indicate that they had no
            # impact on the model's decision
            if shap_value != 0:
                if feature_names and feature_values:
                    feature = '{} = {}'.format(
                        feature_names[feature_idx], feature_values[feature_idx])
                    tmp.append({OUTPUT.FEATURE: feature, OUTPUT.SCORE: shap_value})
                else:
                    tmp.append({OUTPUT.FEATURE: feature_idx, OUTPUT.SCORE: shap_value})

        dict_explanation[label] = {
            OUTPUT.PREDICTION: confidence,
            OUTPUT.EXPLANATION: tmp
        }

    return dict_explanation
