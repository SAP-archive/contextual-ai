from xai.evaluation.basic_result import ClassificationResult
from xai.evaluation.confusion_matrix import ConfusionMatrix
from xai.util import get_table_layout
from xai import constants


class BinaryClassificationResult(ClassificationResult):
    def __init__(self):
        super(BinaryClassificationResult, self).__init__()

    def load_results_from_meta(self, evaluation_result: dict):
        for metric, value in evaluation_result.items():
            if metric == constants.TRAIN_TEST_CM:
                self.confusion_matrices = ConfusionMatrix(label=['0', '1'], confusion_matrix=value)
            else:
                self.update_result(metric, 1, value)

    def convert_metrics_to_table(self):
        table_header = ['Metric', 'Value']
        table_content = []
        for metric in self.metric_set:
            table_content.append([metric.capitalize(), "%.4f"%self.resultdict[metric][1]])
        layout = get_table_layout(table_header)
        output_tables = ('Overall Result', table_header, table_content, layout)
        return output_tables

    def get_confusion_matrices(self):
        return self.confusion_matrices
