import math
import operator
import re
from collections import Counter
from collections import defaultdict
from typing import Callable, Optional, Dict, List, Set

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from xai.data.explorer.abstract_analyzer import AbstractDataAnalyzer
from xai.data.explorer.text.text_stats import TextStats


class TextDataAnalyzer(AbstractDataAnalyzer):
    """
    TextDataAnalyzer calculates the TF-IDF, TF for the input corpus, and percentage of pre-defined patterns
    """

    def __init__(self, preprocess_fn: Optional[Callable[[str], str]] = None,
                 predefined_pattern: Optional[Dict[str, str]] = {},
                 tokenizer: Optional[Callable[[str], List[str]]] = word_tokenize,
                 stop_words: Optional[Set] = None,
                 stop_words_by_languages: Optional[List[str]] = None):
        """
        initialize TextDataAnalyzer
        Args:
            preprocess_fn: the function that pre-processes the text, returns the processed text
            predefined_pattern: the dictionary maps a pattern name to its regex string
            tokenizer: the function tokenize a text into a list of tokens, the default tokenizer is the `word_tokenize`
                       in nltk.tokenize
            stop_words: the set of stop words that will be ignored in the final stats
            stop_words_by_languages: a list of language code (from nltk.corpus) to determine the stop words set by languages.
                                     Supported by `nltk.corpus.stopwords`. If `stop_words` is not None, it will be ignored.
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

        self.processor = processing

        if stop_words is None:
            stop_words = set()
            for lang in stop_words_by_languages:
                stop_words.update(stopwords.words(lang))
        self.stop_words = frozenset(stop_words)

        self._total_count = 0
        self._pattern_occurrence_counter = defaultdict(int)
        self._pattern_document_counter = defaultdict(int)
        self._word_counter = defaultdict(int)
        self._character_counter = defaultdict(int)
        self._term_frequency = Counter()
        self._document_frequency = Counter()
        self.stats = None

    def feed(self, doc):
        """
        feed document text string to analyzer for stats analysis
        Args:
            doc: one document text string that will be analysed in the analyzer
        """

        tokens, pattern_count, doc = self.preprocessor(doc)

        # update pattern count
        for pattern_name, pattern_count in pattern_count.items():
            self.pattern_occurence_counter[pattern_name] += pattern_count
            if pattern_count > 0:
                self._pattern_document_counter[pattern_name] += 1

        # update word count and char count
        self._word_counter[len(tokens)] += 1
        self._character_counter[len(doc)] += 1

        # get tf per doc
        word_counter = Counter(tokens)
        for word in self.stop_words:
            del word_counter[word]

        # update tf and df
        self._term_frequency.update(word_counter)
        self._document_frequency.update(word_counter.keys())
        self._total_count += 1

    def get_statistics(self) -> TextStats:
        """
        map stats information into a json object

        Returns:
            a json that represent frequency count and total count
        """
        tfidf = dict()
        for word in self._term_frequency.keys():
            self.tfidf[word] = self._term_frequency[word] * math.log(
                self._total_count / self._document_frequency[word])

        TFIDF = {word: tfidf for word, tfidf in sorted(tfidf.items(), key=operator.itemgetter(1), reverse=True)}

        pattern_stats = dict()
        for pattern_name in self._pattern_occurrence_counter.keys():
            pattern_stats[pattern_name] = (
                self._pattern_occurrence_counter[pattern_name], self._pattern_document_counter[pattern_name])
        self.stats = TextStats(total_count=self._total_count, pattern_stats=pattern_stats,
                               word_count=self._word_counter, char_count=self._character_counter,
                               term_frequency=self._term_frequency, document_frequency=self._document_frequency,
                               tfidf=TFIDF)
        return self.stats
