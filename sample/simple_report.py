#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Sample Code to generate report """

import sys
sys.path.append('../')
import json

from xai.formatter import Report, PdfWriter

################################################################################
### Sample Report
################################################################################


def main():
    ## Create Report
    report = Report(name='Sample Report')

    ### Create Cover Section
    report.cover.add_section_title(text="Summary")
    report.cover.add_paragraph(text="This is summary Info")

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
    report.content.add_section_title("Example for Data Analysis ")
    ### Add Header Level 1
    report.content.add_header_level_1(text='Data Analysis')

    ### Add Header Level 2
    report.content.add_header_level_2(text='Data Class Distribution')
    ### Add Dataset distribution
    with open('./sample_data/data_distribution.json', 'r') as f:
        data_dist = json.load(f)
    data_distributions = []
    for k, v in data_dist.items():
        data_distributions.append((k, v))
    print(data_distributions)
    report.content.add_data_set_distribution(data_distributions)

    ### Add Header Level 2
    report.content.add_header_level_2(text='Data Field Attribute')
    ### Data Field Attribute
    with open('./sample_data/data_attribute.json', 'r') as f:
        data_attribute = json.load(f)
    print(data_attribute)
    report.content.add_data_attributes(data_attribute)

    ### Add Header Level 2
    report.content.add_header_level_2(text='Data Missing Value Check')
    ### Missing value
    with open('./sample_data/missing_value.json', 'r') as f:
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
    with open('./sample_data/categorical_data.json', 'r') as f:
        categorical_data = json.load(f)
    print(categorical_data)

    for field_name, field_distribution in categorical_data.items():
        report.content.add_categorical_field_distribution(
            field_name=field_name, field_distribution=field_distribution)

    ### Add Header Level 3
    report.content.add_header_level_3(text='Numerical Field Distribution')
    ### Numerical field distribution
    with open('./sample_data/numerical_data.json', 'r') as f:
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
    with open('./sample_data/text_data.json', 'r') as f:
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
    with open('./sample_data/datetime_data.json', 'r') as f:
        datetime_data = json.load(f)
    print(datetime_data)

    for field_name, field_distribution in datetime_data.items():
        report.content.add_datetime_field_distribution(field_name=field_name,
                                                       field_distribution=field_distribution)

    ### Add Header Level 2
    report.content.add_header_level_2(text='Confusion Matrix')
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

    report.content.add_confusion_matrix_results(confusion_matrix_list)

    ### Add Header Level 1
    report.content.add_header_level_1(
        text='Multi-class Classification Evaluation Analysis')

    with open('./sample_data/multi_evaluation_results.json', 'r') as f:
        eval_result = json.load(f)

    label_key = 'label_1'
    label_eval_result = eval_result[label_key]
    vis_result = label_eval_result['vis_result']
    del (label_eval_result['vis_result'])

    ### Add Header Level 2
    report.content.add_header_level_2(text='Confidence Distribution')
    ###  Probability Plot
    for class_name, class_value in vis_result.items():
        print('Class:', class_name)
        for key, value in class_value.items():
            print(' - %s:' % key, type(value), value[:4])

    report.content.add_multi_class_confidence_distribution([('', vis_result)])

    ### Add Header Level 2
    report.content.add_header_level_2(text='Confusion Matrix')
    ### Confusion Matrix
    print(label_eval_result['CM'])

    report.content.add_confusion_matrix_results(
        confusion_matrix_tuple=[('', label_eval_result['CM'])])

    with open('./sample_data/evaluation_result_summary.json', 'r') as f:
        evaluation_result_data = json.load(f)
    print(evaluation_result_data)

    report.cover.add_evaluation_result_summary(
        evaluation_result=evaluation_result_data)

    ### Lastly generate report with the writer instance
    report.generate(writer=PdfWriter(name='sample-report'))

if __name__ == "__main__":
    main()

