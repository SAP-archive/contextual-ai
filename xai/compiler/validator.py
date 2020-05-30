#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Compiler - Explainer """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import itertools
from collections import defaultdict
from copy import deepcopy

from xai.compiler.base import Dict2Obj
from xai.data.constants import DATATYPE
from xai.data.exceptions import AnalyzerDataTypeNotSupported
from xai.data.explorer import CategoricalDataAnalyzer, NumericDataAnalyzer, \
    TextDataAnalyzer, DatetimeDataAnalyzer
from xai.data.explorer import CategoricalStats, NumericalStats, TextStats, \
    DatetimeStats
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
        duplication_rule (dict): a dict which represents the rule, of which there are following keys:
                                - keys (list of str): the list of columns that the duplication is checked on.
                                                 Default is None and duplication is checking on all columns.
                                - to_file (str): the filepath that duplicate-removed dataframe dumps to.
                                                 Default is None and no save back,
        orphan_rules (dict): a dict which represents the rule, of which there are following keys:
                                - rules: a list of dict object, which of each object is a rule and has following keys:
                                        - local_key (str): column name in current data frame
                                        - foreign_data (str): foreign file path
                                        - foreign_key (str): column name in the foreign file
                                - to_file (str): filepath to dump the orphan-droped data frame.
                                                 Default is None and no save back.

    Example:
        "component": {
            "package": "xai",
            "module": "compiler",
            "class": "DuplicationOrphanCheck",
            "attr": {
              "data": "./student.csv",
              "duplication_rule": {
                "keys": [
                  "STUDENT_ID"
                ],
                "to_file": "./data/drop_student.csv"
              },
              "orphan_rules": {
                  "rules":[
                    {
                      "local_key": "STUDENT_ID",
                      "foreign_data": "./course.csv",
                      "foreign_key": "STUDENT_ID"
                    }
                  ],
                  "to_file": "./data/drop_student_2.csv"
              }
            }
          }
    """
    schema = {
        "definitions": {
            "orphan_rule": {
                "type": "object",
                "properties": {
                    "local_key": {"type": "string"},
                    "foreign_data": {"type": ["string", "object"]},
                    "foreign_key": {"type": "string"},
                },
                "required": ["local_key", "foreign_data", "foreign_key"]
            }
        },
        "type": "object",
        "properties": {
            "data": {"type": ["string", "object"]},
            "duplication_rule": {
                "type": "object",
                "properties": {
                    "keys": {
                        "type": "array",
                        "items": {"type": "string"},
                        "default": None
                    },
                    "to_file": {
                        "type": "string",
                        "default": None
                    },
                }
            },
            "orphan_rules": {
                "type": "object",
                "properties": {
                    "rules": {
                        "type": "array",
                        "items": {
                            "$ref": "#/definitions/orphan_rule"
                        }
                    },
                    "to_file": {
                        "type": "string",
                        "default": None}
                }
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
        data_var = self.assert_attr(key='data')
        duplication_rule = self.assert_attr(key='duplication_rule', default=None)
        orphan_rules = self.assert_attr(key='orphan_rules')

        df = None
        # -- Load Data --
        if not (data_var is None):
            df = self.load_data(data_var, header=True)

        # -- Information about Raw Dataframe --
        self.report.detail.add_key_value_pairs(info_list=[('Total number of raw samples', df.shape[0])],
                                               notes='Raw Data Quantity')

        # -- Initialize DataframeValidator --
        dv_processor = DataframeValidator()

        # -- Duplication Check about Raw Dataframe --
        if 'keys' in duplication_rule:
            duplication_keys = duplication_rule['keys']
        else:
            duplication_keys = None
        if 'to_file' in duplication_rule:
            duplication_to_file = duplication_rule['to_file']
        else:
            duplication_to_file = None

        duplicated_indices = dv_processor.duplication_check(df, duplication_keys)
        drop_indices = list(itertools.chain.from_iterable([l[1:] for l in duplicated_indices]))

        self.report.detail.add_key_value_pairs(info_list=[('Total number of samples after duplication check on %s' % (
            duplication_keys if duplication_keys is not None else "all columns"),
                                                           df.shape[0] - len(drop_indices))],
                                               notes='Duplication Check')
        duplicate_dropped_df = df.drop(index=drop_indices)

        if duplication_to_file is not None:
            duplicate_dropped_df.to_csv(duplication_to_file)

        # -- Orphan Relation Check about Duplicated Data --
        orphan_check_info = []
        if "rules" in orphan_rules:
            rules = orphan_rules["rules"]
        else:
            rules = []

        if "to_file" in orphan_rules:
            orphan_to_filepath = orphan_rules["to_file"]
        else:
            orphan_to_filepath = None

        all_orphaned_index = set()

        for rule in rules:
            local_key = rule['local_key']
            foreign_var = rule['foreign_data']
            foreign_key = rule['foreign_key']

            foreign_df = None
            if not (foreign_var is None):
                foreign_df = self.load_data(foreign_var, header=True)

            orphan_indices = dv_processor.orphaned_relation_check(df_a=duplicate_dropped_df,
                                                                  df_b=foreign_df,
                                                                  col_a=local_key,
                                                                  col_b=foreign_key)

            all_orphaned_index.update(set(orphan_indices))

            orphan_check_info.append(("[%s] not in [%s of %s]" % (local_key, foreign_key, foreign_var),
                                      len(orphan_indices)))

        if len(orphan_check_info) > 0:
            self.report.detail.add_key_value_pairs(info_list=orphan_check_info, notes='Orphaned Relation Check')

        orphan_dropped_df = duplicate_dropped_df.drop(index=list(all_orphaned_index))

        if orphan_to_filepath is not None:
            orphan_dropped_df.to_csv(orphan_to_filepath)


################################################################################
### Complete Match Check
################################################################################
class CompleteMatchCheck(Dict2Obj):
    """
    Compiler for Complete Match Check

    Param:
        package (str, Optional): component package name
        module (str, Optional): component module name
        class (str): component class name

    Attr:
        data (str): path to dataframe file
        entity_a_column(str): the index column in entity A
        entity_b_column(str): the index column in entity B
        relational_a_columns(dict): a config dict represents the distributions to be shown in the entity A,
                                    it has the following keys:
                                    - columns(list of str): a list of columns that require visualization for columns
                                    - foreign_file(str): file path to data file for entity.
                                                         Default is None if the columns are in the same data frame.
                                    - foreign_index(str): the index column in foreign data mapped to `entity_a_column`.
                                             Default is `entity_a_column` and will be ignored if foreign_file is None.
        relational_b_columns(dict): a config dict represents the distributions to be shown in the entity B.
                                    Details see above for `relational_a_columns`.

    Example:
        "component": {
            "package": "xai",
            "module": "compiler",
            "class": "CompleteMatchCheck",
            "attr": {
              "data": "matching.csv",
              "entity_a_column": "STUDENT_ID",
              "entity_b_column": "COURSE_ID",
              "relational_a_columns": {
                    "foreign_file": "student.csv",
                    "foreign_index": "STUDENT_ID",
                    "columns": [
                        {"name": "GENDER", "type": "categorical},
                        {"name": "AGE", "type": "numerical}
                    ]
              },
              "relational_b_columns": {
                    "foreign_file": "course.csv",
                    "foreign_index": "COURSE_ID",
                    "columns": [
                        {"name": "DEPARTMENT", "type": "categorical"},
                        {"name": "DURATION", "type": "numerical"}
                    ]
              }
            }
          }
    """
    schema = {
        "definitions": {
            "relational_columns": {
                "type": "object",
                "properties": {
                    "foreign_file": {"type": ["string", "object"]},
                    "foreign_index": {"type": "string"},
                    "columns": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "property": {
                                "name": {"type": "string"},
                                "type": {"enum": ["categorical", "numerical", "text", "datetime"]}
                            }
                        }
                    },
                },
                "required": ["columns"]
            }
        },
        "type": "object",
        "properties": {
            "data": {"type": ["string", "object"]},
            "entity_a_column": {"type": "string"},
            "entity_b_column": {"type": "string"},
            "relational_a_columns": {"$ref": "#/definitions/relational_columns"},
            "relational_b_columns": {"$ref": "#/definitions/relational_columns"}
        },
        "required": ["data", "entity_a_column", "entity_b_column"]
    }

    def __init__(self, dictionary):
        """
        Init

        Args:
            dictionary (dict): attribute to set
        """
        super(CompleteMatchCheck, self).__init__(dictionary,
                                                 schema=self.schema)

    def __call__(self, report: Report, level: int):
        """
        Execution

        Args:
            report (Report): report object
            level (int): content level
        """
        super(CompleteMatchCheck, self).__call__(report=report,
                                                 level=level)

        # -- Load Parameters --
        data_var = self.assert_attr(key='data')
        entity_a_column = self.assert_attr(key='entity_a_column')
        entity_b_column = self.assert_attr(key='entity_b_column')

        relational_a_columns = self.assert_attr(key='relational_a_columns', optional=True)
        relational_b_columns = self.assert_attr(key='relational_b_columns', optional=True)

        df = None
        # -- Load Data --
        if not (data_var is None):
            df = self.load_data(data_var, header=True)

        def get_relational_column_config(config, default_entity_key):
            """
            helper method to retrieve valid information from relational column config json
            Args:
                config (dict): same format as `relational_a_columns` and `relational_b_columns`
                default_entity_key(str): default index key for the entity to search for distribution

            Returns:
                entity_df: pandas.DataFrame, the data frame for entity
                entity_key: str, the index search for mapping with `entity_a_column` or `entity_b_column`
                entity_unit_stats: dict, the basic unit dict to capture the distribution.
                                    - key: column name
                                    - value: corresponding analyzer based on data type
            """

            entity_df = df
            entity_unit_stats = dict()
            entity_key = default_entity_key

            if "foreign_file" in config:
                foreign_var = config["foreign_file"]
                if not (foreign_var is None):
                    entity_df = self.load_data(foreign_var, header=True)
                if "foreign_index" in config:
                    entity_key = config["foreign_index"]

            for item in config['columns']:
                col_name = item['name']
                col_type = item['type']
                if col_type == DATATYPE.CATEGORY:
                    entity_unit_stats[col_name] = CategoricalDataAnalyzer()
                    entity_df[col_name] = entity_df[col_name].astype(str)
                elif col_type == DATATYPE.NUMBER:
                    entity_unit_stats[col_name] = NumericDataAnalyzer()
                    entity_df[col_name] = entity_df[col_name].astype(float)
                elif col_type == DATATYPE.FREETEXT:
                    entity_unit_stats[col_name] = TextDataAnalyzer()
                    entity_df[col_name] = entity_df[col_name].astype(str)
                elif col_type == DATATYPE.DATETIME:
                    entity_unit_stats[col_name] = DatetimeDataAnalyzer()
                    entity_df[col_name] = entity_df[col_name].astype(str)
                else:
                    raise AnalyzerDataTypeNotSupported(data_type=col_type)

            return entity_df, entity_key, entity_unit_stats

        # -- Initialize the stats default dict --
        entity_a_stats = None
        entity_b_stats = None
        if relational_a_columns is not None:
            entity_a_df, entity_a_key, entity_a_unit_stats = \
                get_relational_column_config(config=relational_a_columns,
                                             default_entity_key=entity_a_column)
            entity_a_stats = defaultdict(lambda: deepcopy(entity_a_unit_stats))

        if relational_b_columns is not None:
            entity_b_df, entity_b_key, entity_b_unit_stats = \
                get_relational_column_config(config=relational_b_columns,
                                             default_entity_key=entity_b_column)
            entity_b_stats = defaultdict(lambda: deepcopy(entity_b_unit_stats))

        # -- Check Complete Match --
        dv = DataframeValidator()
        complete_matches = dv.find_m_to_n_complete_matches(df=df, col_a=entity_a_column, col_b=entity_b_column)
        # -- Process complete match result and update visualization columns stats --

        print("number of complete matches:", complete_matches)
        m2n_stats = defaultdict(int)

        for col_a, col_b in complete_matches:
            m = len(col_a)
            n = len(col_b)
            m2n_stats[(m, n)] += 1
            if entity_a_stats is not None:
                sub_df = entity_a_df[entity_a_df[entity_a_key].isin(col_a)].drop_duplicates(subset=[entity_a_key],
                                                                                            inplace=False)
                for col_name, analyzer in entity_a_stats[(m, n)].items():
                    values = sub_df[col_name].values.tolist()
                    analyzer.feed_all(values)

            if entity_b_stats is not None:
                sub_df = entity_b_df[entity_b_df[entity_b_key].isin(col_b)].drop_duplicates(subset=[entity_b_key],
                                                                                            inplace=False)
                for col_name, analyzer in entity_b_stats[(m, n)].keys():
                    values = sub_df[col_name].values.tolist()
                    analyzer.feed_all(values)

        # -- Process complete match result and update visualization columns stats --
        table_header = ['M', 'N', 'Count', entity_a_column, entity_b_column]

        def draw_distribution_for_stats(stats):
            """
            Internal function to draw stats
            Args:
                stats: stat object generated from data.explorer
            """

            if type(stats) == CategoricalStats:
                dist_header = ["Value", "Count", "Percentage"]
                dist_values = []
                count_sum = sum(list(stats.frequency_count.values()))
                for key, value in stats.frequency_count.items():
                    dist_values.append([key, value, "%.2f%%" % (value / count_sum * 100)])
                report.detail.add_table(table_header=dist_header, table_data=dist_values,
                                        col_width=[40, 40, 40])
            elif type(stats) == NumericalStats:
                dist_header = ['Statistical Field', 'Value']
                dist_values = list()
                dist_values.append(['Total valid count', "%d" % int(stats.total_count)])
                dist_values.append(['Min', "%.3f" % float(stats.min)])
                dist_values.append(['Max', "%.3f" % float(stats.max)])
                dist_values.append(['Mean', "%.3f" % float(stats.mean)])
                dist_values.append(['Median', "%.3f" % float(stats.median)])
                dist_values.append(['Standard deviation', "%.3f" % float(stats.sd)])
                dist_values.append(['NAN count', "%d" % int(stats.nan_count)])
                report.detail.add_table(table_header=dist_header, table_data=dist_values,
                                        col_width=[60, 60])
            elif type(stats) == TextStats:
                report.detail.add_text_field_distribution(col_name, {'': stats})
            elif type(stats) == DatetimeStats:
                report.detail.add_datetime_field_distribution(col_name, {'': stats})

        for (m, n) in sorted(m2n_stats.keys()):
            count = m2n_stats[(m, n)]
            table_values = [[m, n, count, count * m, count * n]]
            print(m, n, count, count * m, count * n)
            report.detail.add_table(table_header=table_header, table_data=table_values, col_width=[20, 20, 20, 50, 50])

            if entity_a_stats is not None:
                for col_name, analyzer in entity_a_stats[(m, n)].items():
                    report.detail.add_paragraph('Distribution: %s' % col_name)
                    stats = analyzer.get_statistics()
                    draw_distribution_for_stats(stats)

            if entity_b_stats is not None:
                for col_name, analyzer in entity_b_stats[(m, n)].items():
                    report.detail.add_paragraph('Distribution: %s' % col_name)
                    stats = analyzer.get_statistics()
                    draw_distribution_for_stats(stats)
