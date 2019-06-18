from plugin.xai.data_explorer.abstract_analyzer import AbstractAnalyzer


class DataAnalyzerSuite:
    def __init__(self):
        self.analyzer_list = []
        self.metadata = {}
    def add_analyzer(self, analyzer: AbstractAnalyzer):
        self.analyzer_list.append(analyzer)

    def analyze_sample(self, sample, class_value):
        for analyzer in self.analyzer_list:
            analyzer.analyze_sample(sample, class_value)

    def aggregate(self):
        for analyzer in self.analyzer_list:
            analyzer.aggregate()

    def get_overall_metadata(self):
        for analyzer in self.analyzer_list:
            meta = analyzer.summarize_info()
            for key, value in meta.items():
                if key in self.metadata:
                    self.metadata[key].update(value)
                else:
                    self.metadata[key] = value
        return self.metadata
