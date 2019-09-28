#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Components """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from xai.compiler.base import Dict2Obj
from xai.formatter import PdfWriter, HtmlWriter


################################################################################
### PDF
################################################################################
class Pdf(Dict2Obj):

    def exec(self):
        """Execution"""
        return PdfWriter(name=self.name, path=self.path)

################################################################################
### HTML
################################################################################
class Html(Dict2Obj):

    def exec(self):
        """Execution"""
        return HtmlWriter(name=self.name, path=self.path)
