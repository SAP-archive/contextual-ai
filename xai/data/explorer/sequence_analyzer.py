#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from xai.data.explorer.abstract_labelled_analyzer import AbstractLabelledDataAnalyzer
from xai.data.exceptions import InvalidTypeError, InconsistentSize


class SequenceAnalyzer:
    """
    Class to analyze sequence data
    """
    def __init__(self, analyzer: AbstractLabelledDataAnalyzer):
        """
        Initialize sequence analyzer

        Args:
            analyzer: labelled data analyzer
        """
        self.analyzer = analyzer

    def feed(self, value, label):
        """
        Feed sequence values into analyzer and aggregate the stats

        Args:
            value: a list of items
            label: label associated with the value

        """
        if type(value) != list:
            raise InvalidTypeError('value', type(value), '<list>')

        for item in value:
            self.analyzer.feed(value=item, label=label)

    def feed_all(self, values, labels):
        """
        Feed all sequence values into analyzer and aggregate the stats
        Args:
            values: lists of items
            labels: labels associated with the value
        """
        if len(values) != len(labels):
            raise InconsistentSize('values', 'labels', len(values), len(labels))

        value_label = zip(values, labels)
        for value, label in value_label:
            self.feed(value, label)

    def get_statistics(self):
        """
        Get stats object for analyzer

        Returns:
            Object that extends the AbstractStats for all class stats
            and a dictionary maps label to the aggregated stats json object

        """
        return self.analyzer.get_statistics()
