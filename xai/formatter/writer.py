#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Abstract Writer """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import ABC, abstractmethod

from typing import Tuple, Dict, List

from xai.formatter.section import CoverSection, DetailSection

################################################################################
### Writer Strategy
################################################################################
class Writer(ABC):
    """
    The Strategy interface declares operations common to all
    supported report output.
    """
    def __init__(self, *values) -> None:
        """
        Abstract Writer
        """
        self._values = values

    @property
    def values(self):
        """Returns keyword-ed variable."""
        return self._values

    def __str__(self):
        return 'Writer:(' + str(self.values) + ')'

    @abstractmethod
    def out(self):
        """
        Output Report
        """
        pass

    @abstractmethod
    def set_report_title(self, title: str):
        """
        Add new page
        Args:
            title(str): header title
        """
        pass

    @abstractmethod
    def build_cover_section(self, section: CoverSection):
        """
        Build Cover Section
        Args:
            section(CoverSection): Cover Section of report
        """
        pass

    @abstractmethod
    def build_content_section(self, section: DetailSection,
                              content_table=False):
        """
        Build Details Section
        Args:
            section(DetailSection): Details Section of report
            content_table (bool): is content table enabled
                            default False
        """
        pass

    @abstractmethod
    def add_new_page(self):
        """
        Add new page
        """
        pass

    @abstractmethod
    def draw_header(self, text: str, level: int, link=None):
        """
        Draw Header
        Args:
            text(str): header text in the report
            level(int): header level
            link: header link
        """
        pass

    @abstractmethod
    def draw_title(self, text: str, level: int, link=None):
        """
        Draw Title
        Args:
            text(str): title in the report
            level(int): title type (section or paragraph)
            link: title link
        """
        pass

    @abstractmethod
    def draw_paragraph(self, text: str):
        """
        Draw Paragraph
        Args:
            text(str): html text to render in the report
        """
        pass

    @abstractmethod
    def draw_data_missing_value(self, notes: str, missing_count: dict,
                                total_count: dict, ratio=False):
        """
        Draw Missing Data Value Summary Table
        Args:
            notes(str): Explain the block
            missing_count(dict): Missing Count
            total_count(dict): Total Count
            ratio(bool): True if `missing_value` is the percentage
        """
        pass

    @abstractmethod
    def draw_data_set_distribution(self, notes: str,
                                  data_set_distribution: Tuple[str, dict],
                                  max_class_shown=20):
        """
        Draw information of distribution on data set
        Args:
            notes(str): Explain the block
            data_set_distribution (tuple: (str,dict)):
                - tuple[0] str: label/split name
                - tuple[1] dict: key - class_name/split_name,
                                 value - class_count/split_count
            max_class_shown (int, Optional): maximum number of classes shown
                          in the figure, default is 20
            notes (str, Optional):
                explain the block
        """
        pass