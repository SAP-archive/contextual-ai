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
    COMPONENT_ATTR_VARS_PREFIX = 'var:'
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
            "sections": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "desc": {"type": "string"},
                    "sections":
                        {
                            "type": "array",
                            "items": {"$ref": "#/definitions/sections"},
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
                    "items": {"$ref": "#/definitions/sections"},
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
            with open(str(config)) as file:
                data = json.load(file)
        elif extension == '.yml':
            with open(str(config)) as file:
                data = yaml.load(file, Loader=yaml.SafeLoader)
        else:
            raise CompilerException('Unsupported config file, %s' % config)

        validate(instance=data, schema=Configuration.SCHEMA)
        return data

    @staticmethod
    def render_config(contents: dict, variables: dict):
        """
        Rendering Config

        Args:
            contents (dict): contents dict object
            variables: dictionary of the current globals/locals symbol table
        """
        for content in contents:
            if Constant.COMPONENT.value in content:
                component = content[Constant.COMPONENT.value]
                if Constant.COMPONENT_ATTR.value in component:
                    attr = component[Constant.COMPONENT_ATTR.value]
                    for k, v in attr.items():
                        if isinstance(v, str) and \
                                Constant.COMPONENT_ATTR_VARS_PREFIX.value in v:
                            p, n = v.split(Constant.COMPONENT_ATTR_VARS_PREFIX.value, 1)
                            if n in variables:
                                attr[k] = variables[n]

            if Constant.SECTION_LIST.value in content:
                Configuration.render_config(
                    contents=content[Constant.SECTION_LIST.value],
                    variables=variables)

    @staticmethod
    def _load_config(config, variables: dict):
        """
        Load Config File - file path or dict

        Args:
            config (str/dict): path to config json/yaml file or dict pre-loaded
            variables: dictionary of the current globals/locals symbol table
        """
        _result = dict()
        if not (config is None):
            if type(config) == str:
                _result = Configuration._load(Path(config))
            elif type(config) == dict:
                _result = config
            else:
                raise CompilerException(
                    'Unsupported config format, %s' % config)

            # -- Start Rendering --
            if not (variables is None):
                Configuration.render_config(
                    contents=_result[Constant.CONTENT_LIST.value],
                    variables=variables)
        return _result

    def __init__(self, config=None, variables: dict = None) -> None:
        """
        Configuration setup

        Args:
            config (str/dict): path to config json/yaml file or dict pre-loaded
            variables: dictionary of the current globals/locals symbol table
        """
        self._config = Configuration._load_config(config, variables)

    def __call__(self, config=None, variables: dict = None):
        """
        Configuration execution

        Args:
            config (str/dict): path to config json/yaml file or dict pre-loaded
            variables: dictionary of the current globals/locals symbol table
        Returns:
            configuration dict object
        """
        if not (config is None):
            self._config = Configuration._load_config(config, variables)
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
        self._config = config()

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
                Controller.render_component(report=report,
                                            component=component,
                                            level=current_level)
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
                attr: dict, level=None):
        """
        Dynamically import and load class

        Args:
            report (Report): report object
            package (str): component package
            module (str): component module name
            name (str): component class name
            attr (dict): component class attributes in dict
            level (int): content level
        Returns: class object
        """
        imported_module = import_module('.' + module, package=package)
        cls = getattr(imported_module, name)
        obj = cls(attr)
        obj(report=report, level=level)

    @staticmethod
    def render_component(report: Report, component: dict, level: int):
        """
        Rendering Report component

        Args:
            report (Report): report object
            component (dict): component info in dict
            level (int): content level
        """
        if Constant.COMPONENT_CLASS.value in component:
            name = component[Constant.COMPONENT_CLASS.value]
            package = Controller.value_extractor(
                items=component, key=Constant.COMPONENT_PACKAGE.value,
                default='xai')
            module = Controller.value_extractor(
                items=component, key=Constant.COMPONENT_MODULE.value,
                default='compiler')
            attr = Controller.value_extractor(
                items=component, key=Constant.COMPONENT_ATTR.value,
                default=dict())
            Controller.factory(report=report, package=package,
                               module=module, name=name, attr=attr,
                               level=level)
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
                    default='xai')
                module = Controller.value_extractor(
                    items=writer, key=Constant.COMPONENT_MODULE.value,
                    default='compiler')
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

        # validate(instance=self._dict, schema=self._schema)
        for key in self._dict:
            setattr(self, key, self._dict[key])

    def __call__(self, report: Report, level: int):
        """
        Call

        Args:
            report (Report): report object
            level (int): content level
        """
        self._report = report
        self._level = level

    @property
    def report(self):
        """Returns Report object."""
        return self._report

    @property
    def level(self):
        """Returns Report section level."""
        return self._level

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

    def add_header(self, text: str):
        if not (text is None):
            if self.level == Constant.S1.value:
                self.report.detail.add_header_level_1(text=text)
            elif self.level == Constant.H1.value:
                self.report.detail.add_header_level_2(text=text)
            elif self.level == Constant.H2.value:
                self.report.detail.add_header_level_3(text=text)
            else:
                self.report.detail.add_paragraph(text=text)

    @staticmethod
    def load_data(input, *, header=True):
        """
        Load Data from variable or file based on the file extension.
        This function is based on pandas and numpy tools, when the file is in a
        standard format. Various file types are supported (.npy, .csv, .json,
        .jsonl, .xls, .xlsx, .tsv, .pickle, .pick)

        Args:
            input: vars to the data file
            header (bool): load data with header, default is True

        Returns:
            Object
        """
        if type(input) != str:
            return input

        # -- Parse/read if the input is a str --
        path = Path(input)
        extension = path.suffix.lower()
        if extension == '.npy':
            data = np.load(path)
        elif extension == ".json":
            data = pd.read_json(str(path))
        elif extension == ".jsonl":
            data = pd.read_json(str(path), lines=True)
        elif extension == ".dta":
            data = pd.read_stata(str(path))
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
                data = pd.read_csv(str(path), header=None)
        return data
