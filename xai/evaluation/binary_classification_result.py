from xai.evaluation.basic_result import ClassificationResult
from xai.evaluation.confusion_matrix import ConfusionMatrix
from xai.util import get_table_layout
from xai import constants


class BinaryClassificationResult(ClassificationResult):
    def __init__(self, ):
        super(BinaryClassificationResult, self).__init__()

    def load_results_from_meta(self, metadata: dict):
        for split, evaluation_result in metadata.items():
            for metric, value in evaluation_result.items():
                if type(value) != dict:
                    self.update_result(split, metric, 1, value)
                if metric == constants.TRAIN_TEST_CM:
                    self.confusion_matrices[split] = ConfusionMatrix(label=['0', '1'], confusion_matrix=value)

    def convert_metrics_to_table(self):
        table_header = ['Metric']
        table_header.extend([split.capitalize() for split in self.split_set])
        table_content = []
        for metric in self.metric_set:
            row = [metric.capitalize()]
            row.extend(["{:.4f}".format(self.resultdict[split][metric][1]) for split in self.split_set if
                        (type(self.resultdict[split][metric][1]) == float or self.resultdict[split][metric] == 'nan')])
            if len(row) == len(table_header):
                table_content.append(row)
        layout = get_table_layout(table_header)
        output_tables = [('Overall Result', table_header, table_content, layout)]
        return output_tables

    def get_confusion_matrices(self):
        return self.confusion_matrices
