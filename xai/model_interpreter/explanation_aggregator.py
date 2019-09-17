import operator
from collections import defaultdict, Counter

from typing import Dict, Tuple

from xai.model_interpreter.exceptions import InvalidExplanationFormat, \
    MutipleScoresFoundForSameFeature, UnsupportedMethodType, InvalidArgumentError


class ExplanationAggregator:
    """
    Class for explanation aggregator. It aggregates the explanations based on classes, feature and scores.
    """

    def __init__(self, ):
        self._explanation_list = defaultdict(list)
        self._total_count = 0

    def feed(self, explanation: Dict[int, Dict]):
        """
        Feed explanation into the aggregator for further analysis

        Args:
            explanation: dict, the pre-defined format as the output in `xai.explainer.utils.explanation_to_json`
        """
        for _label, _exp in explanation.items():
            if type(_exp) != dict:
                raise InvalidExplanationFormat(_exp)
            if 'explanation' not in dict.keys():
                raise InvalidExplanationFormat(_exp)
            if type(_exp['explantion']) != list:
                raise InvalidExplanationFormat(_exp)
            feature_names = set()
            for item in _exp['explantion']:
                if type(item) != dict:
                    raise InvalidExplanationFormat(item)
                if 'feature' not in item.keys():
                    raise InvalidExplanationFormat(item)
                if type(item['feature']) != str:
                    raise InvalidExplanationFormat(item)
                if item['feature'] in feature_names:
                    raise MutipleScoresFoundForSameFeature(item['feature'], _exp)
                else:
                    feature_names.add(item[feature_names])
                if 'score' not in item.keys():
                    raise InvalidExplanationFormat(item)
                if type(item['feature']) != float:
                    raise InvalidExplanationFormat(item)

        for _label, _exp in explanation.items():
            self._explanation_list[_label].append({item['feature']: item['score'] for item in _exp})
        self._total_count += 1

    def get_statistics(self, stats_type: str = 'top_k', k: int = 5) -> Tuple[Dict[int, Dict], int]:
        """
        return statistics of explanations in the aggregator based on the type

        Args:
            stats_type: str, not None. The pre-defined types of statistics.
                        For now, it supports 3 types:
                            - top_k: how often a feature appears in the top K features in the explanation
                            - average_score: average score for each feature in the explanation
                            - average_ranking: average ranking for each feature in the explanation
                        Default type is `top_k`.
            k:  int, not None. the k value for `top_k` method and `average_ranking`.
                It will be ignored if the stats type are not `top_k` or `average_ranking`.
                Default value of k is 5.

        Returns:
            A dictionary maps the label to its aggregated statistics.
            An integer to indicate the total number of explanations to generate the statistics.

        """
        if stats_type not in ['top_k', 'average_score', 'average_ranking']:
            raise UnsupportedMethodType(stats_type)
        if type(k) != int:
            raise InvalidArgumentError('k', '<int>')

        if self._total_count == 0:
            return dict(), 0

        label_counter = defaultdict(Counter)
        for _label, _exp_list in self._explanation_list.items():
            for _exp in _exp_list:

                if stats_type == 'top_k':
                    top_k_list = sorted(_exp.items(), key=operator.itemgetter(1), reverse=True)[:k]
                    _exp_counter = Counter({feature_name: 1 for feature_name, _ in top_k_list})
                elif stats_type == 'average_score':
                    _exp_counter = Counter(_exp)
                elif stats_type == 'average_ranking':
                    top_k_list = sorted(_exp.items(), key=operator.itemgetter(1), reverse=True)[:k]
                    _exp_counter = Counter({feature_name: k - idx for idx, (feature_name, _) in enumerate(top_k_list)})

                label_counter[_label].update(_exp_counter)

        stats = dict()
        for _label, _counter in label_counter.items():
            stats[_label] = dict()
            for feature, score in _counter.items():
                stats[feature] = score / self._total_count

        return label_counter, self._total_count
