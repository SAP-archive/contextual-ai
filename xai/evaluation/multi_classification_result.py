from xai.evaluation.basic_result import ClassificationResult
from xai.evaluation.confusion_matrix import ConfusionMatrix
from xai.util import get_table_layout
from xai import constants
from collections import defaultdict


class MultiClassificationResult(ClassificationResult):
    def __init__(self):
        super(MultiClassificationResult, self).__init__()
        self.average_result_dict = defaultdict(lambda: defaultdict(int))

    def load_results_from_meta(self, metadata: dict):
        for split, evaluation_result in metadata.items():
            for metric, values in evaluation_result.items():
                if metric == constants.TRAIN_TEST_CM:
                    self.confusion_matrices[split] = ConfusionMatrix(label=values['labels'],
                                                                     confusion_matrix=values['values'])
                    continue
                if 'class' in values:
                    class_values = values['class']
                    for class_label, class_value in class_values.items():
                        self.update_result(split, metric, class_label, class_value)
                if 'average' in values:
                    self.average_result_dict[split][metric] = values['average']

    def convert_metrics_to_table(self):
        output_tables = []
        for split in self.split_set:
            if len(self.metric_set) > len(self.label_set):
                # set label as columns, metric as rows
                table_header = ['Metric']
                table_header.extend([label for label in self.label_set])

                table_content = []
                for metric in self.metric_set:
                    row = [metric.capitalize()]
                    row.extend(["{:.4f}".format(self.resultdict[split][metric][label]) for label in self.label_set])
                    table_content.append(row)
            else:
                # set metric as columns, label as rows

                table_header = ['Label']
                table_header.extend([metric.capitalize() for metric in self.metric_set])

                table_content = []
                for label in self.label_set:
                    row = [label]
                    row.extend(
                        ["{:.4f}".format(self.resultdict[split][metric][label]) if type(
                            self.resultdict[split][metric][label]) == float else 'nan' for metric in self.metric_set])
                    table_content.append(row)

            # add in average result if any[
            if split in self.average_result_dict.keys():
                if table_header[0] == 'Label':
                    row = ['Average']
                    row.extend(
                        ["{:.4f}".format(self.average_result_dict[split][metric]) for metric in self.metric_set])
                    table_content.append(row)
                elif table_header[0] == 'Metric':
                    table_header.append('Average')
                    for row in table_content:
                        metric = row[0]
                        row.append(self.average_result_dict[split][metric])
            layout = get_table_layout(table_header)
            table = ("%s Result" % (split.capitalize()), table_header, table_content, layout)

            output_tables.append(table)

        return output_tables

    def get_confusion_matrices(self):
        return self.confusion_matrices
