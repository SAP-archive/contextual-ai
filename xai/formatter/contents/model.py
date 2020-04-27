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
###  Model Interpreter for Classification and Regression
################################################################################
class ModelInterpreter(Content):
    """
    Model Interpreter for Classification and Regression
    """

    def __init__(self, mode: str, class_stats: dict, total_count: int,
                 stats_type: str, k:int, top: int=15, notes=None) -> None:
        """
        Add model interpreter by class

        Args:
            mode (str): Model Model - classification/regression model
            class_stats (dict): A dictionary maps the label to its aggregated statistics
            total_count (int): The total number of explanations to generate the statistics
            stats_type (str): The defined stats_type for statistical analysis
            k (int): The k value of the defined stats_type
            top (int): the number of top explanation to display
            notes(str): text to explain the block
        """
        super(ModelInterpreter, self).__init__(mode, class_stats, total_count,
                                               stats_type, k, top, notes)
        self._mode = mode
        self._class_stats = class_stats
        self._total_count = total_count
        self._stats_type = stats_type
        self._k = k
        self._top = top
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "This section shows {} model interpreter.".format(mode)

    @property
    def mode(self):
        """Returns Mode."""
        return self._mode

    @property
    def class_stats(self):
        """Returns Class Aggregated Statistics."""
        return self._class_stats

    @property
    def total_count(self):
        """Returns The total number of explanations."""
        return self._total_count

    @property
    def stats_type(self):
        """Returns the defined stats_type for statistical analysis."""
        return self._stats_type

    @property
    def k(self):
        """Returns the k value of the defined stats_type."""
        return self._k

    @property
    def top(self):
        """Returns the number of top explanation to display."""
        return self._top

    @property
    def notes(self):
        """Returns model interpreter by class info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Model Interpreter By Class

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_model_interpreter(notes=self.notes, mode=self.mode,
                                      class_stats=self.class_stats,
                                      total_count=self.total_count,
                                      stats_type=self.stats_type,
                                      k=self.k, top=self.top)

################################################################################
###  Error Analysis for Classification and Regression
################################################################################
class ErrorAnalysis(Content):
    """
    Error Analysis for Classification and Regression
    """

    def __init__(self, mode: str, error_stats: dict, stats_type: str,
                 k:int, top: int=15, notes=None) -> None:
        """
        Add error analysis by class

        Args:
            mode (str): Model Model - classification/regression model
            error_stats (dict): A dictionary maps the label to its aggregated statistics
            stats_type (str): The defined stats_type for statistical analysis
            k (int): The k value of the defined stats_type
            top (int): the number of top explanation to display
            notes(str): text to explain the block
        """
        super(ErrorAnalysis, self).__init__(mode, error_stats, top, notes)
        self._mode = mode
        self._error_stats = error_stats
        self._stats_type = stats_type
        self._k = k
        self._top = top
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "This section shows {} error analysis.".format(mode)

    @property
    def mode(self):
        """Returns Mode."""
        return self._mode

    @property
    def error_stats(self):
        """Returns Class Aggregated Statistics."""
        return self._error_stats

    @property
    def stats_type(self):
        """Returns the defined stats_type for statistical analysis."""
        return self._stats_type

    @property
    def k(self):
        """Returns the k value of the defined stats_type."""
        return self._k

    @property
    def top(self):
        """Returns the number of top explanation to display."""
        return self._top

    @property
    def notes(self):
        """Returns model interpreter by class info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Error Analysis By Class

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_error_analysis(notes=self.notes, mode=self.mode,
                                   error_stats=self.error_stats,
                                   stats_type=self.stats_type,
                                   k=self.k, top=self.top)
