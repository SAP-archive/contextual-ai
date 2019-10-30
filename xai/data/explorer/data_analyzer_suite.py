#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import Optional, Dict, Union, List

from xai.data.abstract_stats import AbstractStats
from xai.data.constants import DATATYPE
from xai.data.exceptions import AttributeNotFound, InconsistentSize, AnalyzerDataTypeNotSupported
from xai.data.exceptions import InvalidTypeError
from xai.data.explorer.categorical.labelled_categorical_analyzer import LabelledCategoricalDataAnalyzer
from xai.data.explorer.datetime.labelled_datetime_analyzer import LabelledDatetimeDataAnalyzer
from xai.data.explorer.numerical.labelled_numerical_analyzer import LabelledNumericalDataAnalyzer
from xai.data.explorer.sequence_analyzer import SequenceAnalyzer
from xai.data.explorer.text.labelled_text_analyzer import LabelledTextDataAnalyzer


class DataAnalyzerSuite:
    """
    A data analyzer suite that allows users to add multiple data analyzers and analyze specified according to data type
    """

    def __init__(self, data_type_list: List, column_names: List = None, sequence_names: List = None):
        """
        Initialize data analyzer suite

        Args:
            data_type_list: list, a list of pre-defined data type.
                            If column_names is not provided, data_type_list should for all the columns.
            column_names: list, a list of column names.
            sequence_names: list, a list of feature names that is considered sequence data.
        """
        if column_names is not None:
            if type(column_names) == list:
                if len(column_names) != len(data_type_list):
                    raise InconsistentSize('data_type_list', 'column_name', len(column_names), len(data_type_list))
            else:
                raise InvalidTypeError(data_type_list, type(data_type_list), '<list>')

        else:
            column_names = list(range(len(data_type_list)))

        self.schema = dict(zip(column_names, data_type_list))

        self.analyzers = dict()

        if sequence_names is None:
            sequence_names = []

        for key, data_type in self.schema.items():
            if data_type == DATATYPE.CATEGORY:
                analyzer = LabelledCategoricalDataAnalyzer()
            elif data_type == DATATYPE.NUMBER:
                analyzer = LabelledNumericalDataAnalyzer()
            elif data_type == DATATYPE.FREETEXT:
                analyzer = LabelledTextDataAnalyzer()
            elif data_type == DATATYPE.DATETIME:
                analyzer = LabelledDatetimeDataAnalyzer()
            else:
                raise AnalyzerDataTypeNotSupported(data_type)

            if key in sequence_names:
                self.analyzers[key] = SequenceAnalyzer(analyzer=analyzer)
            else:
                self.analyzers[key] = analyzer

    def feed_row(self, sample: Union[Dict, List], label: Optional = None):
        """
        Feed one sample into the analyzer suite to aggregate stats according to data type attribute

        Args:
            sample: json object
            label: class label associated to the sample, default is None when no label provided
        """
        if type(sample) == list and len(sample) != len(self.analyzers):
            raise InconsistentSize('sample', 'label', len(sample), len(self.analyzers))
        for attribute_name, analyzer in self.analyzers.items():
            if attribute_name not in sample:
                raise AttributeNotFound(attribute_name, sample)
            analyzer.feed(value=sample[attribute_name], label=label)

    def feed_column(self, column_name: Union[int, str], column_data: List, labels: List = None):
        """
        Feed a series of samples into the analyzer suite to aggregate stats according to data type attribute

        Args:
            column_name: str or int, column name/column index
            column_data: list, a sequence of values
            labels: list, class labels associated to the samples, default is None when no label provided

        """
        if labels is None:
            labels = [None] * len(column_data)

        if type(column_data) == list and len(column_data) != len(labels):
            raise InconsistentSize('column_data', 'labels', len(column_data), len(labels))

        if column_name not in self.analyzers.keys():
            raise AttributeNotFound(column_name, list(self.analyzers.keys()))

        self.analyzers[column_name].feed_all(values=column_data, labels=labels)

    def get_statistics(self) -> Dict[str, AbstractStats]:
        """
        Get overall stats for the entire data analyzer suite

        Returns:
            A dictionary maps attribute name to stats json object representation
        """
        overall_stats = dict()
        for attribute_name, analyzer in self.analyzers.items():
            overall_stats[attribute_name] = analyzer.get_statistics()
        return overall_stats
