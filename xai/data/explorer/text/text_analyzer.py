#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import math
from collections import Counter
from collections import defaultdict

import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from typing import Callable, Optional, Dict, List, Set

from xai.data.constants import TermFrequencyType
from xai.data.exceptions import InvalidTypeError, UndefinedRequiredParams
from xai.data.explorer.abstract_analyzer import AbstractDataAnalyzer
from xai.data.explorer.text.text_stats import TextStats


class TextDataAnalyzer(AbstractDataAnalyzer):
    """
    This analyzer class analyzes text data and calculates the TF-IDF, TF for the input corpus,
    and percentage of pre-defined patterns
    """

    def __init__(self, preprocess_fn: Optional[Callable[[str], str]] = None,
                 predefined_pattern: Optional[Dict[str, str]] = {},
                 tokenizer: Optional[Callable[[str], List[str]]] = word_tokenize,
                 stop_words: Optional[Set] = None,
                 stop_words_by_languages: Optional[List[str]] = None,
                 tf_type: Optional = TermFrequencyType.TF_ABSOLUTE):
        """
        Initialize TextDataAnalyzer

        Args:
            preprocess_fn: the function that pre-processes the text, returns the processed text
            predefined_pattern: the dictionary maps a pattern name to its regex string
            tokenizer: the function tokenize a text into a list of tokens, the default tokenizer is the `word_tokenize`
                       in nltk.tokenize
            stop_words: the set of stop words that will be ignored in the final stats
            stop_words_by_languages: a list of language code (from nltk.corpus) to determine the stop words set by languages.
                                     Supported by `nltk.corpus.stopwords`. If `stop_words` is not None, it will be ignored.
            tf_type: how the term frequency is calculated, default is
                    - TF_ABSOLUTE: the occurrence of t in document d, i.e. f(t,d)
                    - TF_BOOLEAN: 1 if term appeared in the document, otherwise 0
                    - TF_NORMALIZE_BY_MAX: f(t,d) normalized by the maximum term frequency
                    - TF_NORMALIZE_BY_DOC: f(t,d) normalized by the total number of terms in the document
                    - TF_LOGARITHM: log (1+ f(t,d))
                    - TF_AUGMENTED: 0.5 + 0.5 * (f(t,d) / max(f(t',d)) for t' in d)
        """
        super(TextDataAnalyzer, self).__init__()

        def processing(text):
            if preprocess_fn is not None:
                text = preprocess_fn(text)
            pattern_count = dict()
            for pattern_name, pattern_regex in predefined_pattern.items():
                pattern_count[pattern_name] = len(re.findall(pattern_regex, text, re.MULTILINE))
            tokens = tokenizer(text)
            return tokens, pattern_count, text

        self.preprocessor = processing

        if stop_words is None:
            stop_words = set()
            if stop_words_by_languages is not None:
                for lang in stop_words_by_languages:
                    stop_words.update(stopwords.words(lang))
        self.stop_words = frozenset(stop_words)

        self._total_count = 0
        self._pattern_occurrence_counter = defaultdict(int)
        self._pattern_document_counter = defaultdict(int)
        self._word_counter = defaultdict(int)
        self._character_counter = defaultdict(int)
        self._absolute_term_frequency = Counter()
        self._term_frequency = Counter()
        self._document_frequency = Counter()
        if tf_type not in [TermFrequencyType.TF_ABSOLUTE, TermFrequencyType.TF_BOOLEAN,
                           TermFrequencyType.TF_NORMALIZED_BY_DOC, TermFrequencyType.TF_NORMALIZED_BY_MAX,
                           TermFrequencyType.TF_LOGARITHM, TermFrequencyType.TF_AUGMENTED]:
            raise InvalidTypeError(tf_type, 'tf_type', '<one of the TermFrequencyType>')
        self.tf_type = tf_type

    def feed(self, doc):
        """
        Feed document text string to analyzer for stats analysis

        Args:
            doc: one document text string that will be analysed in the analyzer
        """

        tokens, pattern_counter, doc = self.preprocessor(doc)

        # update pattern count
        for pattern_name, pattern_count in pattern_counter.items():
            self._pattern_occurrence_counter[pattern_name] += pattern_count
            if pattern_count > 0:
                self._pattern_document_counter[pattern_name] += 1

        # update word count and char count
        self._word_counter[len(tokens)] += 1
        self._character_counter[len(doc)] += 1

        # get tf per doc
        word_counter = Counter(tokens)
        for word in self.stop_words:
            del word_counter[word]

        if self.tf_type == TermFrequencyType.TF_ABSOLUTE:
            tf = word_counter
        elif self.tf_type == TermFrequencyType.TF_BOOLEAN:
            tf = Counter(word_counter.keys())
        elif self.tf_type == TermFrequencyType.TF_NORMALIZED_BY_MAX:
            max_tf = max(word_counter.values())
            tf = {w: f / max_tf for w, f in word_counter.items()}
        elif self.tf_type == TermFrequencyType.TF_NORMALIZED_BY_DOC:
            num_tokens = len(tokens)
            tf = {w: f / num_tokens for w, f in word_counter.items()}
        elif self.tf_type == TermFrequencyType.TF_LOGARITHM:
            tf = {w: math.log(1 + f) for w, f in word_counter.items()}
        elif self.tf_type == TermFrequencyType.TF_AUGMENTED:
            max_tf = max(word_counter.values())
            tf = {w: (0.5 + 0.5 * (f / max_tf)) for w, f in word_counter.items()}

        # update tf and df
        self._term_frequency.update(tf)
        self._absolute_term_frequency.update(word_counter)
        self._document_frequency.update(word_counter.keys())
        self._total_count += 1

    def get_statistics(self, global_doc_frequency: Optional[Dict[str, int]] = None,
                       total_doc_count: Optional[int] = None) -> TextStats:
        """
        Map stats information into a json object

        Args:
            global_doc_frequency: a dictionary maps term to the count of documents globally that contain the term.
                    Default is None, the tfidf will be calculated with the accumulated document frequency.
            total_doc_count: total number of documents corresponding to the global_doc_frequency

        Returns:
            A json that represents frequency count and total count
        """
        tfidf = dict()
        if global_doc_frequency is None:
            for word in self._term_frequency.keys():
                tfidf[word] = self._term_frequency[word] * math.log(
                    self._total_count / self._document_frequency[word]) / self._total_count
        else:
            if total_doc_count is None:
                raise UndefinedRequiredParams('total_doc_count')
            for word in global_doc_frequency.keys():
                if word in self._term_frequency:
                    tfidf[word] = self._term_frequency[word] * math.log(
                        total_doc_count / global_doc_frequency[word]) / self._total_count
                else:
                    tfidf[word] = 0
            for word in global_doc_frequency.keys():
                document_frequency = dict()
                document_frequency[word] = self._document_frequency[word] if word in self._document_frequency else 0

        pattern_stats = dict()
        for pattern_name in self._pattern_occurrence_counter.keys():
            pattern_stats[pattern_name] = (
                self._pattern_occurrence_counter[pattern_name], self._pattern_document_counter[pattern_name])
        stats = TextStats(total_count=self._total_count, pattern_stats=pattern_stats,
                          word_count=dict(self._word_counter), char_count=dict(self._character_counter),
                          term_frequency=dict(self._absolute_term_frequency),
                          document_frequency=dict(self._document_frequency),
                          tfidf=tfidf)
        return stats
