from abc import ABC, abstractmethod
from typing import List, Dict

import numpy as np


# TODO * decide on initialisation specification
# TODO * decide on methods
# TODO * decide on specifications of each method (inputs, input types, outputs, and output types)

class AbstractExplainer(ABC):
    # FIXME | why is the constant outside of __init__? Seems like not-good practice
    TOP_EXPLAIN_FEATURES = 5

    def __init__(self, explainer_name: str, class_names: List[str], feature_names: List[str],
                 categorical_dict: Dict[list]):
        # FIXME | no doc strings
        # FIXME | feature_names, categorical_dict are not required for text explainers
        # FIXME | class_names should be optional
        # FIXME | explainer_name should be optional
        self.explainer_name = explainer_name

        self.class_names = class_names
        self.feature_names = feature_names
        self.categorical_dict = categorical_dict

        self.explainer = None
        self.predict_fn = None
        self.train_data = None

    @abstractmethod
    def initialize_explainer(self, predict_fn, train_data: np.array):
        raise NotImplementedError("Derived class should implement this")

    @abstractmethod
    def explain_instance(self, sample, num_features=TOP_EXPLAIN_FEATURES) -> str:
        raise NotImplementedError("Derived class should implement this")

    @abstractmethod
    def save_explainer(self, path: str) -> bool:
        """
        Saves the explainer to disk.

        Args:
            path (str): Path to which the explainer is stored

        Returns:
            (bool) Whether saving the explainer was successful or not
        """
        raise NotImplementedError("Derived class should implement this")

    @abstractmethod
    def load_explainer(self, path: str) -> bool:
        """
        Loads the explainer from disk.

        Args:
            path (str): Path to the explainer

        Returns:
            (bool) Whether the explainer was successfully loaded or not

        Notes:
            load_explainer should not return the explainer, but it should instead load the
            AbstractExplainer instance with the explainer (e.g. set the self.explainer to the loaded
            object)
        """
        # TODO what is this?
        raise NotImplementedError("Derived class should implement this")
