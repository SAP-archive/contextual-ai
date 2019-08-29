from xai.data_explorer.abstract_labelled_analyzer import AbstractLabelledDataAnalyzer
from xai.data_explorer.config import DICT_DATATYPE_TO_ANALYZER
from xai.data_explorer.data_exceptions import AttributeNotFound, InconsistentIteratorSize, AnalyzerDataTypeNotSupported


class DataAnalyzerSuite:
    """
    a data analyzer suite allows users to add many data analyzer and analyze sample in
    """

    def __init__(self):
        self.analyzers = dict()

    def add_analyzer(self, attribute_name: str or int, analyzer: AbstractLabelledDataAnalyzer):
        self.analyzer_list[attribute_name] = analyzer

    def add_analyzer_by_data_type(self, attribute_name: str or int, data_type: str):
        if data_type not in DICT_DATATYPE_TO_ANALYZER.keys():
            raise AnalyzerDataTypeNotSupported(data_type)
        self.analyzer_list[attribute_name] = DICT_DATATYPE_TO_ANALYZER[data_type]

    def feed(self, sample, label):
        for attribute_name, analyzer in self.analyzers.items():
            if attribute_name not in sample:
                raise AttributeNotFound(attribute_name, sample)
            analyzer.feed(value=sample[attribute_name], label=label)

    def feed_all(self, samples, labels):
        if len(samples) != len(labels):
            raise InconsistentIteratorSize(len(samples), len(labels))

        sample_label = zip(samples, labels)
        for sample, label in sample_label:
            for attribute_name, analyzer in self.analyzers.items():
                if attribute_name not in sample:
                    raise AttributeNotFound(attribute_name, sample)
                analyzer.feed(value=sample[attribute_name], label=label)

    def get_statistics(self):
        for analyzer in self.analyzer_list:
            meta = analyzer.summarize_info()
            for key, value in meta.items():
                if key in self.metadata:
                    self.metadata[key].update(value)
                else:
                    self.metadata[key] = value
        return self.metadata
