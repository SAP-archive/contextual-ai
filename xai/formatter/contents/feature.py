#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Feature Content """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import List

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
