#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import List

from xai import constants
from xai.model.evaluation.basic_result import ClassificationResult
from xai.model.evaluation.confusion_matrix import ConfusionMatrix
from xai.util import get_table_layout


################################################################################
### Binary Classification Result
################################################################################
class BinaryClassificationResult(ClassificationResult):
    """
    evaluation result class for binary classification problem
    """

    def __init__(self):
        super(BinaryClassificationResult, self).__init__()

    def load_results_from_meta(self, evaluation_result: dict, label: List = None):
        """
        save metrics into the object result class

        Args:
            evaluation_result(dict): key-value pair for metric
                - key: metric name
                - value: metric dict
            label(list): classification label list
        """
        for metric, value in evaluation_result.items():
            if metric == constants.METRIC_CM:
                if label is None:
                    label = ['0', '1']
                self.confusion_matrix = ConfusionMatrix(label=label, confusion_matrix=value)
            else:
                self.update_result(metric, 1, value)

    def convert_metrics_to_table(self):
        """
        converts the metrics saved in the object to a table that is ready to render in the report.

        Returns:
            a set of tables (title, header, values)
        """

        table_header = ['Metric', 'Value']
        table_content = []
        for metric in self.metric_set:
            table_content.append([metric.capitalize(), "%.4f" % self.resultdict[metric][1]])
        layout = get_table_layout(table_header)
        output_tables = ('Overall Result', table_header, table_content, layout)
        return output_tables

    def get_confusion_matrix(self):
        """
        returns the ConfusionMatrix object associated with the result

        Returns:
            ConfusionMatrix object
        """

        return self.confusion_matrix
