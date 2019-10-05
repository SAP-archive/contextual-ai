#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

#TODO: consolidate exception

class InvalidExplanationFormat(Exception):
    """
    Raised when an explanation is not of a valid format
    """

    def __init__(self, exp):
        message = 'The following explanation has invalid format! ' \
                  'The entire explanation will be ignored. {}'.format(exp)
        Exception.__init__(self, message)
        self.message = message


class MutipleScoresFoundForSameFeature(Exception):
    """
    Raised when multiple scores are found for the same feature in the explanation
    """

    def __init__(self, feature_name, exp):
        message = 'The following explanation has more than one score for feature [{}]! ' \
                  'The entire explanation will be ignored. {}'.format(
            feature_name, exp)
        Exception.__init__(self, message)
        self.message = message


class UnsupportedMethodType(Exception):
    """
    Raised when method type is not supported.
    """

    def __init__(self, stats_type):
        message = 'The method type [{}] is currently not supported. '.format(stats_type)
        Exception.__init__(self, message)
        self.message = message


class InvalidArgumentError(Exception):
    """
    Raised when the argument is not valid..
    """

    def __init__(self, arg_name, valid_type):
        message = 'The argument [{}] is not of valid type [{}]. '.format(arg_name, valid_type)
        Exception.__init__(self, message)
        self.message = message


class InterpreterUninitializedError(Exception):
    """
    Raised when explanations are attempted to be produced by an unitilized explainer
    """

    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message


class InconsistentSize(Exception):
    """
    Raised when two lists have different lengths
    """

    def __init__(self, column_a, column_b, length_a, length_b):
        message = "'{}' and '{}' have different lengths: {}, " \
                  "{}.".format(column_a, column_b, length_a, length_b)
        Exception.__init__(self, message)
        self.message = message


class TrainingDataNotProvided(Exception):
    """
    Raised when training data is not provided
    """

    def __init__(self):
        message = "Training data is not provided."
        Exception.__init__(self, message)
        self.message = message
