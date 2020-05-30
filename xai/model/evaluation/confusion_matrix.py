#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import defaultdict
from typing import List

import numpy as np
import warnings


################################################################################
### Confusion Matrix
################################################################################
class ConfusionMatrix:
    def __init__(self, label: List[str], confusion_matrix: List[List[float]]):
        self.label = label
        self.confusion_matrix = confusion_matrix

    def get_values(self):
        return self.confusion_matrix

    def get_labels(self):
        return self.label

    def get_top_k_similar_classes(self, k, top_n_class=10, tf_thresdhold=0.8):
        if k > len(self.confusion_matrix):
            raise Exception('Error: N exceeds the class numbers.')
        values = np.array(self.confusion_matrix)
        class_count = np.sum(values, axis=1)

        top_classes = np.argsort(class_count)[::-1]
        similar_class = defaultdict(list)

        if len(top_classes) < top_n_class:
            top_n_class = len(top_classes)
        for i in range(top_n_class):
            targeted_class = top_classes[i]
            predicted_distribution = values[targeted_class, :]
            true_positive = predicted_distribution[targeted_class]
            tf_rate = true_positive / class_count[targeted_class]
            if tf_rate > tf_thresdhold:
                warnings.warn(message='Class [%s] is well classified, ignored in ' \
                               'finding similar class.' % self.label[targeted_class])
                continue
            args = np.argsort(predicted_distribution)[::-1]
            j = 0
            counter = 0
            while counter < k:
                sim_idx = args[j]
                if sim_idx == targeted_class:
                    j += 1
                    continue
                similar_class[self.label[targeted_class]].append(
                    (self.label[sim_idx], values[:, [targeted_class, sim_idx]][[targeted_class, sim_idx], :]))
                j += 1
                counter += 1
        return similar_class
