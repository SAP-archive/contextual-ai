#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Base """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from importlib import import_module
import json
import yaml
from enum import Enum

from xai.exception import GeneralException
from xai.formatter import Report


################################################################################
### Report Enum Constant
################################################################################
class Constant(Enum):

    NAME = 'name'
    ENABLE_OVERVIEW = 'overview'
    ENABLE_CONTENT_TABLE = 'content_table'

    CONTENT_LIST = 'contents'
    SECTION_TITLE = 'title'
    SECTION_DESC = 'desc'
    COMPONENT = 'component'
    COMPONENT_CLASS = 'class'
    COMPONENT_PACKAGE = 'package'
    COMPONENT_MODULE = 'module'
    COMPONENT_ATTR = 'attr'
    SECTION_LIST = 'sections'

    S1 = 0
    H1 = 1
    H2 = 2
    H3 = 3

    PATH = 'path'
    WRITERS = 'writers'


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
            if Constant.COMPONENT.value in content:
                component = content[Constant.COMPONENT.value]
                Controller.render_component(report=report, component=component)
            if Constant.SECTION_LIST.value in content:
                Controller.render_contents(report=report,
                                           contents=content[Constant.SECTION_LIST.value],
                                           level=current_level+1)

    @staticmethod
    def value_extractor(items, key, default):
        """
        Extract value with key, return default if not found

        Args:
            items: items
            key (str): key
            default: default return
        Returns: default
        """
        if key in items:
            return items[key]
        return default

    @staticmethod
    def factory(package: str, module: str, name: str, attr: dict):
        """
        Dynamically import and load class

        Args:
            package (str): component package
            module (str): component module name
            name (str): component class name
            attr (dict): component class attributes in dict
        Returns: class object
        """
        imported_module = import_module('.' + module, package=package)
        cls = getattr(imported_module, name)
        return cls(attr)

    @staticmethod
    def render_component(report: Report, component: dict):
        """
        Rendering Report component

        Args:
            report (Report): report object
            component (dict): component info in dict
        """
        if Constant.COMPONENT_CLASS.value in component:
            name = component[Constant.COMPONENT_CLASS.value]
            package = Controller.value_extractor(items=component,
                                                 key=Constant.COMPONENT_PACKAGE.value,
                                                 default='xai.compiler')
            module = Controller.value_extractor(items=component,
                                                key=Constant.COMPONENT_MODULE.value,
                                                default='components')
            attr = Controller.value_extractor(items=component,
                                              key=Constant.COMPONENT_ATTR.value,
                                              default=dict())
            obj = Controller.factory(package=package, module=module,
                                     name=name, attr=attr)
            print(obj)
            print("color %s" % obj.color)
            obj.exec()
        else:
            raise GeneralException("class is not defined")


    @staticmethod
    def output(report: Report, writers: dict):
        """
        Rendering Report to writer

        Args:
            report (Report): report object
            writers (dict): output writer dict object
        """
        for writer in writers:
            if Constant.COMPONENT_CLASS.value in writer:
                name = writer[Constant.COMPONENT_CLASS.value]
                package = Controller.value_extractor(items=writer,
                                                     key=Constant.COMPONENT_PACKAGE.value,
                                                     default='xai.compiler')
                module = Controller.value_extractor(items=writer,
                                                    key=Constant.COMPONENT_MODULE.value,
                                                    default='writer')
                attr = Controller.value_extractor(items=writer,
                                                  key=Constant.COMPONENT_ATTR.value,
                                                  default=dict())
                obj = Controller.factory(package=package, module=module,
                                         name=name, attr=attr)
                report.generate(writer=obj.exec())
            else:
                raise GeneralException("class is not defined")

    def render(self):
        """Render Report"""
        report = Report(name=self.config[Constant.NAME.value])
        report.set_content_table(indicator=self.config[
            Constant.ENABLE_CONTENT_TABLE.value])

        self.render_contents(report=report,
                             contents=self.config[Constant.CONTENT_LIST.value],
                             level=Constant.S1.value)
        self.output(report=report, writers=self.config[Constant.WRITERS.value])

################################################################################
### Dict to Object
################################################################################
class Dict2Obj:

    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __repr__(self):
        """"""
        return "<Dict2Obj: %s>" % self.__dict__