#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""Report Section - Base"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Tuple, Dict, List

################################################################################
### Section Strategy
################################################################################
class Section:

    COVER = 10
    CONTENT_TABLE = 20
    DETAIL = 30

    def __init__(self, type: int, contents=None):
        """
        Report Section
        Args:
            type (int): Section Type (cover, detail)
            contents(list) Content List
        """
        self._type = type
        self._contents = contents

    @property
    def type(self):
        """Returns section type."""
        return self._type

    @property
    def contents(self) -> list:
        """Returns section content list."""
        return self._contents


    ##########################################################################
    ###  Content Object add below
    ##########################################################################

    def add_new_page(self):
        """
        add a new page
        :return:
        """
        from xai.formatter.content import NewPage
        self.contents.append(NewPage())

    def add_header_level_1(self, text: str):
        """
        add a header level 1 into the section
        Args:
            text(str): header level 1 in the report
        """
        from xai.formatter.content import Header
        self._contents.append(Header(text=text, level=Header.LEVEL_1))

    def add_header_level_2(self, text: str):
        """
        add a header level 2 into the section
        Args:
            text(str): header level 2 in the report
        """
        from xai.formatter.content import Header
        self._contents.append(Header(text=text, level=Header.LEVEL_2))

    def add_header_level_3(self, text: str):
        """
        add a header level 3 into the section
        Args:
            text(str): header level 3 in the report
        """
        from xai.formatter.content import Header
        self._contents.append(Header(text=text, level=Header.LEVEL_3))

    def add_section_title(self, text: str):
        """
        add a title into the section
        Args:
            text(str): title in the report
        """
        from xai.formatter.content import SectionTitle
        self.contents.append(SectionTitle(text=text))

    def add_paragraph_title(self, text: str):
        """
        add a title into the paragraph
        Args:
            text(str): title in the report
        """
        from xai.formatter.content import ParagraphTitle
        self._contents.append(ParagraphTitle(text=text))

    def add_paragraph(self, text: str):
        """
        add a paragraph into the section
        Args:
            text(str): html text to render in the report
        """
        from xai.formatter.content import Paragraph
        self.contents.append(Paragraph(text=text))

    def add_data_missing_value(self, missing_count: dict,
                               total_count: list, ratio=False, notes=None):
        """
        add information of missing value for data fields to the report
        Args:
            missing_count (dict):
                - key: data field name
                - value: the count or the percentage of missing value in the field
            total_count (dict, Optinal):
                - key: data field name
                - value: the count of missing value in the field
            ratio (bool): True if `missing_value` is the percentage
            notes (str, Optional):
                explain the block
        """
        from xai.formatter.content import DataMissingValue
        self._contents.append(DataMissingValue(missing_count=missing_count,
                                               total_count=total_count,
                                               ratio=ratio, notes=notes))

    def add_data_set_distribution(self, dataset_distribution: Tuple[str, dict],
                                  max_class_shown=20, notes=None):
        """
        add information of distribution on data set to the report
        Args:
            dataset_distribution (tuple: (str,dict)):
                - tuple[0] str: label/split name
                - tuple[1] dict: key - class_name/split_name,
                                 value - class_count/split_count
            max_class_shown (int, Optional): maximum number of classes shown
            in the figure, default is 20
            notes (str, Optional):
                explain the block
        """
        from xai.formatter.content import DataSetDistribution
        self._contents.append(DataSetDistribution(
            dataset_distribution=dataset_distribution,
            max_class_shown=max_class_shown, notes=notes))

################################################################################
###  Cover Section
################################################################################
class CoverSection(Section):
    """
    Cover Section
    """

    def __init__(self) -> None:
        """
        Cover Section
        """
        from xai.formatter.content import NewPage
        contents = list()
        contents.append(NewPage())
        super(CoverSection, self).__init__(type=Section.COVER,
                                           contents=contents)

################################################################################
###  Detail Section
################################################################################
class DetailSection(Section):
    """
    Details Section
    """

    def __init__(self) -> None:
        """
        Details Section
        """
        from xai.formatter.content import NewPage
        contents = list()
        contents.append(NewPage())
        super(DetailSection, self).__init__(type=Section.DETAIL,
                                            contents=contents)