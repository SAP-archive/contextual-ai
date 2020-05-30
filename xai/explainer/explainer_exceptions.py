#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

class DomainNotSupported(Exception):
    """
    Raised when an unsupported domain is provided
    """
    def __init__(self, domain):
        message = 'Domain {} is currently not supported.'.format(domain)
        Exception.__init__(self, message)
        self.message = message


class AlgorithmNotFoundInDomain(Exception):
    """
    Raised when an unsupported algorithm is provided
    """
    def __init__(self, domain, algorithm):
        message = 'Algorithm {} is not found in domain {}.'.format(algorithm, domain)
        Exception.__init__(self, message)
        self.message = message


class ExplainerUninitializedError(Exception):
    """
    Raised when explanations are attempted to be produced by an unitilized explainer
    """
    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message

class UnsupportedModeError(Exception):
    """
    Raised when an unsupported mode is provided
    """
    def __init__(self, message):
        Exception.__init__(self, message)
        self.message = message
