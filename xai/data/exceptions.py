#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

class AttributeNotFound(Exception):
    """
    Raised when a defined attribute is not found in the sample
    """

    def __init__(self, attribute_name, sample):
        message = "Attribute '{}' is not found in the sample: {}.".format(attribute_name, sample)
        Exception.__init__(self, message)
        self.message = message


class ColumnNotFound(Exception):
    """
    Raised when a defined column is not found in the dataframe
    """

    def __init__(self, column_name, columns):
        message = "Column '{}' is not found in the dataframe: {}.".format(column_name, columns)
        Exception.__init__(self, message)
        self.message = message


class InconsistentSize(Exception):
    """
    Raised when two lists have different lengths
    """

    def __init__(self, column_A, column_B, length_A, length_B):
        message = "'{}' and '{}' have different lengths: {}, {}.".format(column_A, column_B, length_A, length_B)
        Exception.__init__(self, message)
        self.message = message


class AnalyzerDataTypeNotSupported(Exception):
    """
    Raised when an unsupported analyzer data type is provided
    """

    def __init__(self, data_type):
        message = "Analyzer for data type '{}' is not supported.".format(data_type)
        Exception.__init__(self, message)
        self.message = message


class ItemDataTypeNotSupported(Exception):
    """
    Raised when an unsupported item data type is provided
    """

    def __init__(self, data_type, analyzer_type, supported_types):
        message = "Data type '{}' is not supported for {}. Please input one of the following supported data types:{}". \
            format(data_type, analyzer_type, supported_types)
        Exception.__init__(self, message)
        self.message = message


class NoItemsError(Exception):
    """
    Raised when no items are passed in the stats
    """

    def __init__(self, stats_type):
        message = 'No items passed to the stats object: {}.'.format(stats_type)
        Exception.__init__(self, message)
        self.message = message


class InvalidTypeError(Exception):
    """
    Raised when an object type is invalid
    """

    def __init__(self, att_name, obj_type, supported_types):
        message = "The '{}' type '{}' is invalid, should be '{}'.".format(att_name, obj_type, supported_types)
        Exception.__init__(self, message)
        self.message = message


class InvalidSizeError(Exception):
    """
    Raised when an invalid size is provided
    """

    def __init__(self, att_name, obj_size, supported_sizes):
        message = "The '{}' has invalid size: {}, should be '{}'.".format(att_name, obj_size, supported_sizes)
        Exception.__init__(self, message)
        self.message = message


class UndefinedRequiredParams(Exception):
    """
    Raised when a required params is not defined
    """

    def __init__(self, att_name):
        message = "The '{}' is required but not defined.".format(att_name)
        Exception.__init__(self, message)
        self.message = message
