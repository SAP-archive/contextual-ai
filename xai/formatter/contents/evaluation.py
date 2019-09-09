#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Evaluation Content """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from xai.formatter.contents.base import Content
from xai.formatter.writer.base import Writer


################################################################################
###  Multi Class Evaluation Metric Result Content
################################################################################
class MultiClassEvaluationMetricResult(Content):
    """
    Multi Class Evaluation Metric Result
    """

    def __init__(self, metric_tuple, notes=None) -> None:
        """
        Add information about metric results for multi-class evaluation

        Args:
            metric_tuple(tuple): (evaluation_header, evaluation_metric_dict)
                - evaluation_header(str): a header for current evaluation,
                                        can be split or round number.
                - evaluation_metric_dict(dict): key-value pair for metric
                    - key: metric name
                    - value: metric dict. The dict should either
                     (1) have a `class` keyword, with key-value pair of class name
                            and corresponding values, or
                     (2) have a `average` keyword to show a macro-average metric.
            notes(str): text to explain the block
        """
        super(MultiClassEvaluationMetricResult, self).__init__(metric_tuple,
                                                               notes)
        self._metric_tuple = metric_tuple
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "This section shows multi-class evaluation metric."

    @property
    def metric_tuple(self):
        """Returns metric."""
        return self._metric_tuple

    @property
    def notes(self):
        """Returns multi-class evaluation metric info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Multi Class Evaluation Metric Result

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_multi_class_evaluation_metric_results(notes=self.notes,
                                                          metric_tuple=self.metric_tuple)


################################################################################
###  Binary Class Evaluation Metric Result Content
################################################################################
class BinaryClassEvaluationMetricResult(Content):
    """
    Binary Class Evaluation Metric Result
    """

    def __init__(self, metric_tuple: tuple, aggregated=True,
                 notes=None) -> None:
        """
        add information about metric results for binary-class evaluation

        Args:
            metric_tuple(tuple): (evaluation_header, evaluation_metric_dict)
                - evaluation_header(str): a header for current evaluation, can be split or round number.
                - evaluation_metric_dict(dict): key-value pair for metric
                    - key: metric name
                    - value: metric value
            aggregated(bool): whether to aggregate multiple result tables into one
                                default True
            notes(str): text to explain the block
        """
        super(BinaryClassEvaluationMetricResult, self).__init__(metric_tuple,
                                                                notes)
        self._metric_tuple = metric_tuple
        self._aggregated = aggregated
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "This section shows binary-class evaluation metric."

    @property
    def metric_tuple(self):
        """Returns metric."""
        return self._metric_tuple

    @property
    def aggregated(self):
        """Returns aggregate indicator."""
        return self._aggregated

    @property
    def notes(self):
        """Returns binary-class evaluation metric info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Binary Class Evaluation Metric Result

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_binary_class_evaluation_metric_results(notes=self.notes,
                                                           metric_tuple=self.metric_tuple,
                                                           aggregated=self.aggregated)


################################################################################
###  Confusion Matrix Content
################################################################################
class ConfusionMatrixResult(Content):
    """
    Confusion Matrix
    """

    def __init__(self, confusion_matrix_tuple: tuple, notes=None) -> None:
        """
        add information about confusion matrix to report

        Args:
            confusion_matrix_tuple(tuple): (confusion_matrix_header,
            confusion_matrix_dict)
                - confusion_matrix_header(str): a header for confusion_matrix,
                                            can be split or round number.
                - confusion_matrix_dict(dict):
                    - `labels`(:list of :str): label of classes
                    - `values`(:list of :list): 2D list for confusion matrix value,
                                        row for predicted, column for true.
            notes(str): text to explain the block
        """
        super(ConfusionMatrixResult, self).__init__(confusion_matrix_tuple,
                                                    notes)
        self._confusion_matrix_tuple = confusion_matrix_tuple
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "This section shows confusion matrix result."

    @property
    def confusion_matrix_tuple(self):
        """Returns confusion matrix."""
        return self._confusion_matrix_tuple

    @property
    def notes(self):
        """Returns confusion matrix info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Confusion Matrix Result

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_confusion_matrix_results(notes=self.notes,
                                             confusion_matrix_tuple=self.confusion_matrix_tuple)


################################################################################
###  Multi Class Confidence Distribution Content
################################################################################
class MultiClassConfidenceDistribution(Content):
    """
    Multi-Class Confidence Distribution
    """

    def __init__(self, visual_result_tuple: tuple, max_num_classes=9,
                 notes=None) -> None:
        """
        add information about multi class confidence distribution to report

        Args:
            *visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
               - visual_result_header(str): a header for confusion_matrix, can be split or round number.
               - visual_result_dict(dict): key-value
                   - key(str): the predicted class
                   - value(dit): result dict
                        - `gt` (:list of :str): ground truth class label for all samples
                        - `values` (:list of :float): probability for all samples
            max_num_classes(int, Optional): maximum number of classes
                                    displayed for each graph, default 9
            notes(str,Optional): text to explain the block
       """
        super(MultiClassConfidenceDistribution, self).__init__(
            visual_result_tuple,
            max_num_classes,
            notes)
        self._visual_result_tuple = visual_result_tuple
        self._max_num_classes = max_num_classes
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "This section shows multi-class confidence " \
                          "distribution result."

    @property
    def visual_result_tuple(self):
        """Returns visual result."""
        return self._visual_result_tuple

    @property
    def max_num_classes(self):
        """Returns maximum number of classes."""
        return self._max_num_classes

    @property
    def notes(self):
        """Returns multi class confidence distribution info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Multi-Class Confidence Distribution Result

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_multi_class_confidence_distribution(notes=self.notes,
                                                        visual_result_tuple=self.visual_result_tuple,
                                                        max_num_classes=self.max_num_classes)


################################################################################
###  Binary Class Confidence Distribution Content
################################################################################
class BinaryClassConfidenceDistribution(Content):
    """
    Binary-Class Confidence Distribution
    """

    def __init__(self, visual_result_tuple: tuple, notes=None) -> None:
        """
        add information about binary class confidence distribution to report

        Args:
            *visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
               - visual_result_header(str): a header for confusion_matrix, can be split or round number.
               - visual_result_dict(dict): key-value
                    - `gt` (:list of :str): ground truth class label for all samples
                    - `probability` (:list of :list): 2D list (N sample * 2)
                          to present probability distribution of each sample
            notes(str,Optional): text to explain the block
        """
        super(BinaryClassConfidenceDistribution, self).__init__(
            visual_result_tuple,
            notes)
        self._visual_result_tuple = visual_result_tuple
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "This section shows binary-class confidence " \
                          "distribution result."

    @property
    def visual_result_tuple(self):
        """Returns visual result."""
        return self._visual_result_tuple

    @property
    def notes(self):
        """Returns binary class confidence distribution info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Binary-Class Confidence Distribution Result

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_binary_class_confidence_distribution(notes=self.notes,
                                                         visual_result_tuple=self.visual_result_tuple)


################################################################################
###  Binary Class Reliability Diagram Content
################################################################################
class BinaryClassReliabilityDiagram(Content):
    """
    Binary-Class Reliability Diagram
    """

    def __init__(self, visual_result_tuple: tuple, notes=None) -> None:
        """
        add information about reliability to report

        Args:
            *visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
               - visual_result_header(str): a header for confusion_matrix, can be split or round number.
               - visual_result_dict(dict): key-value
                    - `gt` (:list of :str): ground truth class label for all samples
                    - `probability` (:list of :list): 2D list (N sample * 2) to
                                present probability distribution of each sample
            notes(str,Optional): text to explain the block
        """
        super(BinaryClassReliabilityDiagram, self).__init__(
            visual_result_tuple,
            notes)
        self._visual_result_tuple = visual_result_tuple
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "This section shows binary-class reliability " \
                          "diagram result."

    @property
    def visual_result_tuple(self):
        """Returns visual result."""
        return self._visual_result_tuple

    @property
    def notes(self):
        """Returns binary class reliability diagram info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Binary-Class Reliability Diagram Result

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_binary_class_reliability_diagram(notes=self.notes,
                                                     visual_result_tuple=self.visual_result_tuple)
