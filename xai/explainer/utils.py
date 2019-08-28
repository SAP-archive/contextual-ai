from typing import List, Dict

import numpy as np
from lime.explanation import Explanation


def explanation_to_json(explanation: Explanation,
                         labels: List[int],
                         confidences: np.ndarray) -> Dict[int, Dict]:
    """
    Parses LIME explanation to produce JSON-parseable output format.

    Args:
        explanation (lime.explanation.Explanation): The explanation output from LIME
        labels (list): List of labels for which to get explanations
        confidences (np.ndarray): Model output for a particular instance, which should be a list
            of confidences that sum to one

    Returns:
        (dict) Explanations in JSON format
    """
    dict_explanation = {}

    for label in labels:
        list_explanations = explanation.as_list(label)
        tmp = []
        for exp in list_explanations:
            tmp.append({'feature': exp[0], 'score': exp[1]})
        dict_explanation[label] = {
            'confidence': confidences[label],
            'explanation': tmp
        }

    return dict_explanation
