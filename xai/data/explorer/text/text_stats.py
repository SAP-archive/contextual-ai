from typing import Dict, List, Tuple
import math
import operator
import numpy as np
from collections import defaultdict, Counter
from xai.data.constants import STATSKEY, STATSCONSTANTS
from xai.data.exceptions import NoItemsError
from xai.data.explorer.abstract_stats import AbstractStats


class TextStats(AbstractStats):
    """
    TextStats contains following basic information:

    """

    def __init__(self):
        self._total_count = 0
        self.pattern_occurrence_counter = defaultdict(int)
        self.pattern_document_counter = defaultdict(int)
        self.word_counter = defaultdict(int)
        self.character_counter = defaultdict(int)
        self.term_frequency = Counter()
        self.document_frequency = Counter()
        self._TFIDF = dict()

    def update_pattern_counters(self, pattern_counter_per_doc: Dict[str, int]):
        for pattern_name, pattern_count in pattern_counter_per_doc.items():
            self.pattern_occurence_counter[pattern_name] += pattern_count
            if pattern_count > 0:
                self.pattern_document_counter[pattern_name] += 1

    def update_length_counters(self, word_count: int, char_count: int):
        self.word_counter[word_count] += 1
        self.character_counter[char_count] += 1

    def update_term_and_document_frequency(self, token_counter: Counter):
        self.term_frequency.update(token_counter)
        self.document_frequency.update(token_counter.keys())

    def update_document_total_count(self, increment_by: int):
        self._total_count += increment_by

    def get_tfidf(self):
        tfidf = dict()
        for word in self.term_frequency.keys():
            tfidf[word] = self.term_frequency[word] * math.log(
                self._total_count / self.document_frequency[word])

        self._TFIDF = {word: tfidf for word, tfidf in sorted(tfidf.items(), key=operator.itemgetter(1), reverse=True)}
        return self._TFIDF

    def get_total_count(self) -> int:
        """
        return the total count of values for the stats object

        Returns:
            total count of values
        """
        return self._total_count

    def to_json(self) -> Dict:
        """
        map stats information into a json object

        Returns:
            a json that represent frequency count and total count
        """

        json_obj = dict()
        json_obj[STATSKEY.TOTAL_COUNT] = self._total_count
        json_obj[STATSKEY.PATTERN] = []
        for pattern_name in self.pattern_occurrence_counter.keys():
            pattern_obj = dict()
            pattern_obj[STATSKEY.PATTERN.PATTERN_NAME] = pattern_name
            pattern_obj[STATSKEY.PATTERN.PATTERN_TF] = self.pattern_occurrence_counter[pattern_name]
            pattern_obj[STATSKEY.PATTERN.PATTERN_DF] = self.pattern_document_counter[pattern_name]
            json_obj[STATSKEY.PATTERN].append(pattern_obj)

        json_obj[STATSKEY.TFIDF] = self.get_tfidf()

        return json_obj
