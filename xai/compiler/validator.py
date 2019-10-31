#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Explainer """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from pathlib import Path

import itertools
from collections import Counter
from xai.compiler.base import Dict2Obj
from xai.data.validator.dataframe_validator import DataframeValidator
from xai.formatter import Report


################################################################################
### DuplicationOrphanCheck
################################################################################
class DuplicationOrphanCheck(Dict2Obj):
    """
    Compiler for Duplication Orphan Check

    Param:
        package (str, Optional): component package name
        module (str, Optional): component module name
        class (str): component class name

    Attr:
        data (str): path to dataframe file
        duplication_key (list): a list of column names that data frame is checking duplications on.
                                Default is None and duplication is checking on all columns
        orphan_rules (list of dict): a list of dict object, which of each object is a rule and has following keys:
                                    - local_key (str): column name in current data frame
                                    - foreign_data (str): foreign file path
                                    - foreign_key (str): column name in the foreign file

    Example:
        "component": {
            "package": "xai",
            "module": "compiler",
            "class": "DuplicationOrphanCheck",
            "attr": {
              "data": "./student.csv",
              "duplication_keys": ["STUDENT_ID"],
              "orphan_rules": [
                {
                  "local_key": "STUDENT_ID",
                  "foreign_data": "./course.csv",
                  "foreign_key": "STUDENT_ID"
                }
              ]
            }
          }
    """
    schema = {
        "definitions": {
            "rule": {
                "type": "object",
                "properties": {
                    "local_key": {"type": "string"},
                    "foreign_data": {"type": "string"},
                    "foreign_key": {"type": "string"},
                },
                "required": ["local_key", "foreign_data", "foreign_key"]
            }
        },
        "type": "object",
        "properties": {
            "data": {"type": "string"},
            "duplication_keys": {"type": "array", "items": {"type": "string"}},
            "orphan_rules": {"type": "array", "items": {"$ref": "#/definitions/rule"}},

        },
        "required": ["data"]
    }

    def __init__(self, dictionary):
        """
        Init

        Args:
            dictionary (dict): attribute to set
        """
        super(DuplicationOrphanCheck, self).__init__(dictionary,
                                                     schema=self.schema)

    def __call__(self, report: Report, level: int):
        """
        Execution

        Args:
            report (Report): report object
            level (int): content level
        """
        super(DuplicationOrphanCheck, self).__call__(report=report,
                                                     level=level)
        # -- Load Parameters --
        data_path = self.assert_attr(key='data')
        duplication_keys = self.assert_attr(key='duplication_keys', default=None)
        orphan_rules = self.assert_attr(key='orphan_rules')

        df = None
        # -- Load Data --
        if not (data_path is None):
            df = self.load_data(Path(data_path), header=True)

        # -- Information about Raw Dataframe --
        self.report.detail.add_model_info_summary([('Total number of raw samples', df.shape[0])],
                                                  notes='Raw Data Quantity')

        # -- Initialize DataframeValidator --
        dv_processor = DataframeValidator()

        # -- Duplication Check about Raw Dataframe --

        duplicated_indices = dv_processor.duplication_check(df, duplication_keys)
        drop_indices = itertools.chain.from_iterable([l[1:] for l in duplicated_indices])

        self.report.detail.add_model_info_summary(
            [('Total number of samples after duplication check on %s' % (
                duplication_keys if duplication_keys is not None else "all columns"),
              df.shape[0] - len(list(drop_indices)))],
            notes='Duplication Check')

        # -- Orphan Relation Check about Duplicated Data --
        duplicate_dropped_df = df.drop(index=drop_indices)
        orphan_check_info = []
        for rule in orphan_rules:
            local_key = rule['local_key']
            foreign_path = rule['foreign_data']
            foreign_key = rule['foreign_key']

            foreign_df = None
            if not (foreign_path is None):
                foreign_df = self.load_data(Path(foreign_path), header=True)

            bool_list = dv_processor.orphaned_relation_check(df_a=duplicate_dropped_df,
                                                             df_b=foreign_df,
                                                             col_a=local_key,
                                                             col_b=foreign_key)
            bool_counter = Counter(bool_list)
            orphan_check_info.append(("[%s] not in [%s of %s]" % (local_key, foreign_key, foreign_path),
                                      bool_counter[False]))

        if len(orphan_check_info) > 0:
            self.report.detail.add_model_info_summary(model_info=orphan_check_info, notes='Orphaned Relation Check')
