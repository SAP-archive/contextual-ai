#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Sample Code to generate report """

import sys
sys.path.append('../../../')
print(sys.path)
import json

from xai.formatter import Report, HtmlWriter

################################################################################
### Sample Report
################################################################################


def main():
    ## Create Report
    report = Report(name='Sample Report')

    ### Create Cover Section
    report.cover.add_section_title(text="Overview")
    report.cover.add_paragraph(text="This is summary Info")
    model_info = [('Model ID', '12345678'),
                  ('Model Version', 'v6'),
                  ('Scenario ID', '111222333444555'),
                  ('Notes', 'This model is created as a beta version.')
                  ]
    report.cover.add_model_info_summary(model_info=model_info)

    timing = [('Data Preprocessing', 1000),
              ('Feature Engineering', 10000),
              ('Training', 200200),
              ('Evaluation', 30303)]
    report.cover.add_training_timing(timing=timing)

    data_summary = [('training', 10000),
                    ('validation', 2000),
                    ('testing', 1000)]
    report.cover.add_data_set_summary(data_summary=data_summary)

    with open('./../sample_data/evaluation_result_summary.json', 'r') as f:
        evaluation_result_data = json.load(f)
    print(evaluation_result_data)

    report.cover.add_evaluation_result_summary(
        evaluation_result=evaluation_result_data)

    ### Create Contents Section - Header
    report.content.add_section_title(text="Example for Header")
    #### Header Level 1 and it paragraph
    report.content.add_header_level_1(text='Section Header 1')
    report.content.add_paragraph(text="This is content Info of header 1")
    #### Header Level 2 and it paragraph
    report.content.add_header_level_2(text='Section Header 2')
    report.content.add_paragraph(text="This is content Info of header 2")
    #### Header Level 3 and it paragraph
    report.content.add_header_level_3(text='Section Header 3')
    report.content.add_paragraph(text="This is content Info of header 3")

    ### Create Data Analysis Section
    report.content.add_section_title("Example for Data Analysis")
    ### Add Header Level 1
    report.content.add_header_level_1(text='Data Analysis')

    ### Add Header Level 2
    report.content.add_header_level_2(text='Data Class Distribution')
    ### Add Dataset distribution
    with open('./../sample_data/data_distribution.json', 'r') as f:
        data_dist = json.load(f)
    data_distributions = []
    for k, v in data_dist.items():
        data_distributions.append((k, v))
    print(data_distributions)
    report.content.add_data_set_distribution(data_distributions)

    ### Add Header Level 2
    report.content.add_header_level_2(text='Data Field Attribute')
    ### Data Field Attribute
    with open('./../sample_data/data_attribute.json', 'r') as f:
        data_attribute = json.load(f)
    print(data_attribute)
    report.content.add_data_attributes(data_attribute)

    ### Add Header Level 2
    report.content.add_header_level_2(text='Data Missing Value Check')
    ### Missing value
    with open('./../sample_data/missing_value.json', 'r') as f:
        missing_value = json.load(f)

    missing_count = missing_value["missing_count"]
    total_count = missing_value["total_count"]
    print('missing_count', missing_count)
    print('total_count', total_count)
    report.content.add_data_missing_value(missing_count=missing_count,
                                          total_count=total_count)

    ### Add Header Level 2
    report.content.add_header_level_2(text='Data Field Distribution')
    ### Data Field Distribution Desc
    report.content.add_paragraph(
        text='This section displays distribution for categorical fields, numerical fields and text fields.')

    ### Add Header Level 3
    report.content.add_header_level_3(text='Categorical Field Distribution')
    ### Categorical field distribution
    with open('./../sample_data/categorical_data.json', 'r') as f:
        categorical_data = json.load(f)
    print(categorical_data)

    for field_name, field_distribution in categorical_data.items():
        report.content.add_categorical_field_distribution(
            field_name=field_name, field_distribution=field_distribution)

    ### Add Header Level 3
    report.content.add_header_level_3(text='Numerical Field Distribution')
    ### Numerical field distribution
    with open('./../sample_data/numerical_data.json', 'r') as f:
        numerical_data = json.load(f)

    print('SAMPLE DATA FORMAT')
    print('==================')
    for key, value in numerical_data.items():
        print('Field name:', key)
        for class_key, class_stats in value.items():
            print(' - Class name:', class_key)
            for stats_key, stats_value in class_stats.items():
                print('   * %s:' % stats_key, type(stats_value),
                      stats_value[:min(3, len(stats_value))] if type(
                          stats_value) == list else stats_value)
            break

    for field_name, field_distribution in numerical_data.items():
        report.content.add_numeric_field_distribution(field_name=field_name,
                                                      field_distribution=field_distribution)

    ### Add Header Level 3
    report.content.add_header_level_3(text='Text Field Distribution')
    ### Text field distribution
    with open('./../sample_data/text_data.json', 'r') as f:
        text_data = json.load(f)

    print('SAMPLE DATA FORMAT')
    print('==================')
    for key, value in text_data.items():
        print('Field name:', key)
        for class_key, class_stats in value.items():
            print(' - Class name:', class_key)
            for stats_key, stats_value in class_stats.items():
                print('   * %s:' % stats_key, type(stats_value),
                      stats_value[:min(3, len(stats_value))] if type(
                          stats_value) == list else stats_value)
            break

    for field_name, field_distribution in text_data.items():
        report.content.add_text_field_distribution(field_name=field_name,
                                                   field_distribution=field_distribution)

    ### Add Header Level 3
    report.content.add_header_level_3(text='Datetime Field Distribution')
    ### Datetime field distribution
    with open('./../sample_data/datetime_data.json', 'r') as f:
        datetime_data = json.load(f)
    print(datetime_data)

    for field_name, field_distribution in datetime_data.items():
        report.content.add_datetime_field_distribution(field_name=field_name,
                                                       field_distribution=field_distribution)

    ### Create Feature Analysis Section as new page
    report.content.add_section_title("Example for Feature Analysis ")
    ### Add Header Level 1
    report.content.add_header_level_1(text='Feature Analysis')

    ### Add Header Level 2
    report.content.add_header_level_2(text='Feature Importance')
    ### Feature Importance
    with open('./../sample_data/feature_importance.json', 'r') as f:
        feature_importance = json.load(f)

    print('SAMPLE DATA FOR FEATURE IMPORTANCE')
    print('==================================')
    print(type(feature_importance), feature_importance[:10])

    report.content.add_feature_importance(
        importance_ranking=feature_importance, importance_threshold=0.005)

    ### Create Training Analysis Section as new page
    report.content.add_section_title("Example for Training Analysis ")
    ### Add Header Level 1
    report.content.add_header_level_1(text='Training Analysis')

    ### Add Header Level 2
    report.content.add_header_level_2(text='Hyperparameter Tuning')
    ### Hyperparameter Tuning
    with open('./../sample_data/hyperparameter_tuning.json', 'r') as f:
        hyperparameter_tuning = json.load(f)

    print('search_space:', hyperparameter_tuning['search_space'])
    print('best_idx:', hyperparameter_tuning['best_idx'])
    print('history [first 2 samples]:',
          {k: hyperparameter_tuning['history'][k] for k in
           list(hyperparameter_tuning['history'].keys())[:2]})
    print('benchmark_metric:', hyperparameter_tuning['benchmark_metric'])
    print('benchmark_threshold:', hyperparameter_tuning['benchmark_threshold'])
    print('non_hyperopt_score:', hyperparameter_tuning['non_hyperopt_score'])

    report.content.add_hyperparameter_tuning(
        history=hyperparameter_tuning['history'],
        best_idx=hyperparameter_tuning['best_idx'],
        search_space=hyperparameter_tuning['search_space'],
        benchmark_metric=hyperparameter_tuning['benchmark_metric'],
        benchmark_threshold=hyperparameter_tuning['benchmark_threshold'],
        non_hyperopt_score=hyperparameter_tuning['non_hyperopt_score'])

    ### Add Header Level 2
    report.content.add_header_level_2(text='Deep Learning Training')
    ### Learning Curve
    with open('./../sample_data/learning_curve.json', 'r') as f:
        learning_curve = json.load(f)

    print('best_idx:', learning_curve['best_idx'])
    print('history [first 2 samples]:',
          {k: learning_curve['history'][k] for k in
           list(learning_curve['history'].keys())[:2]})
    print('benchmark_metric:', learning_curve['benchmark_metric'])
    print('benchmark_threshold:', learning_curve['benchmark_threshold'])
    print('training_params:', learning_curve['training_params'])

    report.content.add_learning_curve(history=learning_curve['history'],
                                      best_idx=learning_curve['best_idx'],
                                      benchmark_metric=learning_curve[
                                          'benchmark_metric'],
                                      benchmark_threshold=learning_curve[
                                          'benchmark_threshold'],
                                      training_params=learning_curve[
                                          'training_params'])

    ### Create Data Evaluation Section
    report.content.add_new_page()
    report.content.add_section_title("Example for Data Evaluation")

    ### Add Header Level 1
    report.content.add_header_level_1(
        text='Binary Classification Evaluation Analysis')
    ### Add Header Level 2
    report.content.add_header_level_2(text='Overall Result')
    ### Numeric Metric
    with open('./../sample_data/binary_evaluation_results.json', 'r') as f:
        eval_result = json.load(f)

    splits = eval_result.keys()
    numeric_metrics_list = []

    for split in splits:
        label_eval_result = eval_result[split]
        del (label_eval_result['vis_result'])
        numeric_metrics_list.append((split, label_eval_result))
    print(numeric_metrics_list)

    report.content.add_binary_class_evaluation_metric_results(
        numeric_metrics_list,
        notes='The section shows general results like accuracy, precision, recall.')

    ### Add Header Level 2
    report.content.add_header_level_2(text='Confusion Matrix')
    ### Confusion Matrix
    with open('./../sample_data/binary_evaluation_results.json', 'r') as f:
        eval_result = json.load(f)
    splits = eval_result.keys()
    confusion_matrix_list = []

    for split in splits:
        label_eval_result = eval_result[split]
        confusion_matrix_list.append((split,
                                      {"labels": ["Negative", "Positive"],
                                       "values": label_eval_result["CM"]}))
    print(confusion_matrix_list)

    report.content.add_confusion_matrix_results(
        confusion_matrix_tuple=confusion_matrix_list)

    ### Add Header Level 2
    report.content.add_header_level_2(text='Confidence Distribution')
    ### Confidence Distribution
    with open('./../sample_data/binary_evaluation_results.json', 'r') as f:
        eval_result = json.load(f)

    splits = eval_result.keys()
    probability_plot_list = []

    for split in splits:
        vis_result = eval_result[split]['vis_result']
        probability_plot_list.append((split, vis_result))
        print('Split name:', split)
        for key, value in vis_result.items():
            print(' - %s:' % key, type(value), value[:3])

    report.content.add_binary_class_confidence_distribution(
        probability_plot_list)

    ### Add Header Level 2
    report.content.add_header_level_2(text='Reliability Diagram')
    ### Reliability Diagram
    with open('./../sample_data/binary_evaluation_results.json', 'r') as f:
        eval_result = json.load(f)

    splits = eval_result.keys()
    probability_plot_list = []

    for split in splits:
        label_eval_result = eval_result[split]['vis_result']
        probability_plot_list.append((split, vis_result))
        print('Split name:', split)
        for key, value in vis_result.items():
            print(' - %s:' % key, type(value), value[:3])

    report.content.add_binary_class_reliability_diagram(probability_plot_list)

    ### Add Header Level 1
    report.content.add_header_level_1(
        text='Multi-class Classification Evaluation Analysis')

    with open('./../sample_data/multi_evaluation_results.json', 'r') as f:
        eval_result = json.load(f)

    label_key = 'label_1'
    label_eval_result = eval_result[label_key]
    vis_result = label_eval_result['vis_result']
    del (label_eval_result['vis_result'])

    ### Add Header Level 2
    report.content.add_header_level_2(text='Overall Result')
    ### Numeric Metrics
    print(label_eval_result)

    ### Add Header Level 2
    report.content.add_header_level_2(text='Confusion Matrix')
    ### Confusion Matrix
    print(label_eval_result['CM'])

    report.content.add_confusion_matrix_results(
        confusion_matrix_tuple=[('', label_eval_result['CM'])])

    ### Add Header Level 2
    report.content.add_header_level_2(text='Confidence Distribution')
    ###  Probability Plot
    for class_name, class_value in vis_result.items():
        print('Class:', class_name)
        for key, value in class_value.items():
            print(' - %s:' % key, type(value), value[:4])

    report.content.add_multi_class_confidence_distribution([('', vis_result)])

    ### Lastly generate report with the writer instance
    report.generate(writer=HtmlWriter(name='simple-html-report'))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        print(e)
