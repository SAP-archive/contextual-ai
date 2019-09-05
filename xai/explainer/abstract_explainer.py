import time
from abc import ABC, abstractmethod
import numpy as np
from typing import List, Dict


class AbstractExplainer(ABC):
    TOP_EXPLAIN_FEATURES = 5

    def __init__(self, explainer_name: str, class_names: List[str], feature_names: List[str],
                 categorical_dict: Dict):
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
        raise NotImplementedError("Derived class should implement this")

    @abstractmethod
    def save_to_file(self):
        raise NotImplementedError("Derived class should implement this")

    @abstractmethod
    def load_from_file(self):
        raise NotImplementedError("Derived class should implement this")

    def explain_instance_with_log(self, sample, predict_fn, num_features=TOP_EXPLAIN_FEATURES):
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
