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

    def get_top_k_similar_classes(self, k, top_n_class=10, tf_thresdhold=0.8):
        if k > len(self.confusion_matrix):
            print('Error: N exceeds the class numbers.')
            k = 1
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
                print('Class [%s] is well classified, ignored in finding similar class.' % self.label[targeted_class])
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


if __name__ == "__main__":
    labels = [
        "CI_5",
        "CI_3",
        "CA_1",
        "CI_4",
        "CI_1",
        "CI_57",
        "CI_7",
        "CI_6",
        "CI_8",
        "CI_276",
        "CI_49",
        "CI_2"
    ]
    values = [[10, 1, 0, 68, 29, 0, 4, 10, 0, 0, 12, 0],
              [0, 696, 0, 91, 34, 0, 37, 9, 0, 0, 10, 6],
              [0, 5, 35, 16, 25, 0, 25, 3, 0, 0, 8, 5],
              [0, 45, 0, 390, 62, 0, 36, 14, 0, 0, 15, 12],
              [0, 52, 2, 230, 279, 0, 61, 39, 0, 0, 42, 6],
              [0, 0, 0, 2, 0, 0, 48, 1, 0, 0, 79, 0],
              [0, 1, 0, 15, 10, 0, 567, 6, 0, 0, 15, 2],
              [0, 29, 0, 86, 49, 0, 48, 187, 0, 0, 15, 14],
              [0, 23, 0, 37, 36, 0, 42, 5, 0, 0, 11, 1],
              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 5, 0, 45, 6, 0, 0, 888, 0],
              [1, 30, 1, 35, 13, 0, 15, 16, 0, 0, 5, 233]]

    cm = ConfusionMatrix(label=labels, confusion_matrix=values)
    cm.get_top_k_similar_classes(2)
