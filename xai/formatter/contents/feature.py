#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Feature Content """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import List, Tuple
import numpy

from xai.formatter.contents.base import Content
from xai.formatter.writer.base import Writer


################################################################################
###  Feature Important Content
################################################################################
class FeatureImportance(Content):
    """
    Feature Importance
    """

    def __init__(self,
                 importance_ranking: List[List], importance_threshold: float,
                 maximum_number_feature=20, notes=None) -> None:
        """
        Add information of feature importance to the report.

        Args:
            importance_ranking(:list of :list): a list of 2-item lists,
                                    item[0]: score, item[1] feature_name
            importance_threshold(float): threshold for displaying the
                                        feature name and score in tables
            maximum_number_feature(int): maximum number of features shown in bar-chart diagram
            notes(str): text to explain the block
        """
        super(FeatureImportance, self).__init__(importance_ranking,
                                                importance_threshold,
                                                maximum_number_feature, notes)
        self._importance_ranking = importance_ranking
        self._importance_threshold = importance_threshold
        self._maximum_number_feature = maximum_number_feature
        self._notes = notes

    @property
    def importance_ranking(self):
        """Returns feature importance ranking."""
        return self._importance_ranking

    @property
    def importance_threshold(self):
        """Returns feature importance threshold ."""
        return self._importance_threshold

    @property
    def maximum_number_feature(self):
        """Returns maximum number of features."""
        return self._maximum_number_feature

    @property
    def notes(self):
        """Returns feature importance info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Feature Importance

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_feature_importance(notes=self.notes,
                                       importance_ranking=self.importance_ranking,
                                       importance_threshold=self.importance_threshold,
                                       maximum_number_feature=self.maximum_number_feature)


################################################################################
###  Feature Shap Values Content
################################################################################
class FeatureShapValues(Content):
    """
    Feature Importance
    """

    def __init__(self, mode: str,
                 feature_shap_values: List[Tuple[str, List]],
                 class_id: int,
                 train_data: numpy.ndarray,
                 notes=None) -> None:
        """
        Add information of feature shap values to the report.

        Args:
            mode (str): Model Model - classification/regression model
            feature_shap_values(:list of :tuple): a list of 2-item tuple,
                                                  item[0]: feature name, item[1] shap values on each training samples
            class_id(int): the class id for visualization.
            train_data(numpy.dnarray): Optional, training data, row is for samples, column is for features.
            notes(str): text to explain the block
        """
        super(FeatureShapValues, self).__init__(mode, feature_shap_values,
                                                class_id,
                                                train_data,
                                                notes)
        self._mode = mode
        self._feature_shap_values = feature_shap_values
        self._class_id = class_id
        self._train_data = train_data
        self._notes = notes

    @property
    def mode(self):
        """Returns Mode."""
        return self._mode

    @property
    def feature_shap_values(self):
        """Returns feature shap values."""
        return self._feature_shap_values

    @property
    def class_id(self):
        """Returns class id."""
        return self._class_id

    @property
    def train_data(self):
        """Returns train_data."""
        return self._train_data

    @property
    def notes(self):
        """Returns feature importance info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Feature Importance

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_feature_shap_values(notes=self.notes, mode=self.mode,
                                        feature_shap_values=self.feature_shap_values,
                                        class_id=self.class_id,
                                        train_data=self.train_data)
