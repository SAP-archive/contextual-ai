#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Base """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import warnings
import json
from enum import Enum
from importlib import import_module
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from jsonschema import validate

from xai.exception import CompilerException
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
    SCHEMA = {
        "definitions": {
            "section": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "desc": {"type": "string"},
                    "sections":
                        {
                            "type": "array",
                            "items": {"$ref": "#/definitions/section"},
                            "default": []
                        },
                    "component": {"$ref": "#/definitions/component"}
                },
                "required": ["title"]
            },
            "component": {
                "type": "object",
                "properties": {
                    "package": {"type": "string"},
                    "module": {"type": "string"},
                    "class": {"type": "string"},
                    "attr": {
                        "type": "object"
                    }
                },
                "required": ["class"]
            }
        },

        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "overview": {" type": "boolean"},
            "content_table": {"type": "boolean"},
            "contents":
                {
                    "type": "array",
                    "items": {"$ref": "#/definitions/section"},
                    "default": []
                },
            "writers":
                {
                    "type": "array",
                    "items": {"$ref": "#/definitions/component"}
                }
        },
        "required": ["name", "content_table", "contents", "writers"]
    }

    @staticmethod
    def _load(config: Path) -> dict:
        """
        Load Config File

        Args:
            config (Path): config json/yaml file Path object
        Returns:
            configuration dict object
        """
        extension = config.suffix.lower()
        if extension == '.json':
            with open(config) as file:
                data = json.load(file)
        elif extension == '.yml':
            with open(config) as file:
                data = yaml.load(file, Loader=yaml.SafeLoader)
        else:
            raise CompilerException('Unsupported config file, %s' % config)

        validate(instance=data, schema=Configuration.SCHEMA)
        return data

    def __init__(self, config=None) -> None:
        """
        Configuration setup

        Args:
            config (str): config json/yaml file
        """
        self._config = dict()
        if not (config is None):
            self._config = self._load(Path(config))

    def __call__(self, config=None):
        """
        Configuration execution

        Args:
            config (str): config json/yaml file
        Returns:
            configuration dict object
        """
        if not (config is None):
            self._config = self._load(Path(config))
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
                                           contents=content[
                                               Constant.SECTION_LIST.value],
                                           level=current_level + 1)

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
    def factory(report: Report, package: str, module: str, name: str,
                attr: dict):
        """
        Dynamically import and load class

        Args:
            report (Report): report object
            package (str): component package
            module (str): component module name
            name (str): component class name
            attr (dict): component class attributes in dict
        Returns: class object
        """
        imported_module = import_module('.' + module, package=package)
        cls = getattr(imported_module, name)
        obj = cls(attr)
        obj(report=report)

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
            package = Controller.value_extractor(
                items=component, key=Constant.COMPONENT_PACKAGE.value,
                default='xai.compiler')
            module = Controller.value_extractor(
                items=component, key=Constant.COMPONENT_MODULE.value,
                default='components')
            attr = Controller.value_extractor(
                items=component, key=Constant.COMPONENT_ATTR.value,
                default=dict())
            Controller.factory(report=report, package=package,
                               module=module, name=name, attr=attr)
        else:
            raise CompilerException("class is not defined")

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
                package = Controller.value_extractor(
                    items=writer, key=Constant.COMPONENT_PACKAGE.value,
                    default='xai.compiler')
                module = Controller.value_extractor(
                    items=writer, key=Constant.COMPONENT_MODULE.value,
                    default='writer')
                attr = Controller.value_extractor(
                    items=writer, key=Constant.COMPONENT_ATTR.value,
                    default=dict())
                Controller.factory(report=report, package=package,
                                   module=module, name=name, attr=attr)
            else:
                raise CompilerException("class is not defined")

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

    def __init__(self, dictionary, *, schema):
        """
        Init

        Args:
            dictionary (dict): attribute to set
            schema (dict): schema to validate
        """
        self._dict = dictionary
        self._schema = schema

        validate(instance=self._dict, schema=self._schema)
        for key in self._dict:
            setattr(self, key, self._dict[key])

    def __call__(self, report: Report):
        """
        Call

        Args:
            report (Report): report object
        """
        pass

    def __repr__(self):
        """Return class name and attributes"""
        return "%s: schema[%s] data[%s]" % (self.__class__.__name__,
                                            self._schema,
                                            self.__dict__)

    def assert_attr(self, key: str, *, optional=False, default=None):
        """
        Assert and Get Attribute, raise Compiler exception if not found

        Args:
            key (str): Attribute Name
            optional (Optional): default is False, if set to true,
                        simple return None when attribute not found
            default (Optional): default value if not found

        Returns:
            attribute value
        """
        if hasattr(self, key):
            return getattr(self, key)
        if optional:
            return None
        if not (default is None):
            return default
        raise CompilerException("attribute '%s' is not defined" % key)

    @staticmethod
    def load_data(path: Path, *, header=True):
        """
        Load Data from file based on the file extension.
        This function is based on pandas and numpy tools, when the file is in a
        standard format. Various file types are supported (.npy, .csv, .json,
        .jsonl, .xls, .xlsx, .tsv, .pickle, .pick)

        Args:
            path (str): path to the data file
            header (bool): load data with header, default is True

        Returns:
            DataFrame / Numpy
        """
        extension = path.suffix.lower()
        if extension == '.npy':
            data = np.load(path)
        elif extension == ".json":
            data = pd.read_json(str(path))
        elif extension == ".jsonl":
            data = pd.read_json(str(path), lines=True)
        elif extension == ".tsv":
            data = pd.read_csv(str(path), sep="\t")
        elif extension in [".xls", ".xlsx"]:
            data = pd.read_excel(str(path))
        elif extension in [".pkl", ".pickle"]:
            data = pd.read_pickle(str(path))
        else:
            if extension != ".csv":
                warnings.warn(message="Warning! unsupported extension %s, "
                                      "we default it to be in CSV format." %
                              extension)
            if header:
                data = pd.read_csv(str(path))
            else:
                data = pd.read_csv(str(path), header=header)
        return data
