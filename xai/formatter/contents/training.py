#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Training Content """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from xai.formatter.contents.base import Content
from xai.formatter.writer.base import Writer


################################################################################
###  Hyper Parameter Tuning Content
################################################################################
class HyperParameterTuning(Content):
    """
    Hyper Parameter Tuning
    """

    def __init__(self,
                 history: dict, best_idx: str, search_space=None,
                 benchmark_metric=None, benchmark_threshold=None,
                 non_hyperopt_score=None, notes=None) -> None:
        """
            Add information of hyperparameter tuning to the report.

            Args:
                history(:dict of dict): a dict of training log dict.
                    key: iteration index
                    value: hyperparameter tuning information
                            Each dict has two keys:
                                - params: a dict of which key is the parameter name
                                          and value is parameter value
                                - val_scores: a dict of which key is the metric name
                                             and value is metric value
                best_idx(str):
                    - the best idx based on benchmark metric, corresponding the `history` dict key
                search_space(:dict): parameter name and the search space for each parameter
                benchmark_metric(:str): the metric used for benchmarking during hyperparameter tunning
                benchmark_threshold(:float, Optional): the benchmarking threshold to accept the training
                non_hyperopt_score(:float, Optional): the training metric without hyperparameter tuning
                notes(:str): text to explain the block
        """
        super(HyperParameterTuning, self).__init__(history, best_idx,
                                                   search_space,
                                                   benchmark_metric,
                                                   benchmark_threshold,
                                                   non_hyperopt_score, notes)
        self._history = history
        self._best_idx = best_idx
        self._search_space = search_space
        self._benchmark_metric = benchmark_metric
        self._benchmark_threshold = benchmark_threshold
        self._non_hyperopt_score = non_hyperopt_score
        self._notes = notes

    @property
    def history(self):
        """Returns hyper-parameter tuning history."""
        return self._history

    @property
    def best_idx(self):
        """Returns best idx in hyper-parameter tuning history."""
        return self._best_idx

    @property
    def search_space(self):
        """Returns parameter name and the search space."""
        return self._search_space

    @property
    def benchmark_metric(self):
        """Returns the metric used for benchmarking."""
        return self._benchmark_metric

    @property
    def benchmark_threshold(self):
        """Returns the benchmarking threshold."""
        return self._benchmark_threshold

    @property
    def non_hyperopt_score(self):
        """Returns the training metric without hyper-parameter tuning."""
        return self._non_hyperopt_score

    @property
    def notes(self):
        """Returns hyper-parameter tuning info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Hyper-Parameter Tuning History

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_hyperparameter_tuning(notes=self.notes,
                                          history=self.history,
                                          best_idx=self.best_idx,
                                          search_space=self.search_space,
                                          benchmark_metric=self.benchmark_metric,
                                          benchmark_threshold=self.benchmark_threshold,
                                          non_hyperopt_score=self.non_hyperopt_score)

################################################################################
###  Learning Curve Content
################################################################################
class LearningCurve(Content):
    """
    Learning Curve
    """

    def __init__(self,
                 history: dict, best_idx: str,
                 benchmark_metric=None, benchmark_threshold=None,
                 training_params=None, notes=None) -> None:
        """
            Add information of learning curve to report.

            Args:
                history(:dict of dict): a dict of training log dict.
                    key: epoch index
                    value: learning epoch information
                            Each dict has two keys:
                                - params: a dict of params on current epochs (Optional)
                                - val_scores: a dict of which key is the metric name
                                            and value is metric value
                best_idx(str):
                    - the best epoch based on benchmark metric, corresponding the `history` dict key
                benchmark_metric(:str): the metric used for benchmarking during learning
                benchmark_threshold(:float, Optional): the benchmarking threshold to accept the training

                training_params(:dict): a dict of which key is training parameter name
                                            and value is training parameter value
                notes(:str): text to explain the block
        """
        super(LearningCurve, self).__init__(history, best_idx,
                                            benchmark_metric,
                                            benchmark_threshold,
                                            training_params, notes)
        self._history = history
        self._best_idx = best_idx
        self._benchmark_metric = benchmark_metric
        self._benchmark_threshold = benchmark_threshold
        self._training_params = training_params
        self._notes = notes

    @property
    def history(self):
        """Returns learning epoch history."""
        return self._history

    @property
    def best_idx(self):
        """Returns best epoch."""
        return self._best_idx

    @property
    def benchmark_metric(self):
        """Returns the metric used for benchmarking."""
        return self._benchmark_metric

    @property
    def benchmark_threshold(self):
        """Returns the benchmarking threshold."""
        return self._benchmark_threshold

    @property
    def training_params(self):
        """Returns the training metric without hyper-parameter tuning."""
        return self._training_params

    @property
    def notes(self):
        """Returns learning curve info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Learning Curve

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_learning_curve(notes=self.notes,
                                   history=self.history,
                                   best_idx=self.best_idx,
                                   benchmark_metric=self.benchmark_metric,
                                   benchmark_threshold=self.benchmark_threshold,
                                   training_params=self.training_params)
