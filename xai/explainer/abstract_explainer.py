import time
from abc import ABC, abstractmethod
import numpy as np
from typing import List, Dict

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
    def decode_explaination(self, exp, sample, score) -> str:
        # TODO what is decoding for?
        raise NotImplementedError("Derived class should implement this")

    @abstractmethod
    def save_to_file(self):
        # TODO what is this?
        raise NotImplementedError("Derived class should implement this")

    @abstractmethod
    def load_from_file(self):
        # TODO what is this?
        raise NotImplementedError("Derived class should implement this")

    def explain_instance_with_log(self, sample, predict_fn, num_features=TOP_EXPLAIN_FEATURES):
        # FIXME | shouldn't implement anything in the abstract class
        print("---------------- Explanations from %s ----------------------" % self.explainer_name)
        print('Score:', predict_fn(sample.reshape(1, -1)))
        print("Start explaining...")
        start_time = time.time()
        exp = self.explain_instance(sample, predict_fn, num_features=num_features)
        t = time.time() - start_time
        print("Explainations:")
        print(self.decode_explaination(exp))
        print("Finish explaining!! Time consumed: %s sec. (feature number: %s)" % (t, sample.shape[0]))
        print("================================================================")
        return exp
