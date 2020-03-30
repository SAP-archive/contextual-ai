#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Writers """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from xai.compiler.base import Dict2Obj
from xai.formatter import Report, PdfWriter, HtmlWriter


################################################################################
### PDF
################################################################################
class Pdf(Dict2Obj):
    """
    Compiler Report in PDF format

    Param:
        package (str, Optional): component package name
        module (str, Optional): component module name
        class (str): component class name

    Attr:
        name: report file name
        path: path to persist the report

    Example:
      "writers": [
        {
          "class": "Pdf",
          "attr": {
            "name": "first-simple-report",
            "path": "./sample_output"
          }
        }
      ]
    """
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "path": {" type": "string"}
        },
        "required": ["name"]
    }

    def __init__(self, dictionary):
        """
        Init

        Args:
            dictionary (dict): attribute to set
        """
        super(Pdf, self).__init__(dictionary, schema=self.schema)

    def __call__(self, report: Report, level=None):
        """
        PDF Report Generation

        Args:
            report (Report): report object
            level (int): content level
        """
        name = self.assert_attr(key='name')
        path = self.assert_attr(key='path', default='./')
        report.generate(writer=PdfWriter(name=name, path=path))

################################################################################
### HTML
################################################################################
class Html(Dict2Obj):
    """
    Compiler Report in HTML format

    Param:
        package (str, Optional): component package name
        module (str, Optional): component module name
        class (str): component class name

    Attr:
        name: report file name
        path: path to persist the report

    Example:
      "writers": [
        {
          "class": "Html",
          "attr": {
            "name": "first-simple-report",
            "path": "./sample_output",
            "style": "./simple.css",
            "script": "./simple.jsp"
          }
        }
      ]
    """
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "path": {" type": "string"},
            "style": {" type": "string"},
            "script": {" type": "string"}
        },
        "required": ["name", "path"]
    }

    def __init__(self, dictionary):
        """
        Init

        Args:
            dictionary (dict): attribute to set
        """
        super(Html, self).__init__(dictionary, schema=self.schema)

    def __call__(self, report: Report, level=None):
        """
        HTML Report Generation

        Args:
            report (Report): report object
            level (int): content level
        """
        name = self.assert_attr(key='name')
        path = self.assert_attr(key='path')
        report.generate(writer=HtmlWriter(name=name, path=path))
