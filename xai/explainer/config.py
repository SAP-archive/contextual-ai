#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from xai.explainer.constants import DOMAIN, ALG
from xai.explainer.tabular.lime_tabular_explainer import LimeTabularExplainer
from xai.explainer.tabular.shap_tabular_explainer import SHAPTabularExplainer
from xai.explainer.text.lime_text_explainer import LimeTextExplainer

DICT_DOMAIN_TO_CLASS = {
    DOMAIN.TEXT: {
        ALG.LIME: LimeTextExplainer
    },
    DOMAIN.TABULAR: {
        ALG.LIME: LimeTabularExplainer,
        ALG.SHAP: SHAPTabularExplainer
    }
}

DICT_DOMAIN_TO_DEFAULT_ALG = {
    DOMAIN.TEXT: ALG.LIME,
    DOMAIN.TABULAR: ALG.LIME
}
