#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import List

import numpy as np
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.metrics.classification import precision_recall_fscore_support, confusion_matrix

from xai.constants import METRIC_CM, METRIC_ACCURACY, METRIC_AUC, METRIC_F1, METRIC_RECALL, METRIC_PRECISION
from xai.model.evaluation.binary_classification_result import BinaryClassificationResult
from xai.model.evaluation.multi_classification_result import MultiClassificationResult


################################################################################
### ResultCompiler
################################################################################

class ResultCompiler:
    """
    Class for ResultCompiler
    """

    def __init__(self, labels: List, metric_list: List = None):
        """
        Initialize class for result

        Args:
            labels: list of str, list of labels
            metric_list: list of enum, list of required metric
        """
        self.labels = labels
        if metric_list is None:
            self.metric_list = [METRIC_ACCURACY, METRIC_PRECISION, METRIC_RECALL, METRIC_F1, METRIC_CM, METRIC_AUC]
        else:
            self.metric_list = metric_list
        self.metric_scores_ = dict()
        self.conf = None

    def load_results_from_raw_labels(self, y_true: np.array, y_pred: np.array, conf=None):
        """
        Load results from true labels and predicted labels

        Args:
            y_true: numpy array, true labels
            y_pred: numpy array, predicted labels
            conf: numpy array, confidence scores of predicted labels

        """
        accuracy = accuracy_score(y_pred=y_pred, y_true=y_true)
        auc = None
        self.conf = conf

        if len(self.labels) == 2:
            precision, recall, f_score, true_sum = precision_recall_fscore_support(y_true=y_true,
                                                                                   y_pred=y_pred,
                                                                                   labels=[1])
            if self.conf is not None:
                auc = roc_auc_score(y_true=y_true, y_score=conf)
        else:
            _precision, _recall, _f_score, _ = precision_recall_fscore_support(y_true=y_true,
                                                                               y_pred=y_pred,
                                                                               labels=list(range(len(self.labels))))
            class_precision = {key: value for key, value in list(zip(self.labels, _precision.tolist()))}
            precision = {'class': class_precision, 'average': np.mean(_precision)}

            class_recall = {key: value for key, value in list(zip(self.labels, _recall.tolist()))}
            recall = {'class': class_recall, 'average': np.mean(_recall)}

            class_f_score = {key: value for key, value in list(zip(self.labels, _f_score.tolist()))}
            f_score = {'class': class_f_score, 'average': np.mean(_f_score)}

            class_accuracy = {key: '-' for key in self.labels}
            accuracy = {'class': class_accuracy, 'average': accuracy}

            class_auc = {key: '-' for key in self.labels}
            auc = {'class': class_auc, 'average': 'N.A.'}

        if METRIC_PRECISION in self.metric_list:
            self.metric_scores_[METRIC_PRECISION] = precision
        if METRIC_RECALL in self.metric_list:
            self.metric_scores_[METRIC_RECALL] = recall
        if METRIC_F1 in self.metric_list:
            self.metric_scores_[METRIC_F1] = f_score
        if METRIC_ACCURACY in self.metric_list:
            self.metric_scores_[METRIC_ACCURACY] = accuracy
        if METRIC_CM in self.metric_list:
            self.metric_scores_[METRIC_CM] = {'labels': self.labels,
                                              'values': confusion_matrix(y_true=y_true, y_pred=y_pred)}
        if METRIC_AUC in self.metric_list:
            self.metric_scores_[METRIC_AUC] = auc

    def load_results_from_raw_prediction(self, y_true: np.array, y_prob: np.array):
        """
        Load results from true labels and predicted probability

        Args:
            y_true: numpy array, true labels
            y_prob: numpy array, predicted probability
        """
        if len(y_prob.shape) == 1:
            raise Exception("y_prob should be a shape dimension of 2.")
        elif y_prob.shape[1] != len(self.labels):
            raise Exception("y_prob should have a dimension of (?, %s)" % len(self.labels))
        if y_prob.shape[1] == len(self.labels):
            self.load_results_from_raw_labels(y_true=y_true,
                                              y_pred=np.argmax(y_prob, axis=1),
                                              conf=np.max(y_prob, axis=1))

    def get_result_instance(self):
        """
        Get result object for formatter

        Returns:
            ClassificationResult object
        """
        if len(self.labels) == 2:
            result = BinaryClassificationResult()
            result.load_results_from_meta(evaluation_result={'test': self.metric_scores_})
        else:
            result = MultiClassificationResult()
            result.load_results_from_meta(evaluation_result=self.metric_scores_)
        return result
