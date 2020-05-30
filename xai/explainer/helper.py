#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import Tuple


def parse_feature_meta_tabular(metadata: dict) -> Tuple[list, list, dict]:
    """
    parse feature meta data for tabular
    Args:
        metadata: dict contains class information and feature information

    Returns:
        feature_names: list of feature names
        categorical_idx: list of index of categorical feature
        categorical_mapping: a dict maps feature column index to a list of encoding text

    """
    feature_names = list()
    categorical_idx = list()
    categorical_mapping = dict()
    feature_meta = metadata.get("feature_types", [])
    for idx, feature in enumerate(feature_meta):
        feature_names.append(feature['name'])
        type = feature['type']
        if type == 'categorical':
            categorical_idx.append(idx)
            mapping = feature.get('mapping', None)
            if mapping:
                categorical_mapping[idx] = mapping

    return feature_names, categorical_idx, categorical_mapping
