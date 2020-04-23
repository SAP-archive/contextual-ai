#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import warnings

import dill
import numpy as np
import shap
from typing import Optional, Callable, Any, List, Dict

from xai.explainer.abstract_explainer import AbstractExplainer
from xai.explainer.explainer_exceptions import ExplainerUninitializedError
from xai.explainer.utils import parse_shap_values

NUM_TOP_FEATURES = 5


class SHAPTabularExplainer(AbstractExplainer):

    def __init__(self):
        super(SHAPTabularExplainer, self).__init__()
        self.feature_names = None

    def build_explainer(self,
                        training_data: Any,
                        predict_fn: Callable,
                        feature_names: List[str] = None,
                        **kwargs):
        """
        Builds the SHAP kernel explainer
        See https://shap.readthedocs.io/en/latest/#shap.KernelExplainer for additional details

        Args:
            training_data (numpy.array or pandas.DataFrame or shap.common.DenseData or
                any scipy.sparse matrix): The background dataset to use for integrating
                out features. In other words, the training data for the SHAP explainer
            predict_fn (Callable): User supplied function that takes a matrix of samples
                (# samples x # features) and computes a the output of the model for those samples.
                The output can be a vector (# samples) or a matrix (# samples x # model outputs).
            feature_names (list): List of feature names corresponding to the data

        Returns:
            None
        """
        # Convert feature_names to a list if not None (in case it's a np.ndarray)
        if feature_names is not None:
            feature_names = list(feature_names)
        self.feature_names = feature_names
        self.predict_fn = predict_fn
        self.explainer_object = shap.KernelExplainer(
            model=predict_fn,
            data=training_data)

    def explain_instance(self,
                         instance: np.ndarray,
                         num_samples: Optional[int] = None,
                         num_features: int = NUM_TOP_FEATURES, **kwargs) -> Dict[int, Dict]:
        """
        Estimate the SHAP values for a sample

        Args:
            instance (np.ndarray): A 1D numpy array corresponding to a row/single example
            num_samples (int): The number of re-evaluations to conduct. The higher the samples,
                the lower the variance
            num_features (int): Number of features to include in an explanation

        Returns:
            (dict) A mapping of class to explanations

        Raises:
            ExplainerUninitializedError: Raised if self.explainer_object is None
        """
        if num_samples is None:
            # Let SHAP figure out default number of samples
            num_samples = 'auto'
            warnings.warn(message='SHAP default number of samples[{}]'.format(num_samples))

        if self.explainer_object:
            if len(instance.shape) != 2:
                instance = instance.reshape([1, -1])

            confidences = list(np.array(self.predict_fn(instance)).ravel())

            explanation = self.explainer_object.shap_values(
                X=instance,
                nsamples=num_samples,
                l1_reg='num_features({})'.format(NUM_TOP_FEATURES)
            )
            return parse_shap_values(shap_values=explanation,
                                     confidences=confidences,
                                     feature_names=self.feature_names,
                                     feature_values=list(instance.ravel()))
        else:
            raise ExplainerUninitializedError('This explainer is not yet instantiated! '
                                              'Please call build_explainer()'
                                              'first before calling explain_instance.')

    def save_explainer(self, path: str):
        """
        Save the explainer.

        Args:
            path (str): Path to save the explainer

        Returns:
            None
        """
        dict_to_save = {
            'explainer_object': self.explainer_object,
            'feature_names': self.feature_names,
        }
        with open(path, 'wb') as fp:
            dill.dump(dict_to_save, fp)

    def load_explainer(self, path: str):
        """
        Load the explainer

        Args:
            path (str): Path to load the explainer

        Returns:
            None
        """
        with open(path, 'rb') as fp:
            dict_loaded = dill.load(fp)
            self.explainer_object = dict_loaded['explainer_object']
            self.feature_names = dict_loaded['feature_names']
            self.predict_fn = self.explainer_object.model.f
