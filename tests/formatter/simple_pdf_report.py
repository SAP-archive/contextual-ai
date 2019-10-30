#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Sample Code to generate pdf report """

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append('../../')

from xai.data import DataUtil
from xai.data.constants import DATATYPE

from xai.model.interpreter import FeatureInterpreter
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
    report.detail.add_new_page()
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

    ### Load Data
    training_file_name = './sample_data/titanic.csv'
    data = pd.read_csv(training_file_name)
    ### Add dummy birthday to demonstrate datetime presentation
    bday = []
    for i in range(len(data)):
        year = np.random.randint(low=1960, high=1979)
        month = np.random.randint(low=1, high=12)
        day = np.random.randint(low=1, high=28)
        bday.append("%s" % (10000 * year + 100 * month + day))
    data['Birthday'] = bday

    label_column = 'Survived'

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Data Class (Label) Distribution')
    ### Add Label distribution
    label_distributions = DataUtil.get_label_distribution(data=data,
                                                          label=label_column)
    report.detail.add_data_set_distribution(label_distributions)

    ### Get data types
    feature, valid_feature_names, valid_feature_types, meta = \
        DataUtil.get_column_types(data=data, threshold=0.3, label=label_column)
    ### Get Data Stats
    stats = DataUtil.get_data_statistics(data=data,
                                         feature_names=valid_feature_names,
                                         feature_types=valid_feature_types,
                                         label=label_column)

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Data Field Attribute')
    ### Data Field Attribute
    report.detail.add_data_attributes(meta)

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Data Missing Value Check')
    ### Missing value count
    missing_count, total_count = \
        DataUtil.get_missing_value_count(data=data,
                                         feature_names=valid_feature_names,
                                         feature_types=valid_feature_types)
    report.detail.add_data_missing_value(missing_count=dict(missing_count),
                                         total_count=total_count)

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Data Field Distribution')
    ### Data Field Distribution Desc
    report.detail.add_paragraph(
        text='This section displays distribution for categorical fields, numerical fields and text fields.')

    ### Add Header Level 3
    report.detail.add_header_level_3(text='Categorical Field Distribution')
    ### Categorical field distribution
    for field_name in feature[DATATYPE.CATEGORY]:
        labelled_stats, all_stats = stats[field_name]
        report.detail.add_categorical_field_distribution(field_name=field_name,
                                                         field_distribution=labelled_stats)

    ### Add Header Level 3
    report.detail.add_header_level_3(text='Numerical Field Distribution')
    ### Numerical field distribution
    for field_name in feature[DATATYPE.NUMBER]:
        labelled_stats, all_stats = stats[field_name]
        report.detail.add_numeric_field_distribution(field_name=field_name,
                                                     field_distribution=labelled_stats)

    ### Add Header Level 3
    report.detail.add_header_level_3(text='Text Field Distribution')
    ### Text field distribution
    for field_name in feature[DATATYPE.FREETEXT]:
        labelled_stats, all_stats = stats[field_name]
        report.detail.add_text_field_distribution(field_name=field_name,
                                                  field_distribution=labelled_stats)

    ### Add Header Level 3
    report.detail.add_header_level_3(text='Datetime Field Distribution')
    ### Datetime field distribution
    for field_name in feature[DATATYPE.DATETIME]:
        labelled_stats, all_stats = stats[field_name]
        report.detail.add_datetime_field_distribution(field_name=field_name,
                                                      field_distribution=labelled_stats)


    ### Create Feature Analysis Section as new page
    report.detail.add_new_page()
    report.detail.add_section_title("Example for Feature Analysis ")
    ### Add Header Level 1
    report.detail.add_header_level_1(text='Feature Analysis')

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Feature Importance')
    ### Feature Importance
    path =  Path('./sample_data/model.pkl')
    model = pd.read_pickle(str(path))
    path = Path('./sample_data/train_data.csv')
    data = pd.read_csv(str(path))
    # -- csv including header --
    feature_names = data.columns

    fi = FeatureInterpreter(feature_names=feature_names)
    rank = fi.get_feature_importance_ranking(trained_model=model,
                                             train_x=data,
                                             method='default')
    report.detail.add_feature_importance(
        importance_ranking=rank, importance_threshold=0.005)

    ### Create Performance Analysis Section as new page
    report.detail.add_new_page()
    report.detail.add_section_title("Example for Performance Analysis ")
    report.detail.add_paragraph(text='this is dummy model, no trained with '
                                     'titanic dataset')
    ### Add Header Level 1
    report.detail.add_header_level_1(text='Performance Analysis')
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
    print("report generated : %s/simple-report.pdf" % dir_path)

if __name__ == "__main__":
    main()

