#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Sample Code to generate report """

import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.append('../../')

from xai.data.constants import DATATYPE
from xai.data.explorer.data_analyzer_suite import DataAnalyzerSuite

from xai.data.explorer import CategoricalDataAnalyzer
from xai.formatter import Report, PdfWriter


################################################################################
### Sample Report
################################################################################


def main():
    ## Create Report
    report = Report(name='Sample Report')

    ### Create Cover Section
    report.overview.add_section_title(text="Summary")
    report.overview.add_paragraph(text="This is summary Info")

    ### Create Contents Section - Header
    report.detail.add_section_title(text="Example for Header")
    #### Header Level 1 and it paragraph
    report.detail.add_header_level_1(text='Section Header 1')
    report.detail.add_paragraph(text="This is content Info of header 1")
    #### Header Level 2 and it paragraph
    report.detail.add_header_level_2(text='Section Header 2')
    report.detail.add_paragraph(text="This is content Info of header 2")
    #### Header Level 3 and it paragraph
    report.detail.add_header_level_3(text='Section Header 3')
    report.detail.add_paragraph(text="This is content Info of header 3")

    ### Create Data Analysis Section
    report.detail.add_section_title("Example for Data Analysis ")
    ### Add Header Level 1
    report.detail.add_header_level_1(text='Data Analysis')

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Data Class (Label) Distribution')
    ### Add Label distribution
    training_file_name = './sample_data/titanic.csv'
    data = pd.read_csv(training_file_name)

    label_analyzer = CategoricalDataAnalyzer()
    label_column = 'Survived'

    label_analyzer.feed_all(data[label_column].tolist())
    label_stats = label_analyzer.get_statistics()

    data_distributions = list()
    data_distributions.append((label_column, label_stats.frequency_count))
    print(data_distributions)
    report.detail.add_data_set_distribution(data_distributions)

    ## TODO: where to park the code?
    # get the data type
    def get_column_types(data, threshold, label_column):
        valid_feature_names = []
        valid_feature_types = []
        feature = {}
        feature['categorical'] = []
        feature['numerical'] = []
        meta = {}
        for column in data.columns:
            if column == label_column:
                meta[column] = {'type': 'label', 'used': True,
                                'structured': 'attribute'}
                continue
            col_data = data[column]
            unique_values = col_data.unique()

            if col_data.dtypes == np.float64:
                feature['numerical'].append(column)
                valid_feature_names.append(column)
                valid_feature_types.append(DATATYPE.NUMBER)
                meta[column] = {'type': 'numerical', 'used': True,
                                'structured': 'attribute'}
            elif col_data.dtypes == np.int64:
                if len(unique_values) < threshold * len(col_data):
                    feature['categorical'].append(column)
                    valid_feature_names.append(column)
                    valid_feature_types.append(DATATYPE.CATEGORY)
                    meta[column] = {'type': 'categorical', 'used': True,
                                    'structured': 'attribute'}

                else:
                    print(
                        'Error: %s is suspected to be identifierable features. %s distinct values given %s rows. Will be ignored in data report.' %
                        (column, len(unique_values), len(col_data)))
                    if len(unique_values) == len(col_data):
                        meta[column] = {'type': 'KEY', 'used': False,
                                        'structured': 'attribute'}
            else:
                if len(unique_values) < threshold * len(col_data):
                    feature['categorical'].append(column)
                    valid_feature_names.append(column)
                    valid_feature_types.append(DATATYPE.CATEGORY)
                    meta[column] = {'type': 'categorical', 'used': True,
                                    'structured': 'attribute'}

                else:
                    print(
                        'Warning: %s is suspected to be identifierable features. %s distinct values given %s rows. Set it to text feature.' %
                        (column, len(unique_values), len(col_data)))
                    valid_feature_names.append(column)
                    valid_feature_types.append(DATATYPE.FREETEXT)
                    meta[column] = {'type': 'Text', 'used': False,
                                    'structured': 'attribute'}

        return feature, valid_feature_names, valid_feature_types, meta

    feature, valid_feature_names, valid_feature_types, meta = get_column_types(
        data=data, threshold=0.6, label_column=label_column)

    # pprint(feature)
    print(valid_feature_names)
    print(valid_feature_types)
    print(meta)

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Data Field Attribute')
    ### Data Field Attribute
    report.detail.add_data_attributes(meta)

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Data Missing Value Check')
    ### Missing value
    with open('./sample_data/missing_value.json', 'r') as f:
        missing_value = json.load(f)

    missing_count = missing_value["missing_count"]
    total_count = missing_value["total_count"]
    print('missing_count', missing_count)
    print('total_count', total_count)
    report.detail.add_data_missing_value(missing_count=missing_count,
                                         total_count=total_count)

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Data Field Distribution')
    ### Data Field Distribution Desc
    report.detail.add_paragraph(
        text='This section displays distribution for categorical fields, numerical fields and text fields.')

    ## TODO:
    data_analyzer_suite = DataAnalyzerSuite(data_type_list=valid_feature_types,
                                            column_names=valid_feature_names)
    print(data_analyzer_suite.schema)

    for column, column_type in zip(valid_feature_names, valid_feature_types):
        if column_type == 'categorical':
            data[column][data[column].isnull()] = 'NAN'
        data_analyzer_suite.feed_column(column_name=column,
                                        column_data=data[column].tolist(),
                                        labels=data[label_column])
    stats = data_analyzer_suite.get_statistics()

    ### Add Header Level 3
    report.detail.add_header_level_3(text='Categorical Field Distribution')
    ### Categorical field distribution
    for field_name in feature['categorical']:
        labelled_stats, all_stats = stats[field_name]
        report.detail.add_categorical_field_distribution(field_name=field_name,
                                                         field_distribution=labelled_stats)

    ### Add Header Level 3
    report.detail.add_header_level_3(text='Numerical Field Distribution')
    ### Numerical field distribution
    for field_name in feature['numerical']:
        labelled_stats, all_stats = stats[field_name]
        report.detail.add_numeric_field_distribution(field_name=field_name,
                                                     field_distribution=labelled_stats)

    ### Add Header Level 3
    report.detail.add_header_level_3(text='Text Field Distribution')
    ### Text field distribution
    # with open('./sample_data/text_data.json', 'r') as f:
    #     text_data = json.load(f)
    #
    # print('SAMPLE DATA FORMAT')
    # print('==================')
    # for key, value in text_data.items():
    #     print('Field name:', key)
    #     for class_key, class_stats in value.items():
    #         print(' - Class name:', class_key)
    #         for stats_key, stats_value in class_stats.items():
    #             print('   * %s:' % stats_key, type(stats_value),
    #                   stats_value[:min(3, len(stats_value))] if type(
    #                       stats_value) == list else stats_value)
    #         break
    #
    for field_name, field_distribution in text_data.items():
        report.detail.add_text_field_distribution(field_name=field_name,
                                                  field_distribution=field_distribution)

    ### Add Header Level 3
    # report.detail.add_header_level_3(text='Datetime Field Distribution')
    # ### Datetime field distribution
    # with open('./sample_data/datetime_data.json', 'r') as f:
    #     datetime_data = json.load(f)
    # print(datetime_data)
    #
    # for field_name, field_distribution in datetime_data.items():
    #     report.detail.add_datetime_field_distribution(field_name=field_name,
    #                                                   field_distribution=field_distribution)

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Hyperparameter Tuning')
    ### Hyperparameter Tuning
    with open('./sample_data/hyperparameter_tuning.json', 'r') as f:
        hyperparameter_tuning = json.load(f)

    print('search_space:', hyperparameter_tuning['search_space'])
    print('best_idx:', hyperparameter_tuning['best_idx'])
    print('history [first 2 samples]:',
          {k: hyperparameter_tuning['history'][k] for k in
           list(hyperparameter_tuning['history'].keys())[:2]})
    print('benchmark_metric:', hyperparameter_tuning['benchmark_metric'])
    print('benchmark_threshold:', hyperparameter_tuning['benchmark_threshold'])
    print('non_hyperopt_score:', hyperparameter_tuning['non_hyperopt_score'])

    report.detail.add_hyperparameter_tuning(
        history=hyperparameter_tuning['history'],
        best_idx=hyperparameter_tuning['best_idx'],
        search_space=hyperparameter_tuning['search_space'],
        benchmark_metric=hyperparameter_tuning['benchmark_metric'],
        benchmark_threshold=hyperparameter_tuning['benchmark_threshold'],
        non_hyperopt_score=hyperparameter_tuning['non_hyperopt_score'])

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Confusion Matrix')
    ### Confusion Matrix
    with open('./sample_data/binary_evaluation_results.json', 'r') as f:
        eval_result = json.load(f)
    splits = eval_result.keys()
    confusion_matrix_list = []

    for split in splits:
        label_eval_result = eval_result[split]
        confusion_matrix_list.append((split,
                                      {"labels": ["Negative", "Positive"],
                                       "values": label_eval_result["CM"]}))
    print(confusion_matrix_list)

    report.detail.add_confusion_matrix_results(confusion_matrix_list)

    ### Create Data Evaluation Section
    report.detail.add_new_page()
    report.detail.add_section_title("Example for Data Evaluation ")
    ### Add Header Level 1
    report.detail.add_header_level_1(
        text='Multi-class Classification Evaluation Analysis')

    with open('./sample_data/multi_evaluation_results.json', 'r') as f:
        eval_result = json.load(f)

    label_key = 'label_1'
    label_eval_result = eval_result[label_key]
    vis_result = label_eval_result['vis_result']
    del (label_eval_result['vis_result'])

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Confidence Distribution')
    ###  Probability Plot
    for class_name, class_value in vis_result.items():
        print('Class:', class_name)
        for key, value in class_value.items():
            print(' - %s:' % key, type(value), value[:4])

    report.detail.add_multi_class_confidence_distribution([('', vis_result)])

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Confusion Matrix')
    ### Confusion Matrix
    print(label_eval_result['CM'])

    report.detail.add_confusion_matrix_results(
        confusion_matrix_tuple=[('', label_eval_result['CM'])])

    with open('./sample_data/evaluation_result_summary.json', 'r') as f:
        evaluation_result_data = json.load(f)
    print(evaluation_result_data)

    report.overview.add_evaluation_result_summary(
        evaluation_result=evaluation_result_data)

    ### Lastly generate report with the writer instance
    report.generate(writer=PdfWriter(name='simple-pdf-report',
                                     path='./sample_output'))
    dir_path = os.getcwd()
    print("")
    print("report generated : %s/simple-pdf-report.pdf" % dir_path)

if __name__ == "__main__":
    main()

