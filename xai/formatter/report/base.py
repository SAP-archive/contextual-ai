#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Report Object """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from xai.formatter.report.section import (
    CoverSection,
    DetailSection
)
from xai.formatter.writer.base import Writer


################################################################################
### Report Template
################################################################################
class Report:

    def __init__(self, name: str) -> None:
        """
        Report Template
        Attributes:
            name(str): the report name
        """
        self._name = name

        self._writer = None
        self._cover_section = CoverSection()
        self._detail_section = DetailSection()
        self._has_content_table = True # default having content table

    @property
    def name(self):
        """Returns report name."""
        return self._name

    @property
    def cover(self):
        """Returns cover section."""
        return self._cover_section

    @property
    def content(self):
        """Returns detail section."""
        return self._detail_section

    @property
    def has_content_table(self):
        """Check if content table enabled."""
        return self._has_content_table

    @has_content_table.setter
    def has_content_table(self, indicator: bool):
        """
        Enable/disable content table
        Args:
            indicator (bool): set content table indicator to true/false
        """
        self._has_content_table = indicator

    def generate(self, writer: Writer) -> None:
        """
        Generate report
        Args:
            writer (Writer): report writer
        """
        writer.build(title=self.name, cover=self.cover,
                     detail=self.content,
                     content_table=self.has_content_table)
        writer.out()
