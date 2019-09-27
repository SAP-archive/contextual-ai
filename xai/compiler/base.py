#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Proxy - Base """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import yaml
from enum import Enum

from xai.formatter import Report, PdfWriter, HtmlWriter


################################################################################
### Report Enum Constant
################################################################################
class Constant(Enum):

    NAME = 'name'
    ENABLE_OVERVIEW = 'overview'
    ENABLE_CONTENT_TABLE = 'content_table'

    CONTENTS = 'contents'
    SECTION_TITLE = 'title'
    SECTION_DESC = 'desc'
    SECTION_FUNCTION = 'function'
    SECTIONS = 'sections'

    S1 = 0
    H1 = 1
    H2 = 2
    H3 = 3

    OUTPUT = 'output'
    PATH = 'path'
    WRITERS = 'writers'

    PDF = 'pdf'
    HTML = 'html'




################################################################################
### Configuration
################################################################################
class Configuration:

    @staticmethod
    def _load(config: str) -> dict:
        """
        Load Config File

        Args:
            config (str): config json/yaml file
        Returns:
            configuration dict object
        """
        if config.lower().endswith('.json'):
            with open(config) as file:
                data = json.load(file)
            return data
        elif config.lower().endswith('.yml'):
            with open(config) as file:
                data = yaml.load(file, Loader=yaml.SafeLoader)
            return data

    def __init__(self, config=None) -> None:
        """
        Configuration setup

        Args:
            config (str): config json/yaml file
        """
        self._config = dict()
        if not (config is None):
            self._config = self._load(config)

    def __call__(self, config=None):
        """
        Configuration execution

        Args:
            config (str): config json/yaml file
        Returns:
            configuration dict object
        """
        if not (config is None):
            self._config = self._load(config)
        return self._config

################################################################################
### Controller
################################################################################
class Controller:

    def __init__(self, config=None):
        """
        Controller setup

        Args:
            config (Configuration): configuration dict object
        """
        self._config = config

    @property
    def config(self):
        """Returns Configuration Object"""
        return self._config

    @staticmethod
    def render_contents(report: Report, contents: dict, level: int):
        """
        Rendering Content

        Args:
            report (Report): report object
            contents (dict): contents dict object
            level (int): content level
        """
        current_level = level
        for content in contents:
            if Constant.SECTION_TITLE.value in content:
                title = content[Constant.SECTION_TITLE.value]
                if not (title is None):
                    if current_level == Constant.S1.value:
                        report.detail.add_new_page()
                        report.detail.add_section_title(text=title)
                    elif current_level == Constant.H1.value:
                        report.detail.add_header_level_1(text=title)
                    elif current_level == Constant.H2.value:
                        report.detail.add_header_level_2(text=title)
                    else:
                        report.detail.add_header_level_3(text=title)
            if Constant.SECTION_DESC.value in content:
                desc = content[Constant.SECTION_DESC.value]
                if not (desc is None):
                    report.detail.add_paragraph(text=desc)
            if Constant.SECTIONS.value in content:
                Controller.render_contents(report=report,
                                           contents=content[Constant.SECTIONS.value],
                                           level=current_level+1)

    @staticmethod
    def output(report: Report, output: dict):
        """
        Rendering Report to writer

        Args:
            report (Report): report object
            output (dict): output dict object
        """
        name = output[Constant.NAME.value]
        path = output[Constant.PATH.value]
        for writer in output[Constant.WRITERS.value]:
            if writer.lower() == Constant.PDF.value:
                report.generate(writer=PdfWriter(name=name, path=path))
            if writer.lower() == Constant.HTML.value:
                report.generate(writer=HtmlWriter(name=name, path=path))

    def render(self):
        """Render Report"""
        report = Report(name=self.config[Constant.NAME.value])
        report.set_content_table(indicator=self.config[
            Constant.ENABLE_CONTENT_TABLE.value])

        self.render_contents(report=report,
                             contents=self.config[Constant.CONTENTS.value],
                             level=Constant.S1.value)
        self.output(report=report, output=self.config[Constant.OUTPUT.value])
