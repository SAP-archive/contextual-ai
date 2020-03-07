#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Test Case to generate html report """

import json
import os
import sys
import unittest
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from datetime import datetime

sys.path.append('../../')

from xai.data import DataUtil
from xai.data.constants import DATATYPE

from xai.model.interpreter import FeatureInterpreter
from xai.formatter import Report, HtmlWriter

from tests.formatter.util import prepare_input_path, prepare_output_path

################################################################################
### Generate HTML Report
################################################################################

class TestGenerateHtmlReport(unittest.TestCase):
    """
    Test Case to generate html report
    """

    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        self.name = None
        self.report_name = None
        self.report = None
        self.tag_number = 0

    def test_add_overview(self):
        self.name = "overview"
        self.report_name = "Overview Report"
        self.tag_number = 1
        ## Create Report
        self.report = Report(name=self.report_name)

        ### Create Cover Section
        self.report.overview.add_new_page()
        self.report.overview.add_section_title(text="Overview")
        self.report.overview.add_paragraph(text="This is summary Info")
        model_info = [('Model ID', '12345678'),
                      ('Model Version', 'v6'),
                      ('Scenario ID', '111222333444555'),
                      ('Notes', 'This model is created as a beta version.')
                  ]
        self.report.overview.add_model_info_summary(model_info=model_info)

        timing = [('Data Preprocessing', 1000),
                  ('Feature Engineering', 10000),
                  ('Training', 200200),
                  ('Evaluation', 30303)]
        self.report.overview.add_training_timing(timing=timing)

        data_summary = [('training', 10000),
                        ('validation', 2000),
                        ('testing', 1000)]
        self.report.overview.add_data_set_summary(data_summary=data_summary)

        with open(prepare_input_path(
                data_path='sample_data/evaluation_result_summary.json'),
                'r') as f:
            evaluation_result_data = json.load(f)
        print(evaluation_result_data)

        self.report.overview.add_evaluation_result_summary(
            evaluation_result=evaluation_result_data)
        print(self.report.overview.contents)
        ### added 7 component but length of overview is 8,
        ### there is a default component - new page at the beginning (init)
        self.assertEqual(len(self.report.overview.contents), 8)

    def test_add_header_in_detail(self):
        self.name = "header"
        self.report_name = "Header Report"
        self.tag_number = 1
        ## Create Report
        self.report = Report(name=self.report_name)
        ### Create Contents Section - Header
        self.report.detail.add_section_title(text="Example for Header")
        #### Header Level 1 and it paragraph
        self.report.detail.add_header_level_1(text='Section Header 1')
        self.report.detail.add_paragraph(text="This is content Info of header 1")
        #### Header Level 2 and it paragraph
        self.report.detail.add_header_level_2(text='Section Header 2')
        self.report.detail.add_paragraph(text="This is content Info of header 2")
        #### Header Level 3 and it paragraph
        self.report.detail.add_header_level_3(text='Section Header 3')
        self.report.detail.add_paragraph(text="This is content Info of header 3")
        print(self.report.detail.contents)
        ### There is no default new page -
        self.assertEqual(len(self.report.detail.contents), 7)


    def test_add_basic_key_value_pairs(self):
        self.name = "basic-key-value-pairs"
        self.report_name = "Basic Key-Value Pairs Report"
        self.tag_number = 1
        ## Create Report
        self.report = Report(name=self.report_name)
        ### Create Basic Info Section
        self.report.detail.add_new_page()
        self.report.detail.add_section_title("Example for Basic Info ")
        ### Add Header Level 1
        self.report.detail.add_header_level_1(
            text='Business Logic Filter')
        info_list = list()
        info_list.append(("Filtered Sample Count", 1208))
        info_list.append(("Unique Value Count", [
            ("BANKSTATEMENTKEY[BS]", 725),
            ("RECEIVABLEKEY[RC]", 1208),
            ("Test[3rd-level]", [("result", "it is right?")])
        ]))
        print(info_list)
        self.report.detail.add_key_value_pairs(info_list=info_list,
                                               notes="Filter Name: "
                                                     "<B>advance_payment</B>")
        print(self.report.detail.contents)
        self.assertEqual(len(self.report.detail.contents), 4)

    def test_add_basic_table(self):
        self.name = "basic-table"
        self.report_name = "Basic Table Report"
        self.tag_number = 1
        ## Create Report
        self.report = Report(name=self.report_name)
        ### Create Basic Info Section
        self.report.detail.add_new_page()
        self.report.detail.add_section_title("Example for Basic Table ")
        ### Add Header Level 1
        self.report.detail.add_header_level_1(
            text='Team Info Table')
        header_list = ["Name", "Team"]
        print(header_list)
        data_list = [["Chai", "MKT"], ["NP", "MKT"],
                     ["WJ", "CA"], ["Sean", "CA"]]
        print(data_list)
        self.report.detail.add_table(table_header=header_list,
                                     table_data=data_list,
                                     col_width=[20, 20],
                                     notes="Team Info")
        print(self.report.detail.contents)
        self.assertEqual(len(self.report.detail.contents), 4)

    def test_add_data_analysis(self):
        self.name = "data-analysis"
        self.report_name = "Data Analysis Report"
        self.tag_number = 1
        ## Create Report
        self.report = Report(name=self.report_name)
        ### Create Data Analysis Section
        self.report.detail.add_section_title("Example for Data Analysis ")
        ### Add Header Level 1
        self.report.detail.add_header_level_1(text='Data Analysis')
        self.assertEqual(len(self.report.detail.contents), 2)

        ### Load Data
        file_name = prepare_input_path(data_path='sample_data/titanic.csv')
        data = pd.read_csv(file_name)
        ### Add dummy birthday to demonstrate datetime presentation
        bday = []
        for i in range(len(data)):
            year = np.random.randint(low=1960, high=1979)
            month = np.random.randint(low=1, high=12)
            day = np.random.randint(low=1, high=28)
            bday.append("%s" % (10000 * year + 100 * month + day))
        data['Birthday'] = bday

        label_column = 'Survived'

        ### Get data types - scenario where no metadata provided
        feature, valid_feature_names, valid_feature_types, meta = \
            DataUtil.get_column_types(data=data, threshold=0.3,
                                      label=label_column)
        # -- Cast Data to String --
        non_numeric_features = [name for name, _type in
                                list(zip(valid_feature_names,
                                         valid_feature_types))
                                if _type != DATATYPE.NUMBER]
        if label_column is not None:
            non_numeric_features += [label_column]
        DataUtil.cast_type_to_string(data=data,
                                     feature_names=non_numeric_features)

        ### Add Header Level 2
        self.report.detail.add_header_level_2(
            text='Data Class (Label) Distribution')
        ### Add Label distribution
        label_distributions = DataUtil.get_label_distribution(data=data,
                                                              label=label_column)
        self.report.detail.add_data_set_distribution(label_distributions)
        self.assertEqual(len(self.report.detail.contents), 4)

        ### Get Data Stats
        stats = DataUtil.get_data_statistics(data=data,
                                             feature_names=valid_feature_names,
                                             feature_types=valid_feature_types,
                                             label=label_column)

        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Data Field Attribute')
        ### Data Field Attribute
        self.report.detail.add_data_attributes(meta)
        self.assertEqual(len(self.report.detail.contents), 6)

        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Data Missing Value Check')
        ### Missing value count
        missing_count, total_count = \
            DataUtil.get_missing_value_count(data=data,
                                             feature_names=valid_feature_names,
                                             feature_types=valid_feature_types)
        print(missing_count)
        self.assertEqual(missing_count['Age'], 177)
        self.assertEqual(missing_count['Embarked'], 2)
        print(total_count)
        self.assertEqual(total_count['Name'], 891)
        self.assertEqual(total_count['Embarked'], 891)
        self.assertEqual(len(self.report.detail.contents), 7)
        self.report.detail.add_data_missing_value(
            missing_count=dict(missing_count),
            total_count=total_count)
        self.assertEqual(len(self.report.detail.contents), 8)

        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Data Field Distribution')
        ### Data Field Distribution Desc
        self.report.detail.add_paragraph(
            text='This section displays distribution for categorical fields, numerical fields and text fields.')
        self.assertEqual(len(self.report.detail.contents), 10)

        ### Add Header Level 3
        self.report.detail.add_header_level_3(
            text='Categorical Field Distribution')
        print(feature[DATATYPE.CATEGORY])
        self.assertEqual(len(feature[DATATYPE.CATEGORY]), 5)
        ### Categorical field distribution
        for field_name in feature[DATATYPE.CATEGORY]:
            labelled_stats, all_stats = stats[field_name]
            self.report.detail.add_categorical_field_distribution(
                field_name=field_name, field_distribution=labelled_stats)
        self.assertEqual(len(self.report.detail.contents), 16)

        ### Add Header Level 3
        self.report.detail.add_header_level_3(
            text='Numerical Field Distribution')
        print(feature[DATATYPE.NUMBER])
        self.assertEqual(len(feature[DATATYPE.NUMBER]), 2)
        ### Numerical field distribution
        for field_name in feature[DATATYPE.NUMBER]:
            labelled_stats, all_stats = stats[field_name]
            self.report.detail.add_numeric_field_distribution(
                field_name=field_name, field_distribution=labelled_stats)
        self.assertEqual(len(self.report.detail.contents), 19)

        ### Add Header Level 3
        self.report.detail.add_header_level_3(text='Text Field Distribution')
        print(feature[DATATYPE.FREETEXT])
        self.assertEqual(len(feature[DATATYPE.FREETEXT]), 1)
        ### Text field distribution
        for field_name in feature[DATATYPE.FREETEXT]:
            labelled_stats, all_stats = stats[field_name]
            self.report.detail.add_text_field_distribution(
                field_name=field_name, field_distribution=labelled_stats)
        self.assertEqual(len(self.report.detail.contents), 21)

        ### Add Header Level 3
        self.report.detail.add_header_level_3(
            text='Datetime Field Distribution')
        print(feature[DATATYPE.DATETIME])
        self.assertEqual(len(feature[DATATYPE.DATETIME]), 1)
        ### Datetime field distribution
        for field_name in feature[DATATYPE.DATETIME]:
            labelled_stats, all_stats = stats[field_name]
            self.report.detail.add_datetime_field_distribution(
                field_name=field_name, field_distribution=labelled_stats)

        print(self.report.detail.contents)
        self.assertEqual(len(self.report.detail.contents), 23)


    def test_add_feature_analysis(self):
        self.name = "feature-analysis"
        self.report_name = "Feature Analysis Report"
        self.tag_number = 2
        ## Create Report
        self.report = Report(name=self.report_name)
        ### Create Feature Analysis Section as new page
        self.report.detail.add_new_page()
        self.report.detail.add_section_title("Example for Feature Analysis ")
        ### Add Header Level 1
        self.report.detail.add_header_level_1(text='Feature Analysis')
        self.assertEqual(len(self.report.detail.contents), 3)

        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Feature Importance')
        self.assertEqual(len(self.report.detail.contents), 4)
        ### Feature Importance
        path =  Path(prepare_input_path(data_path='sample_data/model.pkl'))
        model = pd.read_pickle(str(path))
        path = Path(prepare_input_path(data_path='sample_data/train_data.csv'))
        data = pd.read_csv(str(path))
        # -- csv including header --
        feature_names = data.columns

        fi = FeatureInterpreter(feature_names=feature_names)
        rank = fi.get_feature_importance_ranking(trained_model=model,
                                                 train_x=data,
                                                 method='default')
        self.report.detail.add_feature_importance(
            importance_ranking=rank, importance_threshold=0.005)
        self.assertEqual(len(self.report.detail.contents), 5)

        ### Create Performance Analysis Section as new page
        self.report.detail.add_new_page()
        self.report.detail.add_section_title(
            "Example for Performance Analysis ")
        self.report.detail.add_paragraph(
            text='this is dummy model, no trained with titanic dataset')
        ### Add Header Level 1
        self.report.detail.add_header_level_1(text='Performance Analysis')
        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Hyperparameter Tuning')
        self.assertEqual(len(self.report.detail.contents), 10)

        ### Hyperparameter Tuning
        with open(prepare_input_path(
                data_path='sample_data/hyperparameter_tuning.json'),'r') as f:
            hyperparameter_tuning = json.load(f)
        print('search_space:', hyperparameter_tuning['search_space'])
        print('best_idx:', hyperparameter_tuning['best_idx'])
        self.assertEqual(hyperparameter_tuning['best_idx'], '3')
        print('history [first 2 samples]:',
              {k: hyperparameter_tuning['history'][k] for k in
               list(hyperparameter_tuning['history'].keys())[:2]})
        print('benchmark_metric:', hyperparameter_tuning['benchmark_metric'])
        self.assertEqual(hyperparameter_tuning['benchmark_metric'], 'accuracy')
        print('benchmark_threshold:',
              hyperparameter_tuning['benchmark_threshold'])
        self.assertEqual(hyperparameter_tuning['benchmark_threshold'], 0.8)
        print('non_hyperopt_score:',
              hyperparameter_tuning['non_hyperopt_score'])

        self.report.detail.add_hyperparameter_tuning(
            history=hyperparameter_tuning['history'],
            best_idx=hyperparameter_tuning['best_idx'],
            search_space=hyperparameter_tuning['search_space'],
            benchmark_metric=hyperparameter_tuning['benchmark_metric'],
            benchmark_threshold=hyperparameter_tuning['benchmark_threshold'],
            non_hyperopt_score=hyperparameter_tuning['non_hyperopt_score'])
        print(self.report.detail.contents)
        self.assertEqual(len(self.report.detail.contents), 11)


    def test_add_training_analysis(self):
        self.name = "training-analysis"
        self.report_name = "Training Analysis Report"
        self.tag_number = 1
        ## Create Report
        self.report = Report(name=self.report_name)
        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Deep Learning Training')
        ### Learning Curve
        with open(prepare_input_path(
                data_path='sample_data/learning_curve.json'), 'r') as f:
            learning_curve = json.load(f)

        print('best_idx:', learning_curve['best_idx'])
        print('history [first 2 samples]:',
              {k: learning_curve['history'][k] for k in
               list(learning_curve['history'].keys())[:2]})
        print('benchmark_metric:', learning_curve['benchmark_metric'])
        print('benchmark_threshold:', learning_curve['benchmark_threshold'])
        print('training_params:', learning_curve['training_params'])

        self.report.detail.add_learning_curve(
            history=learning_curve['history'],
            best_idx=learning_curve['best_idx'],
            benchmark_metric=learning_curve['benchmark_metric'],
            benchmark_threshold=learning_curve['benchmark_threshold'],
            training_params=learning_curve['training_params'])

    # TODO: Migrate to new format - assert need to update
    def test_add_model_evaluation(self):
        self.name = "model-evaluation"
        self.report_name = "Model Evaluation Report"
        self.tag_number = 1
        ## Create Report
        self.report = Report(name=self.report_name)
        ### Create Data Evaluation Section
        self.report.detail.add_new_page()
        self.report.detail.add_section_title("Example for Data Evaluation")

        ### Add Header Level 1
        self.report.detail.add_header_level_1(
            text='Binary Classification Evaluation Analysis')
        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Overall Result')
        self.assertEqual(len(self.report.detail.contents), 4)

        ### Numeric Metric
        # with open(prepare_input_path(data_path='sample_data/binary_evaluation_results.json'), 'r') as f:
        #     eval_result = json.load(f)
        #
        # splits = eval_result.keys()
        # numeric_metrics_list = []
        #
        # for split in splits:
        #     label_eval_result = eval_result[split]
        #     del (label_eval_result['vis_result'])
        #     numeric_metrics_list.append((split, label_eval_result))
        # print(numeric_metrics_list)
        #
        # self.report.detail.add_binary_class_evaluation_metric_results(
        #     numeric_metrics_list,
        #     notes='The section shows general results like accuracy, precision, recall.')

        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Confusion Matrix')
        ### Confusion Matrix
        # with open(prepare_input_path(data_path='sample_data/binary_evaluation_results.json'), 'r') as f:
        #     eval_result = json.load(f)
        # splits = eval_result.keys()
        # confusion_matrix_list = []
        #
        # for split in splits:
        #     label_eval_result = eval_result[split]
        #     confusion_matrix_list.append((split,
        #                                   {"labels": ["Negative", "Positive"],
        #                                    "values": label_eval_result["CM"]}))
        # print(confusion_matrix_list)
        #
        # self.report.detail.add_confusion_matrix_results(
        #     confusion_matrix_tuple=confusion_matrix_list)
        self.assertEqual(len(self.report.detail.contents), 5)

        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Confidence Distribution')
        ### Confidence Distribution
        # with open(prepare_input_path(data_path='sample_data/binary_evaluation_results.json'), 'r') as f:
        #     eval_result = json.load(f)
        #
        # splits = eval_result.keys()
        # probability_plot_list = []
        #
        # for split in splits:
        #     vis_result = eval_result[split]['vis_result']
        #     probability_plot_list.append((split, vis_result))
        #     print('Split name:', split)
        #     for key, value in vis_result.items():
        #         print(' - %s:' % key, type(value), value[:3])
        #
        # self.report.detail.add_binary_class_confidence_distribution(
        #     probability_plot_list)
        self.assertEqual(len(self.report.detail.contents), 6)

        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Reliability Diagram')
        ### Reliability Diagram
        # with open(prepare_input_path(data_path='sample_data/binary_evaluation_results.json'), 'r') as f:
        #     eval_result = json.load(f)
        #
        # splits = eval_result.keys()
        # probability_plot_list = []
        #
        # for split in splits:
        #     label_eval_result = eval_result[split]['vis_result']
        #     probability_plot_list.append((split, vis_result))
        #     print('Split name:', split)
        #     for key, value in vis_result.items():
        #         print(' - %s:' % key, type(value), value[:3])
        #
        # self.report.detail.add_binary_class_reliability_diagram(probability_plot_list)
        self.assertEqual(len(self.report.detail.contents), 7)

        ### Add Header Level 1
        self.report.detail.add_header_level_1(
            text='Multi-class Classification Evaluation Analysis')
        # with open(prepare_input_path(data_path='sample_data/multi_evaluation_results.json'), 'r') as f:
        #     eval_result = json.load(f)
        #
        # label_key = 'label_1'
        # label_eval_result = eval_result[label_key]
        # vis_result = label_eval_result['vis_result']
        # del (label_eval_result['vis_result'])
        self.assertEqual(len(self.report.detail.contents), 8)

        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Overall Result')
        ### Numeric Metrics
        # print(label_eval_result)
        #
        # ### Add Header Level 2
        # report.detail.add_header_level_2(text='Confusion Matrix')
        # ### Confusion Matrix
        # print(label_eval_result['CM'])
        #
        # self.report.detail.add_confusion_matrix_results(
        #     confusion_matrix_tuple=[('', label_eval_result['CM'])])
        self.assertEqual(len(self.report.detail.contents), 9)

        ### Add Header Level 2
        self.report.detail.add_header_level_2(text='Confidence Distribution')
        ###  Probability Plot
        # for class_name, class_value in vis_result.items():
        #     print('Class:', class_name)
        #     for key, value in class_value.items():
        #         print(' - %s:' % key, type(value), value[:4])
        #
        # self.report.detail.add_multi_class_confidence_distribution([('', vis_result)])
        self.assertEqual(len(self.report.detail.contents), 10)



    def tearDown(self) -> None:
        ### Lastly generate report with the writer instance
        name = '{}-html-report'.format(self.name)
        dir_path = prepare_output_path(working_path='sample_output')
        css = os.path.join(dir_path, 'simple.css')
        js = os.path.join(dir_path, 'simple.js')

        start_time = datetime.now().replace(microsecond=0).replace(second=0)
        self.report.generate(writer=HtmlWriter(name=name,
                                               path=dir_path,
                                               style=css,
                                               script=js))
        end_time = datetime.now().replace(microsecond=0).replace(second=0)
        output = "%s/%s.html" % (dir_path, name)
        print("report generated %s:" % output)

        def time_in_range(start, end, x):
            """Return true if x is in the range [start, end]"""
            if start <= end:
                return start <= x <= end
            else:
                return start <= x or x <= end

        with open(output) as f:
            read_data = f.read()

        index = read_data.find(self.report_name)
        # -- the header start at index 1279 --
        self.assertEqual(index, 1279)

        index = read_data.find('created on')
        create_date = read_data[index+11: index+27]
        print(create_date)
        report_time = datetime.strptime(create_date, '%Y-%m-%d %H:%M')
        self.assertTrue(time_in_range(start_time, end_time, report_time))

        number_of_tags = read_data.count('class="tab_contents"')
        # print(number_of_tags)
        self.assertEqual(number_of_tags, self.tag_number)

# -- Main --
if __name__ == "__main__":
    unittest.main()
