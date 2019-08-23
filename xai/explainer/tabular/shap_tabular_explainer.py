import logging
from typing import Optional, Callable, Any

import dill
import numpy as np
import shap

from ..abstract_explainer import AbstractExplainer
from ..explainer_exceptions import ExplainerUninitializedError

LOGGER = logging.getLogger(__name__)

NUM_TOP_FEATURES = 5

class SHAPTabularExplainer(AbstractExplainer):

    def __init__(self):
        super(AbstractExplainer, self).__init__()

    def build_explainer(self, predict_fn: Callable,
                        data: Any):
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

        Returns:
            None
        """
        self.explainer_object = shap.KernelExplainer(
            model=predict_fn,
            data=data)

    def explain_instance(self, instance: np.array,
                         nsamples: Optional[int],
                         num_features: int = NUM_TOP_FEATURES):
        """
        Estimate the SHAP values for a sample

        Args:
            instance (np.array): A 1D numpy array corresponding to a row/single example
            nsamples (int): The number of re-evaluations to conduct. The higher the samples,
                the lower the variance

        Returns:
            (list) A list of tuples of the form (feature, weight)

        Raises:
            ExplainerUninitializedError: Raised if self.explainer_object is None
        """
        if len(instance.shape) != 2:
            instance = instance.reshape([1, -1])

        if nsamples is None:
            # Let SHAP figure out default number of samples
            nsamples = 'auto'

        if self.explainer_object:
            explanation = self.explainer_object.shap_values(
                X=instance,
                nsamples=nsamples,
                l1_reg='num_features({})'.format(NUM_TOP_FEATURES)
            )
            return explanation
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
        with open(path, 'wb') as fp:
            dill.dump(self.explainer_object, fp)

    def load_explainer(self, path: str):
        """
        Load the explainer

        Args:
            path (str): Path to load the explainer

        Returns:
            None
        """
        with open(path, 'rb') as fp:
            self.explainer_object = dill.load(fp)
