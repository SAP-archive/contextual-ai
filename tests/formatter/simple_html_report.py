#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Sample Code to generate html report """

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append('../../')

import dateutil
from statistics import median
from collections import Counter

from xai.data.constants import DATATYPE
from xai.data.explorer.data_analyzer_suite import DataAnalyzerSuite

from xai.data.explorer import CategoricalDataAnalyzer
from xai.data.validator import EnumValidator
from xai.model.interpreter.feature_interpreter import FeatureInterpreter
from xai.formatter import Report, HtmlWriter

################################################################################
### Sample Report
################################################################################


def main():
    ## Create Report
    report = Report(name='Sample Report')

    ### Create Cover Section
    report.overview.add_new_page()
    report.overview.add_section_title(text="Overview")
    report.overview.add_paragraph(text="This is summary Info")
    model_info = [('Model ID', '12345678'),
                  ('Model Version', 'v6'),
                  ('Scenario ID', '111222333444555'),
                  ('Notes', 'This model is created as a beta version.')
                  ]
    report.overview.add_model_info_summary(model_info=model_info)

    timing = [('Data Preprocessing', 1000),
              ('Feature Engineering', 10000),
              ('Training', 200200),
              ('Evaluation', 30303)]
    report.overview.add_training_timing(timing=timing)

    data_summary = [('training', 10000),
                    ('validation', 2000),
                    ('testing', 1000)]
    report.overview.add_data_set_summary(data_summary=data_summary)

    with open('./sample_data/evaluation_result_summary.json', 'r') as f:
        evaluation_result_data = json.load(f)
    print(evaluation_result_data)

    report.overview.add_evaluation_result_summary(
        evaluation_result=evaluation_result_data)

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
    report.detail.add_new_page()
    report.detail.add_section_title("Example for Data Analysis")
    ### Add Header Level 1
    report.detail.add_header_level_1(text='Data Analysis')

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Data Class Distribution')
    ### Add Label distribution
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
    ## TODO: where to park the code?
    # get the data type
    def get_column_types(data, threshold, label_column):

        def check_numercial(col_data):
            if col_data.dtypes == np.float64:
                return True
            else:
                return False

        def check_datetime(col_data):
            if col_data.dtypes == np.int64:
                return False

            def parse_date(date):
                try:
                    dt = dateutil.parser.parse(str(date))
                    return 0
                except ValueError:
                    return 1

            counter = Counter(col_data.tolist())
            if len(counter) >= threshold * len(col_data):
                invalid_count = 0
                for date in col_data.tolist():
                    invalid_count += parse_date(date)
                if invalid_count < threshold * len(col_data):
                    return True
                else:
                    return False
            else:
                return False

        def check_categorical(col_data):
            counter = Counter(col_data.tolist())
            if len(counter) < threshold * len(col_data):
                _median = median(counter.values())
                if _median == 1:
                    return False
                else:
                    return True
            else:
                return False

        def check_text(col_dat):
            def _get_token_number(x):
                return len(x.split(' '))

            if col_data.dtypes == object:
                if len(col_data.unique()) > len(col_data) * threshold:
                    if median(col_data.apply(_get_token_number)) > 3:
                        return True
                    else:
                        return False

        valid_feature_names = []
        valid_feature_types = []
        feature = {}
        feature['categorical'] = []
        feature['numerical'] = []
        feature['text'] = []
        feature['datetime'] = []
        meta = {}
        for column in data.columns:
            if column == label_column:
                meta[column] = {'type': 'label', 'used': True,
                                'structured': 'attribute'}
                continue
            col_data = data[column]

            if check_datetime(col_data):
                # datetime data
                feature['datetime'].append(column)
                valid_feature_names.append(column)
                valid_feature_types.append(DATATYPE.DATETIME)
                meta[column] = {'type': 'datetime', 'used': True,
                                'structured': 'attribute'}

            elif check_numercial(col_data):
                # numerical data
                feature['numerical'].append(column)
                valid_feature_names.append(column)
                valid_feature_types.append(DATATYPE.NUMBER)
                meta[column] = {'type': 'numerical', 'used': True,
                                'structured': 'attribute'}

            elif check_categorical(col_data):
                # categorical data
                feature['categorical'].append(column)
                valid_feature_names.append(column)
                valid_feature_types.append(DATATYPE.CATEGORY)
                meta[column] = {'type': 'categorical', 'used': True,
                                'structured': 'attribute'}

            elif check_text(col_data):
                # text data
                feature['text'].append(column)
                valid_feature_names.append(column)
                valid_feature_types.append(DATATYPE.FREETEXT)
                meta[column] = {'type': 'Text', 'used': True,
                                'structured': 'attribute'}

            else:
                print(
                    'Warning: the feature [%s] is suspected to be identifierable feature. \n[Examples]: %s\n' % (
                        column, col_data.tolist()[:5]))
                meta[column] = {'type': 'Key', 'used': True,
                                'structured': 'attribute'}

        return feature, valid_feature_names, valid_feature_types, meta

    feature, valid_feature_names, valid_feature_types, meta = get_column_types(
        data=data,
        threshold=0.3,
        label_column=label_column)

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
    def generate_missing_value_schema(valid_feature_names,
                                      valid_feature_types):
        missing_value_schema = dict()
        for name, column_type in zip(valid_feature_names, valid_feature_types):
            if column_type == 'categorical':
                missing_value_schema[name] = ['NAN']
            if column_type == 'numerical':
                missing_value_schema[name] = ['NaN']
        return missing_value_schema

    schema = generate_missing_value_schema(valid_feature_names,
                                           valid_feature_types)
    print(schema)
    json_line = json.loads(data.to_json(orient='records'))
    enum_validator = EnumValidator(schema=schema)
    enum_validator.validate_all(sample_list=json_line)
    stats = enum_validator.get_statistics()
    missing_count = dict(stats.column_stats)
    total_count = {feature_name: stats.total_count for feature_name in
                   schema.keys()}
    print('missing_count', missing_count)
    print('total_count', total_count)
    report.detail.add_data_missing_value(missing_count=dict(missing_count),
                                         total_count=total_count)

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Data Field Distribution')
    ### Data Field Distribution Desc
    report.detail.add_paragraph(
        text='This section displays distribution for categorical fields, numerical fields and text fields.')

    ## TODO: where to park the code?
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
    for field_name in feature['text']:
        labelled_stats, all_stats = stats[field_name]
        report.detail.add_text_field_distribution(field_name=field_name,
                                                  field_distribution=labelled_stats)

    ### Add Header Level 3
    report.detail.add_header_level_3(text='Datetime Field Distribution')
    ### Datetime field distribution
    for field_name in feature['datetime']:
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

    ### Create Training Analysis Section as new page
    report.detail.add_new_page()
    report.detail.add_section_title("Example for Training Analysis ")
    ### Add Header Level 1
    report.detail.add_header_level_1(text='Training Analysis')

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
    report.detail.add_header_level_2(text='Deep Learning Training')
    ### Learning Curve
    with open('./sample_data/learning_curve.json', 'r') as f:
        learning_curve = json.load(f)

    print('best_idx:', learning_curve['best_idx'])
    print('history [first 2 samples]:',
          {k: learning_curve['history'][k] for k in
           list(learning_curve['history'].keys())[:2]})
    print('benchmark_metric:', learning_curve['benchmark_metric'])
    print('benchmark_threshold:', learning_curve['benchmark_threshold'])
    print('training_params:', learning_curve['training_params'])

    report.detail.add_learning_curve(history=learning_curve['history'],
                                     best_idx=learning_curve['best_idx'],
                                     benchmark_metric=learning_curve[
                                          'benchmark_metric'],
                                     benchmark_threshold=learning_curve[
                                          'benchmark_threshold'],
                                     training_params=learning_curve[
                                          'training_params'])

    ### Create Data Evaluation Section
    report.detail.add_new_page()
    report.detail.add_section_title("Example for Data Evaluation")

    ### Add Header Level 1
    report.detail.add_header_level_1(
        text='Binary Classification Evaluation Analysis')
    ### Add Header Level 2
    report.detail.add_header_level_2(text='Overall Result')
    ### Numeric Metric
    with open('./sample_data/binary_evaluation_results.json', 'r') as f:
        eval_result = json.load(f)

    splits = eval_result.keys()
    numeric_metrics_list = []

    for split in splits:
        label_eval_result = eval_result[split]
        del (label_eval_result['vis_result'])
        numeric_metrics_list.append((split, label_eval_result))
    print(numeric_metrics_list)

    report.detail.add_binary_class_evaluation_metric_results(
        numeric_metrics_list,
        notes='The section shows general results like accuracy, precision, recall.')

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

    report.detail.add_confusion_matrix_results(
        confusion_matrix_tuple=confusion_matrix_list)

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Confidence Distribution')
    ### Confidence Distribution
    with open('./sample_data/binary_evaluation_results.json', 'r') as f:
        eval_result = json.load(f)

    splits = eval_result.keys()
    probability_plot_list = []

    for split in splits:
        vis_result = eval_result[split]['vis_result']
        probability_plot_list.append((split, vis_result))
        print('Split name:', split)
        for key, value in vis_result.items():
            print(' - %s:' % key, type(value), value[:3])

    report.detail.add_binary_class_confidence_distribution(
        probability_plot_list)

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Reliability Diagram')
    ### Reliability Diagram
    with open('./sample_data/binary_evaluation_results.json', 'r') as f:
        eval_result = json.load(f)

    splits = eval_result.keys()
    probability_plot_list = []

    for split in splits:
        label_eval_result = eval_result[split]['vis_result']
        probability_plot_list.append((split, vis_result))
        print('Split name:', split)
        for key, value in vis_result.items():
            print(' - %s:' % key, type(value), value[:3])

    report.detail.add_binary_class_reliability_diagram(probability_plot_list)

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
    report.detail.add_header_level_2(text='Overall Result')
    ### Numeric Metrics
    print(label_eval_result)

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Confusion Matrix')
    ### Confusion Matrix
    print(label_eval_result['CM'])

    report.detail.add_confusion_matrix_results(
        confusion_matrix_tuple=[('', label_eval_result['CM'])])

    ### Add Header Level 2
    report.detail.add_header_level_2(text='Confidence Distribution')
    ###  Probability Plot
    for class_name, class_value in vis_result.items():
        print('Class:', class_name)
        for key, value in class_value.items():
            print(' - %s:' % key, type(value), value[:4])

    report.detail.add_multi_class_confidence_distribution([('', vis_result)])

    ### Lastly generate report with the writer instance
    report.generate(writer=HtmlWriter(name='simple-html-report',
                                      path='./sample_output'))

    dir_path = os.getcwd()
    print("")
    print("report generated : %s/simple-report.html" % dir_path)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)
