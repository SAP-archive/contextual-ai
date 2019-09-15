#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Utilities """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# -- Publisher Exception --
class PublisherException(Exception):
    """Publisher exception."""

    def __init__(self, error_message: str, *, error_code=None):
        super().__init__()
        self._message = error_message
        self._code = error_code

    def __repr__(self):
        return 'Error {}[{}]'.format(self._message, self._code)

    def __str__(self):
        return 'Error {}[{}]'.format(self._message, self._code)
