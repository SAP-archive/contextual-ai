from nltk.tokenize import RegexpTokenizer, word_tokenize
from collections import Counter
from collections import defaultdict
import math
import re
import operator
from nltk.corpus import stopwords
from plugin.xai.data_explorer.abstract_analyzer import AbstractAnalyzer
from plugin.xai.data_explorer.sequence_length_analyzer import SequenceLengthAnalyzer
from plugin.xai import constants


class TextAnalyzer(AbstractAnalyzer):
    def __init__(self, feature_list):
        super(TextAnalyzer, self).__init__(feature_list=feature_list)
        self.summary_info = defaultdict(TextHelper)
        self.derived_length_distribution = dict()

    def analyze_sample(self, sample, label_value):
        for feature_key in self.feature_list:
            if feature_key in sample:
                feature_value = sample[feature_key]
                if type(feature_value) == list:
                    for feature_list_value in feature_value:
                        self.summary_info[feature_key].update_tf_idf_items(feature_list_value, label_value)
                else:
                    self.summary_info[feature_key].update_tf_idf_items(feature_value, label_value)

    def aggregate(self):
        for fea in self.summary_info.keys():
            tf_idf = self.summary_info[fea].get_tfidf(limit=TextHelper.TFIDF_TOP_N)
            text_length = self.summary_info[fea].get_text_length_distribution()
            word_count = self.summary_info[fea].get_word_count_num_distribution()

            self.summary_info[fea] = tf_idf
            self.derived_length_distribution['%s_textlength' % fea] = text_length
            self.derived_length_distribution['%s_wordcount' % fea] = word_count

    def summarize_info(self):
        length_analyzer = SequenceLengthAnalyzer(self.derived_length_distribution.keys())
        length_analyzer.summary_info = self.derived_length_distribution
        length_analyzer.aggregate()

        info = {constants.KEY_TEXT_FEATURE_DISTRIBUTION: self.summary_info}
        info.update(length_analyzer.summarize_info())
        return info


class TextHelper:
    TFIDF_TOP_N = 200

    def __init__(self, stopwords_fpath=None):
        self.tf = defaultdict(Counter)
        self.idf = defaultdict(Counter)
        self.tfidf = defaultdict(dict)
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stopwordsset = self.get_stop_words(stopwords_fpath)
        self.class_doc_num = defaultdict(int)
        self.textlength = defaultdict(lambda: defaultdict(int))
        self.wordcount = defaultdict(lambda: defaultdict(int))

    def pre_process(self, text):
        '''
        Cleans an input string using the following steps [from COE]
        :return: 
        '''

        def regex_replace(text, pattern, replaced, regex=True):
            if regex:
                text = re.sub(pattern, replaced, text)
            else:
                text = text.replace(pattern, replaced)
            return text

        text = text.lower()
        text = regex_replace(text, r"\s+", " ")
        text = text.encode("utf8", errors="ignore").decode("utf8")
        text = regex_replace(text, "-", "", regex=False)
        text = regex_replace(text, "\`", "", regex=False)  # remove apostrophe
        text = regex_replace(text, "\'", "", regex=False)  # remove apostrophe
        text = regex_replace(text, r"\S*@\S*", " EMAIL ")
        text = regex_replace(text, r"(http\S+|http\S+)", " URL ")
        text = regex_replace(text, "_", " ", regex=False)

        text = regex_replace(text, r"(\d+\/\d+\/?\d*|\d+\.\d+\.?\d*|\d+\\\d+\\?\d*)", " DATE ")
        text = regex_replace(text, r"\d+:\d+:?\d*", " TIME ")
        text = regex_replace(text, r"(\d+\.\d+|\d+\,\d+|\+\d+|(?<=\s|\.|,)\d+|\d+(?=\s|\.|,)|\#\d+\b|\+\d+\b)",
                             " NUMBER ")
        text = regex_replace(text, r"(?<=\w)([^\w\.,\s\:\/\\+])(?=\w+)", "")
        text = regex_replace(text, r"\,(?=\w\D)", ", ")
        text = regex_replace(text, r"\.(?=\w\D)", ". ")

        # text = regex_replace(text,r"\w*\d\w*", " <code> ")  # words with numbers in between
        # text = regex_replace(text,r"\w+[^\w\s]\w+", " <code> ")  # words with symbols in between
        # text = regex_replace(text,r"\w+([^\w\s]+\w+)+", " <code> ") # words with symbols in between

        # text = regex_replace(text,r"[^\w\s<>]", " ")  # replace non-alphanumerical chars (unicode) with space

        text = regex_replace(text, r"([^\w\s])", " ")

        text = regex_replace(text, r"((?<=\D)\d+(?=\D)|\d+(?=\D)|(?<=\D)\d+)", " NUMBER ")
        text = regex_replace(text, r"\b\d+\b", " NUMBER ")
        text = regex_replace(text, r" +", " ")  # remove extra spaces

        text = text.strip()
        return text

    def get_stop_words(self, stop_file_path):
        """load stop words """
        stop_words_set = set()
        if stop_file_path is None:
            supported_languanges = ['english', 'german']
            for lang in supported_languanges:
                stop_words_set.update(stopwords.words(lang))
            return frozenset(stop_words_set)
        with open(stop_file_path, 'r', encoding="utf-8") as f:
            stopwordslines = f.readlines()
            stop_set = set(m.strip() for m in stopwordslines)
            return frozenset(stop_set)

    def get_word_count_from_doc(self, doc, class_label):
        doc = self.pre_process(doc)
        word_count_vector = Counter(word_tokenize(doc))
        # word_count_vector = Counter(self.tokenizer.tokenize(text=doc))

        num_word_count = sum(word_count_vector.values())
        self.textlength['all'][len(doc)] += 1
        self.wordcount['all'][num_word_count] += 1

        if class_label != 'all':
            self.textlength[class_label][len(doc)] += 1
            self.wordcount[class_label][num_word_count] += 1

        for word in self.stopwordsset:
            del word_count_vector[word]
        for word in ['NUMBER','EMAIL','TIME','DATE','URL']:
            del word_count_vector[word]

        return word_count_vector

    def update_tf_idf_items(self, doc, class_label):
        word_count_vector = self.get_word_count_from_doc(doc, class_label)
        doc_count_vector = Counter(list(word_count_vector.keys()))

        self.tf['all'].update(word_count_vector)
        self.idf['all'].update(doc_count_vector)
        self.class_doc_num['all'] += 1

        if class_label != 'all':
            self.tf[class_label].update(word_count_vector)
            self.idf[class_label].update(doc_count_vector)
            self.class_doc_num[class_label] += 1

    def update_tfidf(self):
        self.tfidf = dict()
        for class_label in self.tf.keys():
            self.tfidf[class_label] = dict()
            for word in self.tf[class_label].keys():
                self.tfidf[class_label][word] = self.tf[class_label][word] * math.log(
                    self.class_doc_num['all'] / self.idf[class_label][word])
            self.tfidf[class_label] = sorted(self.tfidf[class_label].items(), key=operator.itemgetter(1), reverse=True)
            # warning: return a list of tuple instead of a dict

    def get_tfidf(self, limit=None):
        if len(self.tfidf) == 0:
            self.update_tfidf()
        if limit is not None:
            for class_label in self.tfidf.keys():
                self.tfidf[class_label] = self.tfidf[class_label][:limit]
        return self.tfidf

    def get_text_length_distribution(self):
        return self.textlength

    def get_word_count_num_distribution(self):
        return self.wordcount
