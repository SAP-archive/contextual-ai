#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Data """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path

from xai.compiler.base import Dict2Obj
from xai.data import DataUtil
from xai.data.constants import DATATYPE
from xai.formatter import Report


################################################################################
### Data Statistics Analysis
################################################################################
class DataStatisticsAnalysis(Dict2Obj):
    """
     Compiler for Data Statistics Analysis

     Param:
         package (str, Optional): component package name
         module (str, Optional): component module name
         class (str): component class name

     Attr:
         data (str): path to training sample data
         metadata (str, Optional): path to training metadata data,
                Optional, more details statistics can be generate, if provided
         label (str, Optional): label column name
         threshold (number, Optional): data threshold, default 0.3

     Example:
         "component": {
             "package": "xai",
             "module": "compiler",
             "class": "DataExplorer",
             "attr": {
                 "data": "./sample_input/data.csv",
                 "metadata": "./sample_input/metadata.json",
                 "label": "Winner"
                 "threshold": 0.3
             }
         }
     """
    schema = {
        "type": "object",
        "properties": {
            "data": {" type": "string"},
            "label": {"type": "string"},
            "threshold": {
                "type": "number",
                "default": 0.3
            }
        },
        "required": ["data"]
    }

    def __init__(self, dictionary):
        """
        Init

        Args:
            dictionary (dict): attribute to set
        """
        super(DataStatisticsAnalysis, self).__init__(dictionary, schema=self.schema)

    def __call__(self, report: Report, level: int):
        """
        Execution

        Args:
            report (Report): report object
            level (int): content level
        """
        super(DataStatisticsAnalysis, self).__call__(report=report,
                                                     level=level)
        threshold = self.assert_attr(key='threshold', default=0.3)
        # -- Load Data --
        data_path = self.assert_attr(key='data')
        data = self.load_data(Path(data_path))
        # -- Load Metadata --
        metadata_path = self.assert_attr(key='metadata', optional=True)
        metadata = None
        if not (metadata_path is None):
            metadata = self.load_data(Path(metadata_path))
        # -- Label --
        label = self.assert_attr(key='label', optional=True)

        if metadata is None:
            # -- Get default data types --
            feature, valid_feature_names, valid_feature_types, metadata = \
                DataUtil.get_column_types(data=data, threshold=threshold,
                                          label=label)
        ### Get Data Stats
        # TODO: where to get feature names and type when metadata provided

        stats = DataUtil.get_data_statistics(data=data,
                                             feature_names=valid_feature_names,
                                             feature_types=valid_feature_types,
                                             label=label)

        # -- Add Data Label Distribution --
        if not (label is None):
            self.add_header(text='Data Class (Label) Distribution')
            label_distributions = DataUtil.get_label_distribution(data=data,
                                                                  label=label)
            report.detail.add_data_set_distribution(label_distributions)

        # -- Add Data Field Attribute --
        if not (metadata is None):
            self.add_header(text='Data Field Attribute')
            report.detail.add_data_attributes(metadata)

        # -- Add Missing Value Count --
        self.add_header(text='Data Missing Value Check')
        missing_count, total_count = \
            DataUtil.get_missing_value_count(data=data,
                                             feature_names=valid_feature_names,
                                             feature_types=valid_feature_types)
        report.detail.add_data_missing_value(missing_count=dict(missing_count),
                                             total_count=total_count)

        # -- Add Categorical Field Distribution --
        if len(feature[DATATYPE.CATEGORY]) > 0:
            self.add_header(text='Categorical Field Distribution')
            for field_name in feature[DATATYPE.CATEGORY]:
                labelled_stats, all_stats = stats[field_name]
                report.detail.add_categorical_field_distribution(
                    field_name=field_name,
                    field_distribution=labelled_stats)

        # -- Add Numerical Field Distribution --
        if len(feature[DATATYPE.NUMBER]) > 0:
            self.add_header(text='Numerical Field Distribution')
            for field_name in feature[DATATYPE.NUMBER]:
                labelled_stats, all_stats = stats[field_name]
                report.detail.add_numeric_field_distribution(
                    field_name=field_name,
                    field_distribution=labelled_stats)

        # -- Add Text Field Distribution --
        if len(feature[DATATYPE.FREETEXT]) > 0:
            self.add_header(text='Text Field Distribution')
            for field_name in feature[DATATYPE.FREETEXT]:
                labelled_stats, all_stats = stats[field_name]
                report.detail.add_text_field_distribution(
                    field_name=field_name,
                    field_distribution=labelled_stats)

        # -- Add Datetime Field Distribution --
        if len(feature[DATATYPE.DATETIME]) > 0:
            self.add_header(text='Datetime Field Distribution')
            for field_name in feature[DATATYPE.DATETIME]:
                labelled_stats, all_stats = stats[field_name]
                report.detail.add_datetime_field_distribution(
                    field_name=field_name,
                    field_distribution=labelled_stats)
