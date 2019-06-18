from typing import List
from collections import defaultdict
import numpy as np


class ConfusionMatrix:
    def __init__(self, label: List[str], confusion_matrix: List[List[float]]):
        self.label = label
        self.confusion_matrix = confusion_matrix

    def get_values(self):
        return self.confusion_matrix

    def get_labels(self):
        return self.label

    def get_top_k_similar_classes(self, k):
        if k > len(self.confusion_matrix):
            print('Error: N exceeds the class numbers.')
            k = 3
        values = np.array(self.confusion_matrix)
        similar_class = defaultdict(list)
        for idx, label in enumerate(self.label):
            predicted_distribution = values[:, idx]
            args = np.argsort(predicted_distribution)
            for i in range(k):
                sim_idx = args[-i]
                if values[sim_idx,idx] == 0:
                    continue
                similar_class[(self.label[idx])].append(
                    (self.label[sim_idx], values[:, [idx, sim_idx]][[idx, sim_idx], :]))
        return similar_class

    def get_top_k_unsimilar_classes(self, k):
        if k > len(self.confusion_matrix):
            print('Error: N exceeds the class numbers.')
            k = 3
        values = np.array(self.confusion_matrix)
        unsimilar_class = defaultdict(list)
        for idx, label in enumerate(self.label):
            predicted_distribution = values[:, idx]
            args = np.argsort(predicted_distribution)
            for i in range(k):
                unsim_idx = args[i]
                unsimilar_class[(self.label[idx])].append(
                    (self.label[unsim_idx], values[:, [idx, unsim_idx]][[idx, unsim_idx], :]))
        return unsimilar_class
