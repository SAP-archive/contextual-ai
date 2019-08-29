import logging
from typing import Optional, Callable, Any, List, Dict

import dill
import numpy as np
import shap

from ..abstract_explainer import AbstractExplainer
from ..explainer_exceptions import ExplainerUninitializedError

LOGGER = logging.getLogger(__name__)

NUM_TOP_FEATURES = 5


class SHAPTabularExplainer(AbstractExplainer):

    def __init__(self):
        super(SHAPTabularExplainer, self).__init__()

    def build_explainer(self,
                        predict_fn: Callable,
                        data: Any,
                        feature_names: List[str] = None):
        """
        Builds the SHAP kernel explainer
        See https://shap.readthedocs.io/en/latest/#shap.KernelExplainer for additional details

        Args:
            predict_fn (Callable): User supplied function that takes a matrix of samples
                (# samples x # features) and computes a the output of the model for those samples.
                The output can be a vector (# samples) or a matrix (# samples x # model outputs).
            data (numpy.array or pandas.DataFrame or shap.common.DenseData or
                any scipy.sparse matrix): The background dataset to use for integrating
                out features. In other words, the training data for the SHAP explainer
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
            data=data)

    def explain_instance(self,
                         instance: np.ndarray,
                         nsamples: Optional[int] = None,
                         num_features: int = NUM_TOP_FEATURES) -> Dict[int, Dict]:
        """
        Estimate the SHAP values for a sample

        Args:
            instance (np.ndarray): A 1D numpy array corresponding to a row/single example
            nsamples (int): The number of re-evaluations to conduct. The higher the samples,
                the lower the variance
            num_features (int): Number of features to include in an explanation

        Returns:
            (dict) A mapping of class to explanations

        Raises:
            ExplainerUninitializedError: Raised if self.explainer_object is None
        """
        if len(instance.shape) != 2:
            instance = instance.reshape([1, -1])

        confidences = list(np.array(self.predict_fn(instance)).ravel())

        if nsamples is None:
            # Let SHAP figure out default number of samples
            nsamples = 'auto'

        if self.explainer_object:
            explanation = self.explainer_object.shap_values(
                X=instance,
                nsamples=nsamples,
                l1_reg='num_features({})'.format(NUM_TOP_FEATURES)
            )
            return self.parse_shap_values(shap_values=explanation,
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

    def parse_shap_values(self, shap_values: List[np.ndarray], confidences: List[float],
                          feature_names: Optional[List[str]] = None,
                          feature_values: Optional[List[Any]] = None) -> Dict[int, Dict]:
        """
        Parse SHAP values to fit XAI output format

        Args:
            shap_values (list): A list of shap values, a set for each class
            confidences (list): Confidences for each class
            feature_names (list): List of feature names
            feature_values (list): List of values corresponding to feature_names

        Returns:
            (dict) A mapping of class to explanations

        """
        assert len(shap_values) == len(confidences), 'Number of SHAP values should be equal to ' \
                                                     'number of classes!'

        dict_explanation = {}

        for label, confidence in enumerate(confidences):
            tmp = []

            shap_value_class = shap_values[label][0]
            for feature_idx, shap_value in enumerate(shap_value_class):
                # We ignore features which SHAP values are 0, which indicate that they had no
                # impact on the model's decision
                if shap_value != 0:
                    if feature_names and feature_values:
                        feature = '{} = {}'.format(
                            feature_names[feature_idx], feature_values[feature_idx])
                        tmp.append({'feature': feature, 'score': shap_value})
                    else:
                        tmp.append({'feature': feature_idx, 'score': shap_value})

            dict_explanation[label] = {
                'confidence': confidence,
                'explanation': tmp
            }

        return dict_explanation
