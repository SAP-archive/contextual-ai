#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Content Skeleton """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import ABC, abstractmethod

from xai.formatter.writer.base import Writer


################################################################################
### Report Content
################################################################################
class Content(ABC):

    """
    The Implementation defines the interface for all implementation classes.
    """
    def __init__(self, *values) -> None:
        """
        Abstract Content
        """
        self._values = values
        self._link = None

    @property
    def link(self):
        """Returns content link."""
        return self._link

    @link.setter
    def link(self, link):
        """Set content link"""
        self._link = link

    @property
    def values(self):
        """Returns keyword-ed variable."""
        return self._values

    def __str__(self):
        return 'Content:(' + str(self.values) + ')'

    @abstractmethod
    def draw(self, writer: Writer):
        """
        Draw Contents

        Args:
            writer (Writer): Report Writer
        """
        pass

################################################################################
###  New Page
################################################################################
class NewPage(Content):

    def __init__(self) -> None:
        """
        add a new page
        """
        super(NewPage, self).__init__()

    def draw(self, writer: Writer):
        """
        Draw Header

        Args:
            writer (Writer): Report Writer
        """
        writer.add_new_page()

################################################################################
###  Header Content
################################################################################
class Header(Content):
    """
    Header
    """
    # Header Level
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 4

    def __init__(self, text: str, level: int) -> None:
        """
        add a header into the report

        Args:
            text(str): header text in the report
            level(int): header level
        """
        super(Header, self).__init__(text, level)
        self._text = text
        self._level = level

    @property
    def text(self):
        """Returns header text."""
        return self._text

    @text.setter
    def text(self, text):
        """Set header text"""
        self._text = text

    @property
    def level(self):
        """Returns header level."""
        return self._level

    def draw_content_table(self, writer):
        """
        Draw Content Table

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_header(text=self.text, level=self.level, link=self.link)

    def draw(self, writer: Writer):
        """
        Draw Header

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_header(text=self.text, level=self.level, link=self.link)


################################################################################
###  Title Content
################################################################################
class Title(Content):
    """
    Title Content
    """
    # Title Type
    SECTION_TITLE = 1
    PARAGRAPH_TITLE = 2

    def __init__(self, text: str, level: int) -> None:
        """
        add a title into the report

        Args:
            text(str): title text in the report
            level(int): title type (section or paragraph)
        """
        super(Title, self).__init__(text, level)
        self._text = text
        self._level = level

    @property
    def text(self):
        """Returns title text."""
        return self._text

    @text.setter
    def text(self, text):
        """Set title text"""
        self._text = text

    @property
    def level(self):
        """Returns title type level."""
        return self._level

    def draw(self, writer: Writer):
        """
        Draw Title

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_title(text=self.text, level=self.level, link=self.link)


class SectionTitle(Title):
    """
    Section Title
    """
    def __init__(self, text: str) -> None:
        """
        add a section level title into the report

        Args:
            text(str): title text in the report
        """
        super(SectionTitle, self).__init__(text=text,
                                           level=Title.SECTION_TITLE)

class ParagraphTitle(Title):
    """
    Paragraph Title
    """
    def __init__(self, text: str) -> None:
        """
        add a paragraph level title into the report

        Args:
            text(str): title text in the report
        """
        super(ParagraphTitle, self).__init__(text=text,
                                           level=Title.PARAGRAPH_TITLE)

################################################################################
###  Paragraph Content
################################################################################
class Paragraph(Content):
    """
    Paragraph Content
    """

    def __init__(self, text=None) -> None:
        """
        add a paragraph into the report

        Args:
            text(str): html text to render in the report
        """
        super(Paragraph, self).__init__(text)
        self._text = text

    @property
    def text(self):
        """Returns paragraph text."""
        return self._text

    def draw(self, writer: Writer):
        """
        Draw Paragraph
        Args:
            writer (Writer): Report Writer
        """
        writer.draw_paragraph(text=self.text)
