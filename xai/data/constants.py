#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

class THRESHOLD:
    """
    Predefined threshold for data type identification
    """
    UNIQUE_VALUE_REL_THRESHOLD = 0.3
    FLOAT_UNIQUE_ABS_THRESHOLD = 10
    INT_UNIQUE_ABS_THRESHOLD = 15


class DATATYPE:
    """
    Predefined data type for data analyzer
    """

    TYPE = 'type'
    USED = 'used'
    STRUCTURED = 'structured'
    ATTRIBUTE = 'attribute'
    SEQUENCE = 'sequence'

    CATEGORY = 'categorical'
    NUMBER = 'numerical'
    FREETEXT = 'text'
    DATETIME = 'datetime'
    LABEL = 'label'
    KEY = 'key'


class STATSCONSTANTS:
    """
    Constants for stats generation
    """
    DEFAULT_BIN_SIZE = 10
    KDE_BAND_WIDTH = 0.2
    KDE_XGRID_RESOLUTION = 100


class STATSKEY:
    """
    Constants for key used in stats json object
    """
    TOTAL_COUNT = 'total_count'
    NAN_COUNT = 'nan_count'
    DATA_TYPE = 'data_type'
    DATA_COLUMN_NAME = 'attribute_name'
    STATS = 'stats'

    DISTRIBUTION = 'frequency'
    FIELDS = 'fields'

    class DISTRIBUTION_KEY:
        ATTRIBUTE_NAME = 'value'
        ATTRIBUTE_COUNT = 'count'

    HISTOGRAM = 'distribution'

    class HISTOGRAM_KEY:
        X_LEFT = 'bin_left_edge'
        X_RIGHT = 'bin_right_edge'
        BIN_COUNT = 'bin_count'

    KDE = 'kernel_density_estimation'

    class KDE_KEY:
        X = 'x'
        Y = 'y'

    MIN = 'minimum'
    MAX = 'maximum'
    MEAN = 'mean'
    MEDIAN = 'median'
    STDDEV = 'standard_deviation'

    TFIDF = 'tfidf'
    TF = 'term_frequency'
    DF = 'document_frequency'
    PATTERN = 'pattern'

    class PATTERN:
        PATTERN_NAME = 'pattern_name'
        PATTERN_TF = 'occurrence'
        PATTERN_DF = 'doc_with_pattern'


class TermFrequencyType:
    """
    Constants for term frequency type
    """
    TF_ABSOLUTE = 1
    TF_BOOLEAN = 2
    TF_NORMALIZED_BY_MAX = 3
    TF_NORMALIZED_BY_DOC = 4
    TF_LOGARITHM = 5
    TF_AUGMENTED = 6


class DatetimeResolution:
    """
    Constants for datetime resolution
    """
    YEAR = 0
    MONTH = 1
    DAY = 2
    WEEKDAY = 3
    HOUR = 4
    MINUTE = 5
    SECOND = 6
