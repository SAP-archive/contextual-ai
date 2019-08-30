import re
from typing import Callable, Optional, Dict, List, Set
from collections import Counter
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
        self.stats = TextStats()

    def feed(self, doc):
        """
        feed document text string to analyzer for stats analysis
        Args:
            doc: one document text string that will be analysed in the analyzer
        """

        tokens, pattern_count, doc = self.preprocessor(doc)
        self.stats.update_pattern_counters(pattern_counter_per_doc=pattern_count)
        self.stats.update_length_counters(word_count=len(tokens), char_count=len(doc))

        word_counter = Counter(tokens)
        for word in self.stop_words:
            del word_counter[word]

        self.stats.update_term_and_document_frequency(word_counter=word_counter)
        self.stats.update_document_total_count(increment_by=1)

    def feed_all(self, docs):
        for doc in docs:
            self.feed(doc)

    def get_statistics(self)->Dict:
        """
        map stats information into a json object

        Returns:
            a json that represent frequency count and total count
        """
        return self.stats.to_json()




