#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Summary Content """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import List, Tuple

from xai.formatter.contents.base import Content
from xai.formatter.writer.base import Writer


################################################################################
###  Training Timing Content
################################################################################
class TrainingTiming(Content):
    """
    Training Timing
    """

    def __init__(self, timing: List[Tuple[str, int]], notes=None) -> None:
        """
        Add information of timing to the report

        Args:
            timing（:obj:`list` of :obj:`tuple`): list of tuple (name, time in second)
            notes (str): explain the block
        """
        super(TrainingTiming, self).__init__(timing, notes)
        self._timing = timing
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "Training Time Summary"

    @property
    def timing(self):
        """Returns training time."""
        return self._timing

    @property
    def notes(self):
        """Returns training timing info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Timing Table

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_training_time(notes=self.notes, timing=self.timing)


################################################################################
###  Data Set Summary Content
################################################################################
class DataSetSummary(Content):
    """
    Data Set Summary
    """

    def __init__(self, data_summary: List[Tuple[str, int]], notes=None) -> None:
        """
        Add information of dataset summary to the report

        Args:
            data_summary (:obj:`list` of :obj:`tuple`): list of tuple (dataset_name,
                                                        dataset_sample_number)
            notes (str, Optional): explain the block
        """
        super(DataSetSummary, self).__init__(data_summary, notes)
        self._data_summary = data_summary
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "Dataset Summary"

    @property
    def data_summary(self):
        """Returns dataset."""
        return self._data_summary

    @property
    def notes(self):
        """Returns dataset summary info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Data set Summary

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_data_set_summary(notes=self.notes, data_summary=self.data_summary)

################################################################################
###  Evaluation Result Summary Content
################################################################################
class EvaluationResultSummary(Content):
    """
    Evaluation Result Summary
    """

    def __init__(self, evaluation_result: dict, notes=None) -> None:
        """
        Add information of training performance to the result

        Args:
            evaluation_result (dict): evaluation metric
                - key: metric_name
                - value: metric_value: single float value for average/overall metric,
                                        list for class metrics
                sample input 1: {'precision': 0.5}, report value directly
                sample input 2: {'precision': {'class':[0.5,0.4,0.3],'average':0.5}},
                                                report "average" value
                sample input 3: {'precision': {'class':[0.5,0.4,0.3]},
                                report unweighted average for "class" value
            notes (str, Optional): explain the block
        """
        super(EvaluationResultSummary, self).__init__(evaluation_result, notes)
        self._evaluation_result = evaluation_result
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "Evaluation Result Summary"

    @property
    def evaluation_result(self):
        """Returns evaluation result."""
        return self._evaluation_result

    @property
    def notes(self):
        """Returns evaluation result summary info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Evaluation Result Summary

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_evaluation_result_summary(notes=self.notes,
                                              evaluation_result=self.evaluation_result)

################################################################################
###  Model Info Summary Content
################################################################################
class ModelInfoSummary(Content):
    """
    Model Info Summary
    """

    def __init__(self, model_info: list, notes=None) -> None:
        """
        Add information of model info summary to the report

        Args:
            model_info (:obj:`list` of :obj:
                `tuple`, Optional): list of tuple (model info attribute, model info value).
                Default information include `use case name`, `version`, `use case team`.
            notes (str, Optional):
                explain the block
        """
        super(ModelInfoSummary, self).__init__(model_info, notes)
        self._model_info = model_info
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "Model Info Summary"

    @property
    def model_info(self):
        """Returns evaluation result."""
        return self._model_info

    @property
    def notes(self):
        """Returns model info summary info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Model Info Summary

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_model_info_summary(notes=self.notes,
                                       model_info=self.model_info)
