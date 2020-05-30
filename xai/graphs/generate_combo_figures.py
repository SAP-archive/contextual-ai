#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Generate Combo Figures """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import operator
import os
import warnings

from xai import constants
from xai.graphs import format_contants as graph_constants
from xai.graphs import graph_generator as gg


def get_feature_image_for_similar_classes(dataset, label_key, feature_name, base_class, similar_class,
                                          sub_confusion_matrix):
    # TODO: if figure not exist, regenerate

    image_path_a = os.path.join(constants.FIGURE_PATH,
                                ('%s_%s_%s_%s.png' % (dataset, label_key, feature_name, base_class)).replace('/', '-'))
    if not os.path.exists(image_path_a):
        image_path_a = os.path.join(constants.FIGURE_PATH,
                                    ('%s_%s_%s_%s.png' % (
                                        constants.KEY_DATA_ALL, label_key, feature_name, base_class)).replace('/',
                                                                                                              '-'))
    image_path_b = os.path.join(constants.FIGURE_PATH,
                                ('%s_%s_%s_%s.png' % (dataset, label_key, feature_name, similar_class)).replace('/',
                                                                                                                '-'))
    if not os.path.exists(image_path_b):
        image_path_b = os.path.join(constants.FIGURE_PATH,
                                    ('%s_%s_%s_%s.png' % (
                                        constants.KEY_DATA_ALL, label_key, feature_name, similar_class)).replace('/',
                                                                                                                 '-'))

    image_cm = gg.HeatMap(sub_confusion_matrix, 'cm_%s_%s_%s' % (label_key, base_class, similar_class), 'Predicted',
                          'True').draw(x_tick=[base_class, similar_class], y_tick=[base_class, similar_class],
                                       color_bar=False, grey_scale=True)

    return {'image_set': [image_cm, image_path_a, image_path_b],
            'grid_spec': graph_constants.ABSOLUTE_3_COMPARISON_2_GRID_SPEC}


def get_class_confidence_distribution_image_list(label_key, visualization_result, TOP_K_CLASS=9):
    sw_image_path_list = []
    predicted_class_count = dict()
    for label in visualization_result.keys():
        data = visualization_result[label]
        num_sample = len(data[constants.KEY_GROUNDTRUTH])
        predicted_class_count[label] = num_sample

    sorted_class_size = sorted(predicted_class_count.items(), key=operator.itemgetter(1))[::-1]
    warnings.warn(
        message='Top predicted classes: {}'.format(sorted_class_size))
    top_classes = [a for (a, _) in sorted_class_size]

    for class_label in top_classes:
        data = visualization_result[class_label]
        num_sample = len(data[constants.KEY_GROUNDTRUTH])
        if num_sample > 0:
            sw_image_path = gg.ResultProbabilityForMultiClass(data,
                                                              '%s_%s_ConfidenceDistribution' % (
                                                                  label_key, class_label)).draw()
            sw_image_path_list.append(sw_image_path)
        if len(sw_image_path_list) >= TOP_K_CLASS:
            break

    return {'image_set': sw_image_path_list, 'grid_spec': graph_constants.ABSOLUTE_3_EQUAL_GRID_SPEC}


def get_class_reliability_diagram_image_list(label_key, visualization_result, TOP_K_CLASS=9):
    rd_image_path_list = []
    predicted_class_count = dict()
    for label in visualization_result.keys():
        data = visualization_result[label]
        num_sample = len(data[constants.KEY_GROUNDTRUTH])
        predicted_class_count[label] = num_sample

    sorted_class_size = sorted(predicted_class_count.items(), key=operator.itemgetter(1))[::-1]
    warnings.warn(
        message='Top predicted classes: {}'.format(sorted_class_size))
    top_classes = [a for (a, _) in sorted_class_size]

    for class_label in top_classes:
        data = visualization_result[class_label]
        num_sample = len(data[constants.KEY_GROUNDTRUTH])
        if num_sample > 0:
            rd_image_path = gg.ReliabilityDiagramForMultiClass(data,
                                                               '%s_%s_ReliabilityDiagram' % (
                                                                   label_key, class_label)).draw(
                current_class_label=class_label)
            rd_image_path_list.append(rd_image_path)
        if len(rd_image_path_list) >= TOP_K_CLASS:
            break

    return {'image_set': rd_image_path_list, 'grid_spec': graph_constants.ABSOLUTE_RESULT_3_EQUAL_GRID_SPEC}
