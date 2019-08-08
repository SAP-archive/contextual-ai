from xai.evaluation.basic_result import ClassificationResult
from xai.evaluation.confusion_matrix import ConfusionMatrix
from xai.util import get_table_layout
from xai import constants
from collections import defaultdict


class MultiClassificationResult(ClassificationResult):
    def __init__(self):
        super(MultiClassificationResult, self).__init__()
        self.average_result_dict = defaultdict(lambda: defaultdict(int))

    def load_results_from_meta(self, evaluation_result: dict):
        for metric, values in evaluation_result.items():
            if metric == constants.TRAIN_TEST_CM:
                self.confusion_matrices = ConfusionMatrix(label=values['labels'],
                                                          confusion_matrix=values['values'])
            else:
                if 'class' in values:
                    class_values = values['class']
                    for class_label, class_value in class_values.items():
                        self.update_result(metric, class_label, class_value)
                if 'average' in values:
                    self.average_result_dict[metric] = values['average']

    def convert_metrics_to_table(self, label_as_row=True):
        output_tables = []
        if label_as_row:
            # set metric as columns, label as rows
            table_header = ['Label']
            table_header.extend([metric for metric in self.metric_set])

            table_content = []
            for label in self.label_set:
                row = [label]
                row.extend(
                    ["{:.4f}".format(self.resultdict[metric][label]) if type(
                        self.resultdict[metric][label]) == float else 'nan' for metric in self.metric_set])
                table_content.append(row)
        else:
            # set label as columns, metric as rows
            table_header = ['Metric']
            table_header.extend([label for label in self.label_set])

            table_content = []
            for metric in self.metric_set:
                row = [metric]
                row.extend(["{:.4f}".format(self.resultdict[metric][label]) for label in self.label_set])
                table_content.append(row)

        # add in average result if any[
        if table_header[0] == 'Label':
            row = ['Average']
            row.extend(
                ["{:.4f}".format(self.average_result_dict[metric]) for metric in self.metric_set])
            table_content.append(row)
        elif table_header[0] == 'Metric':
            table_header.append('Average')
            for row in table_content:
                metric = row[0]
                row.append("{:.4f}".format(self.average_result_dict[metric]))
        layout = get_table_layout(table_header)
        table = ("Metric Result", table_header, table_content, layout)

        return table

    def get_confusion_matrices(self):
        return self.confusion_matrices
