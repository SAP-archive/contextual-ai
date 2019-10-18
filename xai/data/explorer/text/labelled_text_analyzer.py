#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from copy import deepcopy

from nltk.tokenize import word_tokenize
from typing import Callable, Optional, Dict, List, Set
from typing import Tuple, Union

from xai.data.constants import TermFrequencyType
from xai.data.explorer.abstract_labelled_analyzer import AbstractLabelledDataAnalyzer
from xai.data.explorer.text.text_analyzer import TextDataAnalyzer
from xai.data.explorer.text.text_stats import TextStats


class LabelledTextDataAnalyzer(AbstractLabelledDataAnalyzer):
    def __init__(self, preprocess_fn: Optional[Callable[[str], str]] = None,
                 predefined_pattern: Optional[Dict[str, str]] = {},
                 tokenizer: Optional[Callable[[str], List[str]]] = word_tokenize,
                 stop_words: Optional[Set] = None,
                 stop_words_by_languages: Optional[List[str]] = None,
                 tf_type: Optional[int] = TermFrequencyType.TF_ABSOLUTE):
        """
        Initialize LabelledTextDataAnalyzer.

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
        super().__init__(data_analyzer_cls=TextDataAnalyzer)
        self._analyzer_cls_sample = TextDataAnalyzer(preprocess_fn=preprocess_fn,
                                                     predefined_pattern=predefined_pattern,
                                                     tokenizer=tokenizer,
                                                     stop_words=stop_words,
                                                     stop_words_by_languages=stop_words_by_languages,
                                                     tf_type=tf_type)
        self._all_analyzer = deepcopy(self._analyzer_cls_sample)

    def feed(self, value: Union[str, int], label: Union[str, int]):
        """
        Update the analyzer with value and its corresponding label

        Args:
            value: categorical value
            label: corresponding label for the categorical value
        """
        if label not in self._label_analyzer:
            self._label_analyzer[label] = deepcopy(self._analyzer_cls_sample)
        self._label_analyzer[label].feed(value)
        self._all_analyzer.feed(value)

    def get_statistics(self) -> Tuple[Dict[Union[str, int], TextStats], TextStats]:
        """
        Get stats based on labels

        Returns:
            A dictionary maps label to the aggregated stats obj
        """
        _stats = dict()
        _all_stats = self._all_analyzer.get_statistics()

        df = dict(_all_stats.document_frequency)
        total_doc_count = _all_stats.total_count
        for label, analyzer in self._label_analyzer.items():
            _stats[label] = analyzer.get_statistics(global_doc_frequency=df, total_doc_count=total_doc_count)

        return _stats, _all_stats
