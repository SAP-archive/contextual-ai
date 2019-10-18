#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import Dict, Optional, Tuple

from xai.data.abstract_stats import AbstractStats
from xai.data.constants import STATSKEY
from xai.data.exceptions import InvalidTypeError, InvalidSizeError


class TextStats(AbstractStats):
    """
    TextStats contains following basic information:

    """

    def __init__(self, total_count: Optional[int],
                 pattern_stats: Optional[Dict[str, Tuple[int, int]]] = None,
                 word_count: Optional[Dict[int, int]] = None,
                 char_count: Optional[Dict[int, int]] = None,
                 term_frequency: Optional[Dict[str, int]] = None,
                 document_frequency: Optional[Dict[str, int]] = None,
                 tfidf: Optional[Dict[str, int]] = None):
        """

        Args:
            total_count: total number of documents
            pattern_stats: a dict maps pattern to its frequency
            word_count: a dict maps term count per doc to its frequency
            char_count: a dict maps character count per doc to its frequency
            term_frequency: a dict maps the term to the total frequency count in the entire document set
            document_frequency: a dict maps the term to the number of documents that contains the term
            tfidf: a dict maps to the term to the average tf-idf
        """
        self.total_count = total_count
        self.pattern_stats = pattern_stats
        self.word_count = word_count
        self.char_count = char_count
        self.term_frequency = term_frequency
        self.document_frequency = document_frequency
        self.tfidf = tfidf

    @property
    def total_count(self):
        return self._total_count

    @total_count.setter
    def total_count(self, value: int):
        if type(value) != int:
            raise InvalidTypeError('total_count', type(value), '<int>')
        self._total_count = value

    @property
    def pattern_stats(self):
        return self._pattern_stats

    @pattern_stats.setter
    def pattern_stats(self, value: Dict[str, int]):
        if type(value) != dict:
            raise InvalidTypeError('pattern_stats', type(value), '<dict>')

        for name, count in value.items():
            if type(name) != str:
                raise InvalidTypeError('pattern_stats: key', type(name), '<str>')
            if type(count) != tuple:
                raise InvalidTypeError('pattern_stats: count', type(count), '<tuple>')
            if len(count) != 2:
                raise InvalidSizeError('pattern_stats: count', len(count), 2)
            if type(count[0]) != int:
                raise InvalidTypeError('pattern_stats: count: term_count', type(count[0]), '<int>')
            if type(count[1]) != int:
                raise InvalidTypeError('pattern_stats: count: document_count', type(count[1]), '<int>')

        self._pattern_stats = value

    @property
    def word_count(self):
        return self._word_count

    @word_count.setter
    def word_count(self, value: Dict[str, int]):
        if type(value) != dict:
            raise InvalidTypeError('word_count', type(value), '<dict>')

        for key, count in value.items():
            if type(key) != int:
                raise InvalidTypeError('word_count: key', type(key), '<int>')
            if type(count) != int:
                raise InvalidTypeError('word_count: count', type(count), '<int>')
        self._word_count = value

    @property
    def char_count(self):
        return self._char_count

    @char_count.setter
    def char_count(self, value: Dict[str, int]):
        if type(value) != dict:
            raise InvalidTypeError('char_count', type(value), '<dict>')

        for key, count in value.items():
            if type(key) != int:
                raise InvalidTypeError('char_count: key', type(key), '<int>')
            if type(count) != int:
                raise InvalidTypeError('char_count: count', type(count), '<int>')
        self._char_count = value

    @property
    def term_frequency(self):
        return self._term_frequency

    @term_frequency.setter
    def term_frequency(self, value: Dict[str, int]):
        if type(value) != dict:
            raise InvalidTypeError('term_frequency', type(value), '<dict>')

        for key, count in value.items():
            if type(key) != str:
                raise InvalidTypeError('term_frequency: key', type(key), '<str>')
            if type(count) != int:
                raise InvalidTypeError('term_frequency: count', type(count), '<int>')
        self._term_frequency = value

    @property
    def document_frequency(self):
        return self._document_frequency

    @document_frequency.setter
    def document_frequency(self, value: Dict[str, int]):
        if type(value) != dict:
            raise InvalidTypeError('document_frequency', type(value), '<dict>')

        for key, count in value.items():
            if type(key) != str:
                raise InvalidTypeError('document_frequency: key', type(key), '<str>')
            if type(count) != int:
                raise InvalidTypeError('document_frequency: count', type(count), '<int>')
        self._document_frequency = value

    @property
    def tfidf(self):
        return self._tfidf

    @tfidf.setter
    def tfidf(self, value: Dict[str, int]):
        if type(value) != dict:
            raise InvalidTypeError('tfidf', type(value), '<dict>')

        for key, count in value.items():
            if type(key) != str:
                raise InvalidTypeError('tfidf: key', type(key), '<str>')
            if type(count) not in [float, int]:
                raise InvalidTypeError('tfidf: score', type(count), '<float> or <int>')
        self._tfidf = value

    def to_json(self) -> Dict:
        """
        Map stats information into a json object

        Returns:
            A json that represent frequency count and total count
        """

        json_obj = dict()
        json_obj[STATSKEY.TOTAL_COUNT] = self._total_count
        json_obj[STATSKEY.PATTERN] = []
        for pattern_name in self._pattern_stats.keys():
            pattern_obj = dict()
            pattern_obj[STATSKEY.PATTERN.PATTERN_NAME] = pattern_name
            pattern_obj[STATSKEY.PATTERN.PATTERN_TF] = self._pattern_stats[pattern_name][0]
            pattern_obj[STATSKEY.PATTERN.PATTERN_DF] = self._pattern_stats[pattern_name][1]
            json_obj[STATSKEY.PATTERN].append(pattern_obj)

        json_obj[STATSKEY.TF] = self._term_frequency
        json_obj[STATSKEY.DF] = self._document_frequency
        json_obj[STATSKEY.TFIDF] = self._tfidf

        return json_obj
