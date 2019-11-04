#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Basic Content - commonly use """


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import List, Tuple

from xai.formatter.contents.base import Content
from xai.formatter.writer.base import Writer


################################################################################
###  Basic Key Value Pairs
################################################################################
class BasicKeyValuePairs(Content):
    """
    Basic Key-Value pairs info
    """

    def __init__(self, info: list, notes=None) -> None:
        """
        Add key-value pairs information to the report

        Args:
            info (list): list of tuple / list of (list of tuple))
                multi-level rendering, e.g. to display `model_info`
            notes (str, Optional):
                explain the block
        """
        super(BasicKeyValuePairs, self).__init__(info, notes)
        self._info = info
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "Basic Info (key-value pairs)"

    @property
    def info(self):
        """Returns key-value pairs information."""
        return self._info

    @property
    def notes(self):
        """Returns block description."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Basic Info (key-value pairs) Paragraph

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_basic_key_value_pairs(notes=self.notes, info=self.info)
