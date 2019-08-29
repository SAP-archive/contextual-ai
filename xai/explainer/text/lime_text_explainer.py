import logging
from typing import List, Optional, Callable, Dict

import dill
import numpy as np
from lime.lime_text import LimeTextExplainer as OriginalLimeTextExplainer

from ..abstract_explainer import AbstractExplainer
from ..explainer_exceptions import ExplainerUninitializedError
from ..utils import explanation_to_json

LOGGER = logging.getLogger(__name__)

NUM_TOP_FEATURES = 5


class LimeTextExplainer(AbstractExplainer):

    def __init__(self):
        super(LimeTextExplainer, self).__init__()

    def build_explainer(self, kernel_width: float = 25,
                        verbose: bool = False,
                        class_names: Optional[List[str]] = None,
                        feature_selection: str = 'auto',
                        split_expression: str = '\W+',
                        bow: bool = True):
        """
        Build the LIME text explainer
        For now, the parameters used to instantiate this class are exactly those of
        lime.lime_text.LimeTextExplainer. Original documentation can be found here:
        https://lime-ml.readthedocs.io/en/latest/lime.html#lime.lime_text.LimeTextExplainer

        Args:
            kernel_width (float): Width of the exponential kernel used in the LIME loss function
            verbose (bool): Control verbosity. If true, local prediction values of the LIME model
                are printed
            class_names (list): Class names (positional index corresponding to class index)
            feature_selection (str): Feature selection method. See original docs for more details
            split_expression (str): Regex expression for splitting the text
            bow (bool):  if True (bag of words), will perturb input data by removing all ocurrences of
                individual words. Explanations will be in terms of these words. Otherwise,
                will explain in terms of word-positions, so that a word may be important the
                first time it appears and unimportant the second. Only set to false if the
                classifier uses word order in some way (bigrams, etc).

        Returns:
            None
        """
        self.explainer_object = OriginalLimeTextExplainer(
            kernel_width=kernel_width,
            verbose=verbose,
            class_names=class_names,
            feature_selection=feature_selection,
            split_expression=split_expression,
            bow=bow
        )

        if verbose:
            LOGGER.info('Explainer built successfully!')

    def explain_instance(self, predict_fn: Callable,
                         instance: np.ndarray,
                         labels: List = (1,),
                         top_labels: Optional[int] = None,
                         num_features: Optional[int] = NUM_TOP_FEATURES,
                         num_samples: int = 5000,
                         distance_metric: str = 'cosine') -> Dict[int, Dict]:
        """
        Explain a prediction instance using the LIME text explainer.
        Like with `build_explainer`, the parameters of `explain_instance` are exactly those of
        lime.lime_text.LimeTextExplainer.explain_instance.
        More documentation can be found at:
        https://lime-ml.readthedocs.io/en/latest/lime.html#lime.lime_text.LimeTextExplainer.explain_instance

        Args:
            predict_fn (Callable): A function that takes in a 1D numpy array and outputs a vector
                of probabilities which should sum to 1.
            instance (np.ndarray): A 1D numpy array corresponding to a row/single example
            labels (list): The list of class indexes to produce explanations for
            top_labels (int): If not None, this overwrites labels and the explainer instead produces
                explanations for the top k classes
            num_features (int): Number of features to include in an explanation
            num_samples (int): The number of perturbed samples to train the LIME model with
            distance_metric (str): The distance metric to use for weighting the loss function

        Returns:
            (dict) A mapping of class to explanations

        Raises:
            ExplainerUninitializedError: Raised if self.explainer_object is None
        """
        if self.explainer_object:
            explanation = self.explainer_object.explain_instance(
                text_instance=instance,
                classifier_fn=predict_fn,
                labels=labels,
                top_labels=top_labels,
                num_features=num_features,
                num_samples=num_samples,
                distance_metric=distance_metric
            )

            if top_labels:
                labels_to_extract = list(explanation.as_map().keys())
            else:
                labels_to_extract = labels

            confidences = explanation.predict_proba

            return explanation_to_json(explanation, labels_to_extract, confidences)
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
