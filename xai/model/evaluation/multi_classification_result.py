#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from collections import defaultdict

from xai import constants
from xai.model.evaluation.basic_result import ClassificationResult
from xai.model.evaluation.confusion_matrix import ConfusionMatrix
from xai.util import get_table_layout


################################################################################
### Multi Classification Result
################################################################################
class MultiClassificationResult(ClassificationResult):
    def __init__(self):
        super(MultiClassificationResult, self).__init__()
        self.average_result_dict = defaultdict(lambda: defaultdict(int))

    def load_results_from_meta(self, evaluation_result: dict):
        """
        save metrics into the object result class

        Args:
            evaluation_result(dict): key-value pair for metric
                - key: metric name
                - value: metric dict. The dict should either
                (1) have a `class` keyword, with key-value pair of class name and corresponding values, or
                (2) have a `average` keyword to show a macro-average metric.
        """
        for metric, values in evaluation_result.items():
            if metric == constants.METRIC_CM:
                self.confusion_matrices = ConfusionMatrix(label=values['labels'],
                                                          confusion_matrix=values['values'])
            else:
                if type(values) != dict:
                    continue
                else:
                    if 'class' in values.keys():
                        class_values = values['class']
                        for class_label, class_value in class_values.items():
                            self.update_result(metric, class_label, class_value)
                    if 'average' in values.keys():
                        self.average_result_dict[metric] = values['average']

    def convert_metrics_to_table(self, label_as_row=True):
        """
        converts the metrics saved in the object to a table that is ready to render in the report.

        Args:
            label_as_row (bool): True if each row of the output table is for a class,
                                 False if each row of the output table is for a metric

        Returns:
            a set of table (title, header, values)
        """
        if label_as_row:
            # set metric as columns, label as rows
            table_header = ['Label']
            table_header.extend([metric for metric in self.metric_set])

            table_content = []
            for label in self.label_set:
                row = [label]
                row.extend(
                    ["{:.4f}".format(self.resultdict[metric][label]) if type(
                        self.resultdict[metric][label]) == float else 'nan' for metric in self.metric_set])
                table_content.append(row)
        else:
            # set label as columns, metric as rows
            table_header = ['Metric']
            table_header.extend([label for label in self.label_set])

            table_content = []
            for metric in self.metric_set:
                row = [metric]
                row.extend(["{:.4f}".format(self.resultdict[metric][label]) for label in self.label_set])
                table_content.append(row)

        # add in average result if any[
        if table_header[0] == 'Label':
            row = ['Average']
            row.extend(
                ["{:.4f}".format(self.average_result_dict[metric]) if type(self.average_result_dict[metric]) != str else
                 self.average_result_dict[metric] for metric in self.metric_set])
            table_content.append(row)
        elif table_header[0] == 'Metric':
            table_header.append('Average')
            for row in table_content:
                metric = row[0]
                if type(self.average_result_dict[metric]) != str:
                    row.append("{:.4f}".format(self.average_result_dict[metric]))
                else:
                    row.append(self.average_result_dict[metric])
        layout = get_table_layout(table_header)
        table = ("Metric Result", table_header, table_content, layout)

        return table

    def get_confusion_matrices(self):
        return self.confusion_matrices
