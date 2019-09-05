from typing import Optional, Dict, Iterator

from xai.data.config import DICT_DATATYPE_TO_ANALYZER, DICT_ANALYZER_TO_DATATYPE
from xai.data.constants import STATSKEY
from xai.data.exceptions import AttributeNotFound, InconsistentIteratorSize, AnalyzerDataTypeNotSupported
from xai.data.explorer.labelled_analyzer import LabelledDataAnalyzer


class DataAnalyzerSuite:
    """
    a data analyzer suite allows users to add multiple data analyzers and analyze specified according to data type
    """

    def __init__(self):
        self.analyzers = dict()

    def add_analyzer(self, attribute_name: str or int, analyzer_cls):
        """
        add data analyzer by initializing the analyzer object
        Args:
            attribute_name: name to identify a column/attribute in sample
            analyzer_cls: analyzer implements AbstractLabelledDataAnalyzer
        """
        self.analyzers[attribute_name] = LabelledDataAnalyzer(data_analyzer_cls=analyzer_cls)

    def add_analyzer_by_data_type(self, attribute_name: str or int, data_type: str):
        """
        add data analyzer by data type
        Args:
            attribute_name: name to identify a column/attribute in sample
            data_type: pre-defined data type, see `xai.data.constants.DATATYPE`
        """
        if data_type not in DICT_DATATYPE_TO_ANALYZER.keys():
            raise AnalyzerDataTypeNotSupported(data_type)
        self.analyzers[attribute_name] = DICT_DATATYPE_TO_ANALYZER[data_type]

    def feed(self, sample: Dict, label: Optional = None):
        """
        feed one sample into the analyzer suite to aggregate stats according to data type attribute
        Args:
            sample: json object
            label: class label associated to the sample, default is None when no label provided
        """
        for attribute_name, analyzer in self.analyzers.items():
            if attribute_name not in sample:
                raise AttributeNotFound(attribute_name, sample)
            analyzer.feed(value=sample[attribute_name], label=label)

    def feed_all(self, samples: Iterator[Dict], labels: Optional[Iterator] = None):
        """
        feed a series of samples into the analyzer suite to aggregate stats according to data type attribute
        Args:
            samples: a sequence of json objects
            labels: class labels associated to the samples, default is None when no label provided

        """
        if labels is None:
            labels = [None] * len(samples)

        if len(samples) != len(labels):
            raise InconsistentIteratorSize(len(samples), len(labels))

        sample_label = zip(samples, labels)
        for sample, label in sample_label:
            for attribute_name, analyzer in self.analyzers.items():
                if attribute_name not in sample:
                    raise AttributeNotFound(attribute_name, sample)
                analyzer.feed(value=sample[attribute_name], label=label)

    def get_statistics(self) -> Dict[str, Dict]:
        """
        get overall stats for the entire data analyzer suite.
        Returns:
            a dictionary maps attribute name to stats json object representation.
        """
        overall_stats = []
        for attribute_name, analyzer in self.analyzers.items():
            attribute_stats = dict()
            attribute_stats[STATSKEY.DATA_COLUMN_NAME] = attribute_name
            attribute_stats[STATSKEY.DATA_TYPE] = DICT_ANALYZER_TO_DATATYPE[type(analyzer)]
            attribute_stats.update(analyzer.get_statistics().to_json)
            overall_stats.append(attribute_stats)
        return overall_stats
