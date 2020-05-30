#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
# -- Data Helper --


import json
import warnings
from collections import Counter

from statistics import median

import dateutil
import numpy as np
import math

from xai.data.constants import DATATYPE, THRESHOLD
from xai.data.explorer import (
    CategoricalDataAnalyzer,
    DataAnalyzerSuite
)
from xai.data.validator import MissingValidator


################################################################################
### Data Helper
################################################################################

def get_column_types(*, data, threshold, label=None):
    """
    Retrieve data with default data type, when metadata is not provided

    Args:
        data (pandas): sample data
        threshold (float): data threshold
        label (str, Optional): label column name

    Returns:
        feature, valid_feature_names, valid_feature_types, meta
    """
    def check_key(_data):
        if _data.dtypes in [np.int32, np.int64, np.int16]:
            if _data.is_monotonic:
                return True
            else:
                return False
        else:
            return False

    def check_numerical(_data):
        if _data.dtypes in [np.float64, np.float32, np.int16, np.int32, np.int64]:
            return True
        else:
            return False

    def check_datetime(_data):
        if _data.dtypes in [np.int16, np.int64, np.int32]:
            return False

        def parse_date(_date):
            try:
                dateutil.parser.parse(str(_date))
                return 0
            except ValueError:
                return 1
            except OverflowError:
                return 1

        counter = Counter(_data.tolist())
        if len(counter) >= threshold * len(_data):
            invalid_count = 0
            for date in _data.tolist():
                invalid_count += parse_date(date)
            if invalid_count < threshold * len(_data):
                return True
            else:
                return False
        else:
            return False

    def check_categorical(_data):
        counter = Counter([str(x) if type(x) == float and math.isnan(x) else x for x in _data.tolist()])
        if _data.dtypes in [np.float64, np.float32]:
            _threshold = min(THRESHOLD.FLOAT_UNIQUE_ABS_THRESHOLD,
                             threshold * len(_data))  ## for float type, strict the threshold
        elif _data.dtypes in [np.int16, np.int32, np.int64]:
            _threshold = min(THRESHOLD.INT_UNIQUE_ABS_THRESHOLD,
                             threshold * len(_data))  ## for int type, strict the threshold
        else:
            _threshold = threshold * len(_data)
        if len(counter) < _threshold:
            _median = median(counter.values())
            if _median == 1:
                return False
            else:
                return True
        else:
            return False

    def check_text(_data):
        if _data.dtypes != object:
            return False

        def _get_token_number(x):
            x = str(x)
            return len(x.split(' '))

        if len(_data.unique()) > len(_data) * threshold:
            if median(col_data.apply(_get_token_number)) >= 2:
                return True
            else:
                return False
        else:
            return False

    valid_feature_names = []
    valid_feature_types = []
    feature = dict()
    feature[DATATYPE.CATEGORY] = []
    feature[DATATYPE.NUMBER] = []
    feature[DATATYPE.FREETEXT] = []
    feature[DATATYPE.DATETIME] = []
    meta = {}

    for column in data.columns:
        if column == label:
            meta[column] = {DATATYPE.TYPE: DATATYPE.LABEL,
                            DATATYPE.USED: True,
                            DATATYPE.STRUCTURED: DATATYPE.ATTRIBUTE}
            continue
        col_data = data[column]

        if check_datetime(_data=col_data):
            # datetime data
            feature[DATATYPE.DATETIME].append(column)
            valid_feature_names.append(column)
            valid_feature_types.append(DATATYPE.DATETIME)
            meta[column] = {DATATYPE.TYPE: DATATYPE.DATETIME,
                            DATATYPE.USED: True,
                            DATATYPE.STRUCTURED: DATATYPE.ATTRIBUTE}

        elif check_categorical(_data=col_data):
            # categorical data
            feature[DATATYPE.CATEGORY].append(column)
            valid_feature_names.append(column)
            valid_feature_types.append(DATATYPE.CATEGORY)
            meta[column] = {DATATYPE.TYPE: DATATYPE.CATEGORY,
                            DATATYPE.USED: True,
                            DATATYPE.STRUCTURED: DATATYPE.ATTRIBUTE}

        elif check_key(_data=col_data):
            warnings.warn(
                message='Warning: the feature [%s] is suspected to be key feature as it is monotonic integer. \n'
                        '[Examples]: %s\n' % (column, col_data.tolist()[:5]))
            meta[column] = {DATATYPE.TYPE: DATATYPE.KEY,
                            DATATYPE.USED: False,
                            DATATYPE.STRUCTURED: DATATYPE.ATTRIBUTE}

        elif check_numerical(_data=col_data):
            # numerical data
            feature[DATATYPE.NUMBER].append(column)
            valid_feature_names.append(column)
            valid_feature_types.append(DATATYPE.NUMBER)
            meta[column] = {DATATYPE.TYPE: DATATYPE.NUMBER,
                            DATATYPE.USED: True,
                            DATATYPE.STRUCTURED: DATATYPE.ATTRIBUTE}
        elif check_text(_data=col_data):
            # text data
            feature[DATATYPE.FREETEXT].append(column)
            valid_feature_names.append(column)
            valid_feature_types.append(DATATYPE.FREETEXT)
            meta[column] = {DATATYPE.TYPE: DATATYPE.FREETEXT,
                            DATATYPE.USED: True,
                            DATATYPE.STRUCTURED: DATATYPE.ATTRIBUTE}

        else:
            warnings.warn(
                message='Warning: the feature [%s] is suspected to be identifiable feature. \n'
                        '[Examples]: %s\n' % (column, col_data.tolist()[:5]))
            meta[column] = {DATATYPE.TYPE: DATATYPE.KEY,
                            DATATYPE.USED: False,
                            DATATYPE.STRUCTURED: DATATYPE.ATTRIBUTE}

    return feature, valid_feature_names, valid_feature_types, meta

def get_valid_datatypes_from_meta(meta:dict):
    """
    Parse the meta data into valid input for data analyzers

    Args:
        meta: dict, data meta data

    Returns:
        feature: dict, which maps to data type for feature names
        valid_feature_names: list, which contains all valid feature names
        valid_feature_types: list, which contains all valid feature types
        sequence_features: list, which contains all sequence features
        label: str, label column name
    """
    label = None
    sequence_features = []
    valid_feature_names = []
    valid_feature_types = []
    feature = dict()
    feature[DATATYPE.CATEGORY] = []
    feature[DATATYPE.NUMBER] = []
    feature[DATATYPE.FREETEXT] = []
    feature[DATATYPE.DATETIME] = []

    for feature_name, feature_config in meta.items():
        feature_type = feature_config[DATATYPE.TYPE]
        structured = feature_config[DATATYPE.STRUCTURED]

        if structured == DATATYPE.SEQUENCE:
            sequence_features.append(feature_name)

        if feature_type == DATATYPE.LABEL:
            label = feature_name
        if feature_type == DATATYPE.CATEGORY:
            valid_feature_types.append(DATATYPE.CATEGORY)
            valid_feature_names.append(feature_name)
            feature[DATATYPE.CATEGORY].append(feature_name)
        elif feature_type == DATATYPE.NUMBER:
            valid_feature_types.append(DATATYPE.NUMBER)
            valid_feature_names.append(feature_name)
            feature[DATATYPE.NUMBER].append(feature_name)
        elif feature_type == DATATYPE.FREETEXT:
            valid_feature_types.append(DATATYPE.FREETEXT)
            valid_feature_names.append(feature_name)
            feature[DATATYPE.FREETEXT].append(feature_name)
        elif feature_type == DATATYPE.DATETIME:
            valid_feature_types.append(DATATYPE.DATETIME)
            valid_feature_names.append(feature_name)
            feature[DATATYPE.DATETIME].append(feature_name)

    return feature, valid_feature_names, valid_feature_types, \
           sequence_features, label

def cast_type_to_string(*, data, feature_names: list):
    """
    Cast non-str/int column to string

    Args:
        data (pandas): sample data
        feature_names (list): feature names which not int or str
    """
    def cast_to_str(x):
        return str(x)

    for feature_name in feature_names:
        data[feature_name] = data[feature_name].astype(dtype=object).apply(cast_to_str)

def get_label_distribution(*, data, label):
    """
    Retrieve data label distribution

    Args:
        data (pandas): sample data
        label (str): label column name

    Returns:
        label_distributions
    """
    label_analyzer = CategoricalDataAnalyzer()
    label_analyzer.feed_all(data[label].tolist())
    label_stats = label_analyzer.get_statistics()

    label_distributions = list()
    label_distributions.append((label, label_stats.frequency_count))
    return label_distributions


def get_missing_value_count(*, data, feature_names, feature_types):
    """
    Retrieve missing value count

    Args:
        data (pandas): sample data
        feature_names (list): valid feature names
        feature_types (list): valid feature types

    Returns:
        missing_value_count, total_count
    """

    def generate_missing_value_schema():
        missing_value_schema = dict()
        for name, column_type in zip(feature_names, feature_types):
            if column_type in [DATATYPE.CATEGORY, DATATYPE.DATETIME, DATATYPE.FREETEXT]:
                missing_value_schema[name] = [str(np.nan)]
            else:
                missing_value_schema[name] = []
        return missing_value_schema

    schema = generate_missing_value_schema()
    json_line = json.loads(data.to_json(orient='records'))
    missing_validator = MissingValidator(schema=schema)
    missing_validator.validate_all(sample_list=json_line)
    stats = missing_validator.get_statistics()
    missing_count = dict(stats.column_stats)
    total_count = {feature_name: stats.total_count for feature_name in
                   schema.keys()}
    return missing_count, total_count


def get_data_statistics(*, data, feature_names, feature_types, label=None):
    """
    Retrieve missing value count

    Args:
        data (pandas): sample data
        feature_names (list): valid feature names
        feature_types (list): valid feature types
        label (str, Optional): label column name

    Returns:
        data_stats
    """
    data_analyzer_suite = DataAnalyzerSuite(data_type_list=feature_types,
                                            column_names=feature_names)
    labels = None
    if not (label is None):
        labels = data[label]

    for column, column_type in zip(feature_names, feature_types):
        data_analyzer_suite.feed_column(column_name=column,
                                        column_data=data[column].tolist(),
                                        labels=labels)

    stats = data_analyzer_suite.get_statistics()
    return stats
