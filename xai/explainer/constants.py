#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

class DOMAIN:
    """
    Domain of the data
    """
    TABULAR = 'tabular'
    TEXT = 'text'


class ALG:
    """
    Code name for algorithms
    """
    LIME = 'lime'
    SHAP = 'shap'

class MODE:
    """
    Problem types for the explainer
    """
    CLASSIFICATION = 'classification'
    REGRESSION = 'regression'

class OUTPUT:
    PREDICTION = 'prediction'
    EXPLANATION = 'explanation'
    FEATURE = 'feature'
    SCORE = 'score'
