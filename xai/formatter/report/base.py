#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Report Object """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from xai.formatter.report.section import (
    OverviewSection,
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

        Args:
            name(str): the report name
        """
        self._name = name

        self._writer = None
        self._overview_section = OverviewSection()
        self._detail_section = DetailSection()
        self._has_content_table = True # default having content table

    @property
    def name(self):
        """Returns report name."""
        return self._name

    @property
    def overview(self):
        """Returns overview section."""
        return self._overview_section

    @property
    def detail(self):
        """Returns detail section."""
        return self._detail_section

    @property
    def has_content_table(self):
        """Check if content table enabled."""
        return self._has_content_table

    def set_content_table(self, indicator):
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
        writer.build(title=self.name, overview=self.overview,
                     detail=self.detail,
                     content_table=self.has_content_table)
        writer.out()
