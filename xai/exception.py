#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Exception """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


################################################################################
### ERROR Constants
################################################################################
GENERAL_ERROR = 500


################################################################################
### General Exception
################################################################################
class GeneralException(Exception):
    """General exception."""

    def __init__(self, error_message: str, *, error_code=GENERAL_ERROR):
        super().__init__()
        self._message = error_message
        self._code = error_code

    def __repr__(self):
        return 'Error {}[{}]'.format(self._message, self._code)

    def __str__(self):
        return 'Error {}[{}]'.format(self._message, self._code)

################################################################################
### Compiler Exception
################################################################################
class CompilerException(GeneralException):
    """Compiler exception"""