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

from xai.data.constants import DATATYPE
from xai.data.explorer import (
    CategoricalDataAnalyzer,
    DataAnalyzerSuite
)
from xai.data.validator import EnumValidator


################################################################################
### Data Helper
################################################################################

def get_column_types(*, data, threshold, label):
    """
    Retrieve data with default data type, when metadata is not provided

    Args:
        data (pandas): sample data
        threshold (float): data threshold
        label (str): label column name

    Returns:
        feature, valid_feature_names, valid_feature_types, meta
    """

    def check_numerical(_data):
        if _data.dtypes == np.float64:
            return True
        else:
            return False

    def check_datetime(_data):
        if _data.dtypes == np.int64:
            return False

        def parse_date(_date):
            try:
                dt = dateutil.parser.parse(str(_date))
                return 0
            except ValueError:
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
        counter = Counter(_data.tolist())
        if len(counter) < threshold * len(_data):
            _median = median(counter.values())
            if _median == 1:
                return False
            else:
                return True
        else:
            return False

    def check_text(_data):
        def _get_token_number(x):
            return len(x.split(' '))

        if _data.dtypes == object:
            if len(_data.unique()) > len(_data) * threshold:
                if median(col_data.apply(_get_token_number)) > 3:
                    return True
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
            meta[column] = {'type': DATATYPE.LABEL,
                            'used': True,
                            'structured': 'attribute'}
            continue
        col_data = data[column]

        if check_datetime(_data=col_data):
            # datetime data
            feature[DATATYPE.DATETIME].append(column)
            valid_feature_names.append(column)
            valid_feature_types.append(DATATYPE.DATETIME)
            meta[column] = {'type': DATATYPE.DATETIME,
                            'used': True,
                            'structured': 'attribute'}

        elif check_numerical(_data=col_data):
            # numerical data
            feature[DATATYPE.NUMBER].append(column)
            valid_feature_names.append(column)
            valid_feature_types.append(DATATYPE.NUMBER)
            meta[column] = {'type': DATATYPE.NUMBER,
                            'used': True,
                            'structured': 'attribute'}

        elif check_categorical(_data=col_data):
            # categorical data
            feature['categorical'].append(column)
            valid_feature_names.append(column)
            valid_feature_types.append(DATATYPE.CATEGORY)
            meta[column] = {'type': DATATYPE.CATEGORY,
                            'used': True,
                            'structured': 'attribute'}

        elif check_text(_data=col_data):
            # text data
            feature['text'].append(column)
            valid_feature_names.append(column)
            valid_feature_types.append(DATATYPE.FREETEXT)
            meta[column] = {'type': DATATYPE.FREETEXT,
                            'used': True,
                            'structured': 'attribute'}

        else:
            warnings.warn(
                message='Warning: the feature [%s] is suspected to be identifierable feature. \n'
                        '[Examples]: %s\n' % (column, col_data.tolist()[:5]))
            meta[column] = {'type': DATATYPE.KEY,
                            'used': True,
                            'structured': 'attribute'}

    return feature, valid_feature_names, valid_feature_types, meta

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
            if column_type == DATATYPE.CATEGORY:
                missing_value_schema[name] = ['NAN']
            if column_type == DATATYPE.NUMBER:
                missing_value_schema[name] = ['NaN']
        return missing_value_schema

    schema = generate_missing_value_schema()
    json_line = json.loads(data.to_json(orient='records'))
    enum_validator = EnumValidator(schema=schema)
    enum_validator.validate_all(sample_list=json_line)
    stats = enum_validator.get_statistics()
    missing_count = dict(stats.column_stats)
    total_count = {feature_name: stats.total_count for feature_name in
                   schema.keys()}
    return missing_count, total_count

def get_data_statistics(*, data, feature_names, feature_types, label):
    """
    Retrieve missing value count

    Args:
        data (pandas): sample data
        feature_names (list): valid feature names
        feature_types (list): valid feature types
        label (str): label column name

    Returns:
        data_stats
    """
    data_analyzer_suite = DataAnalyzerSuite(data_type_list=feature_types,
                                            column_names=feature_names)
    for column, column_type in zip(feature_names, feature_types):
        if column_type == DATATYPE.CATEGORY:
            data[column][data[column].isnull()] = 'NAN'
        data_analyzer_suite.feed_column(column_name=column,
                                        column_data=data[column].tolist(),
                                        labels=data[label])
    stats = data_analyzer_suite.get_statistics()
    return stats
