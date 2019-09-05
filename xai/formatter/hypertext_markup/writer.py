#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""HTML Report Formatter - Base"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import copy
import shutil
import tempfile

from typing import Tuple, Dict, List

from xai.formatter.contents import Header, SectionTitle, Title
from xai.formatter.report.section import CoverSection, DetailSection

from xai.formatter.hypertext_markup.publisher import CustomHtml, Div
from xai.formatter.writer import Writer


################################################################################
### HTML Writer Visitor
################################################################################
class HtmlWriter(Writer):

    def __init__(self, name='training_report',
                 path='./', ) -> None:
        """
        Generate HTML report

        Args:
            name (str, Optional): filename of report,
                        default is 'training_report'
            path (str, Optional): output path (default current dict './')
        """
        super(HtmlWriter, self).__init__()
        self._path = path
        self._name = name
        self._html = CustomHtml(name=name, path=path)

        # create article division list
        self.html.article.append(Div())

        # set up temporary image folder
        self.figure_path = tempfile.TemporaryDirectory().name
        os.mkdir(self.figure_path)

    @property
    def path(self):
        """Returns PDF output path"""
        return self._path

    @property
    def name(self):
        """Returns PDF report name."""
        return self._name

    @property
    def html(self):
        """Returns HTML File object."""
        return self._html

    def out(self):
        """
        Output Report
        """
        self.html.to_file()
        # clean up temp folder
        if os.path.exists(self.figure_path):
            shutil.rmtree(self.figure_path)

    def build(self, title: str, cover: CoverSection,
              detail: DetailSection, content_table=False):
        """
        Build Report

        Args:
            title(str): header title
            cover(CoverSection): Cover Section of report
            detail(DetailSection): Details Section of report
            content_table (bool): is content table enabled
                            default False
        """
        # -- Create HTML Body Section Header --
        self.html.header.append(self.html.add_header(text=title, heading='h1'))

        # -- Create HTML Body Section Article --
        if len(cover.contents) > 1:
            for content in cover.contents:
                content.draw(writer=self)

        _h1_count = 0
        _h2_count = 0
        _h3_count = 0
        dc_contents = copy.deepcopy(detail.contents)
        for content in dc_contents:
            if isinstance(content, Header):
                if content.level == Header.LEVEL_1:
                    _h1_count += 1
                    _h2_count = 0
                    _h3_count = 0
                    content.text = '%s %s' % (_h1_count, content.text)
                elif content.level == Header.LEVEL_2:
                    _h2_count += 1
                    _h3_count = 0
                    content.text = '%s.%s %s' % (_h1_count, _h2_count,
                                                 content.text)
                elif content.level == Header.LEVEL_3:
                    _h3_count += 1
                    content.text = '%s.%s.%s %s' % (_h1_count, _h2_count,
                                                    _h3_count, content.text)
        if len(dc_contents) > 1:
            for content in dc_contents:
                content.draw(writer=self)

    ################################################################################
    ###  Base Section
    ################################################################################
    def add_new_page(self):
        """
        Add new page
        """
        self.html.article.append(Div())

    def draw_header(self, text: str, level: int, link=None):
        """
        Draw Header

        Args:
            text(str): header text in the report
            level(int): header level
            link: header link
        """
        if level == Header.LEVEL_1:
            self.html.article[-1].items.append(
                self.html.add_header(text=text, heading='h2', link=link))
        elif level == Header.LEVEL_2:
            self.html.article[-1].items.append(
                self.html.add_header(text=text, heading='h3', link=link))
        elif level == Header.LEVEL_3:
            self.html.article[-1].items.append(
                self.html.add_header(text=text, heading='h4', link=link))

    def draw_title(self, text: str, level: int, link=None):
        """
        Draw Title

        Args:
            text(str): title in the report
            level(int): title type (section or paragraph)
            link: title link
        """
        # each section == new page
        self.add_new_page()
        self.html.article[-1].title = text
        self.html.article[-1].items.append(
            self.html.add_header(text=text, heading='h2',
                                 link=link, style=True))

    def draw_paragraph(self, text: str):
        """
        Draw Paragraph

        Args:
            text(str): html text to render in the report
        """
        self.html.article[-1].items.append(self.html.add_paragraph(text=text))

    ################################################################################
    ###  Summary Section
    ################################################################################

    def draw_training_time(self, notes: str, timing: List[Tuple[str, int]]):
        """
        Draw information of timing to the report

        Args:
            notes(str): Explain the block
            timing (:obj:`list` of :obj:`tuple`): list of tuple
                        (name, time in second)
        """
        # -- Draw Content --
        self.html.article[-1].items.append(self.html.add_header(text=notes,
                                                                heading='h3'))
        # self.html.article[-1].items.append(
        #     self.html.create_unordered_kay_value_pair_list(items=timing))
        self.html.article[-1].items.append(
            self.html.create_overview_table(data=timing))


    def draw_data_set_summary(self, notes: str,
                              data_summary: List[Tuple[str, int]]):
        """
        Draw information of dataset summary to the report

        Args:
            notes(str): Explain the block
            data_summary (:obj:`list` of :obj:`tuple`): list of tuple
                        (dataset_name, dataset_sample_number)
        """
        # -- Draw Content --
        self.html.article[-1].items.append(self.html.add_header(text=notes,
                                                                heading='h3'))
        # self.html.article[-1].items.append(
        #     self.html.create_unordered_kay_value_pair_list(items=data_summary))
        self.html.article[-1].items.append(
            self.html.create_overview_table(data=data_summary))

    def draw_evaluation_result_summary(self, notes: str,
                                       evaluation_result: dict):
        """
        Draw information of training performance to the result

        Args:
            evaluation_result (dict): evaluation metric
                - key: metric_name
                - value: metric_value: single float value for average/overall metric,
                                        list for class metrics
                sample input 1: {'precision': 0.5}, report value directly
                sample input 2: {'precision': {'class':[0.5,0.4,0.3],'average':0.5}},
                                            report "average" value
                sample input 3: {'precision': {'class':[0.5,0.4,0.3]},
                                    report unweighted average for "class" value
            notes (str, Optional): explain the block
        """
        import numpy as np
        # -- Draw Content --
        self.html.article[-1].items.append(self.html.add_header(text=notes,
                                                                heading='h3'))
        items = dict()
        for result in evaluation_result:
            for metric_name, metric_value in result.items():
                valid = False
                if type(metric_value) == dict:
                    if 'average' in metric_value.keys():
                        key = "%s (average)" % metric_name.capitalize()
                        if type(metric_value['average']) == float or type(
                                metric_value['average']) == str:
                            value = "%.4f " % metric_value['average']
                    elif 'class' in metric_value.keys():
                        key = "%s (macro average)" % metric_name.capitalize()
                        if type(metric_value['class']) == list:
                            valid = True
                            for e in metric_value['class']:
                                if type(e) != float and type(e) != str:
                                    valid = False
                        if not valid:
                            continue
                        value = "%.4f" % np.mean(
                            np.array(metric_value['class']))
                    else:
                        print(
                            'No defined keys (`class`,`average`) found in metric value: %s' % (
                                metric_value.keys()))
                        continue

                elif type(metric_value) == float:
                    key = "%s" % metric_name.capitalize()
                    value = "%.4f" % metric_value
                elif type(metric_value) == str:
                    key = "%s" % metric_name.capitalize()
                    value = metric_value
                else:
                    print(
                        'Unsupported metric value type for metric (%s): %s' % (
                        metric_name, type(metric_value)))
                    continue
                if key not in items:
                    items[key] = list()
                items.get(key).append(value)

        self.html.article[-1].items.append(
            self.html.add_overview_table_with_dict(data=items))

    def draw_model_info_summary(self, notes: str, model_info: list):
        """
        Draw information of model info to the result

        Args:
            model_info (:obj:`list` of :obj:
              `tuple`, Optional): list of tuple (model info attribute, model info value).
               Default information include `use case name`, `version`, `use case team`.
            notes (str, Optional): explain the block
        """
        # -- Draw Content --
        self.html.article[-1].items.append(self.html.add_header(text=notes,
                                                                heading='h3'))
        # self.html.article[-1].items.append(
        #     self.html.create_unordered_kay_value_pair_list(items=model_info))
        self.html.article[-1].items.append(
            self.html.create_overview_table(data=model_info))


    ################################################################################
    ###  Data Section
    ################################################################################

    def draw_data_missing_value(self, notes: str, missing_count: dict,
                                total_count: dict, ratio=False):
        """
        Draw Missing Data Value Summary Table

        Args:
            notes(str): Explain the block
            missing_count(dict): Missing Count
            total_count(dict): Total Count
            ratio(bool): True if `missing_value` is the percentage
        """
        from collections import defaultdict
        def get_missing_data_info():
            """
            Build missing data summary
            Returns: Missing data summary
                table_header (list):
                table_data (list):
                col_width (list):
            """
            data_dict = defaultdict(dict)
            field_set = set(total_count.keys())
            field_set.update(set(missing_count.keys()))
            for feature_name in field_set:
                if feature_name not in total_count:
                    data_dict[feature_name]['total_count'] = '-'
                else:
                    data_dict[feature_name]['total_count'] = \
                        total_count[feature_name]

                if feature_name not in missing_count:
                    data_dict[feature_name]['missing_value_count'] = 0
                    data_dict[feature_name]['percentage'] = 0
                else:
                    if ratio:
                        data_dict[feature_name]['percentage'] = \
                            missing_count[feature_name]
                        data_dict[feature_name]['missing_value_count'] = '-'
                    else:
                        data_dict[feature_name]['missing_value_count'] = \
                            missing_count[feature_name]
                        if data_dict[feature_name]['total_count'] != '-':
                            data_dict[feature_name]['percentage'] = \
                                data_dict[feature_name][
                                    'missing_value_count'] / \
                                data_dict[feature_name]['total_count']
            if len(total_count) > 0:
                table_header = ['Feature', 'Missing Value Count',
                                'Percentage(%)']
                table_data = []
                for field_name, field_data in data_dict.items():
                    table_data.append(
                        [field_name, "%s / %s" % (
                            field_data['missing_value_count'],
                            field_data['total_count']),
                         "%.2f%%" % field_data['percentage']])
            else:
                if ratio:
                    table_header = ['Feature', 'Missing Value Percentage']
                    table_data = []
                    for field_name, field_data in data_dict.items():
                        table_data.append(
                            [field_name, field_data['percentage']])
                else:
                    table_header = ['Feature', 'Missing Value Count']
                    table_data = []
                    for field_name, field_data in data_dict.items():
                        table_data.append(
                            [field_name, field_data['missing_value_count']])

            return table_header, table_data

         # -- Draw Content --
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        header, data = get_missing_data_info()
        if len(data) > 0:
            self.html.article[-1].items.append(
                self.html.add_table(header=header, data=data))

    def draw_data_set_distribution(self, notes: str,
                                   data_set_distribution: Tuple[str, dict],
                                   max_class_shown=20):
        """
        Draw information of distribution on data set

        Args:
            notes(str): Explain the block
            data_set_distribution (tuple: (str,dict)):
                - tuple[0] str: label/split name
                - tuple[1] dict: key - class_name/split_name,
                                 value - class_count/split_count
            max_class_shown (int, Optional): maximum number of classes shown
                          in the figure, default is 20
            notes (str, Optional):
                explain the block
        """
        from xai.graphs import graph_generator
        def get_data_set_distribution():
            code = dict()
            for ds_name, ds_dist in data_set_distribution:
                code[ds_name] = sum(list(ds_dist.values()))
            return code

        # -- Draw Content --
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        dist_count = get_data_set_distribution()

        for name, dist in data_set_distribution:
            title = "Data Distribution for %s" % name
            self.html.article[-1].items.append(
                self.html.add_header(text=title, heading='h3'))
            self.html.article[-1].items.append(
                self.html.add_paragraph(text='Count: %s' %
                                             dist_count.get(name), style='B'))
            if len(dist) > max_class_shown:
                self.html.article[-1].items.append(
                    self.html.add_paragraph(
                        text='(Only %s shown amount %s classes)' % (
                            max_class_shown, len(dist))))

            image_path = graph_generator.BarPlot(
                file_path='%s/%s_data_distribution.png' % (self.figure_path,
                                                           name),
                data=dist, title=title,
                x_label='Number of samples',
                y_label='Category').draw(caption=name,
                                         ratio=True,
                                         limit_length=max_class_shown)
            self.html.article[-1].items.append(
                self.html.add_image(src=image_path, alt=title))

    def draw_data_attributes(self, notes: str, data_attribute: Dict):
        """
        Draw information of data attribute for data fields to the report

        Args:
            notes(str): Explain the block
            data_attribute (:dict of :dict):
                -key: data field name
                -value: attributes (dict)
                    - key: attribute name
                    - value: attribute value
        """
        def get_data_attributes():
            attribute_list = list(
                set().union(*[set(attribute_dict.keys())
                              for attribute_dict in data_attribute.values()]))
            table_header = ['Field Name'] + [attribute.capitalize()
                                             for attribute in attribute_list]

            table_data = []
            for field_name, field_attributes in data_attribute.items():
                row = [field_name]
                for attribute_name in attribute_list:
                    if attribute_name in field_attributes.keys():
                        row.append(field_attributes[attribute_name])
                    else:
                        row.append('-')
                table_data.append(row)

            return table_header, table_data

        # -- Draw Content --
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        header, data = get_data_attributes()
        self.html.article[-1].items.append(
            self.html.add_table(header=header, data=data))

    def draw_categorical_field_distribution(self, notes: str,
                                            field_name: str,
                                            field_distribution: dict,
                                            max_values_display=20,
                                            colors=None):
        """
        Draw information of field value distribution for categorical type to
        the report.

        Args:
            notes(str): Explain the block
            field_name (str): data field name
            field_distribution (:dict of :dict):
                -key: label_name
                -value: frequency distribution under the `label_name`(dict)
                    - key: field value
                    - value: field value frequency
            max_values_display (int): maximum number of values displayed
            colors (list): the list of color code for rendering different class
        """
        from xai.graphs import graph_generator
        if colors is None:
            colors = ["Blues_d", "Reds_d", "Greens_d", "Purples_d",
                      "Oranges_d"]
        # -- Draw Content --
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        for idx, (label_name, frequency_distribution) in enumerate(
                field_distribution.items()):
            title = 'For %s samples' % label_name
            self.html.article[-1].items.append(
                self.html.add_header(text=title, heading='h5'))
            if len(frequency_distribution) / sum(
                    frequency_distribution.values()) > 0.5:
                self.html.article[-1].items.append(
                    self.html.add_paragraph(text=
                    'Warning: %s unique values found in %s samples.' % (
                        len(frequency_distribution),
                        sum(frequency_distribution.values()))), style='BI')
                break

            if len(field_distribution) > max_values_display:
                self.html.article[-1].items.append(
                    self.html.add_paragraph(text='%s of %s are displayed)' % (
                    max_values_display, len(field_distribution))))

            figure_path = '%s/%s_%s_field_distribution.png' % (
                self.figure_path, field_name, label_name)
            image_path = graph_generator.BarPlot(file_path=figure_path,
                                                 data=frequency_distribution,
                                                 title=title,
                                                 x_label="",
                                                 y_label=field_name).draw(
                limit_length=max_values_display,
                color_palette=colors[idx % len(colors)])
            self.html.article[-1].items.append(
                self.html.add_image(src=image_path, alt=title))

    def draw_numeric_field_distribution(self, notes: str,
                                        field_name: str,
                                        field_distribution: dict,
                                        force_no_log=False,
                                        x_limit=False,
                                        colors=None):
        """
         Draw information of field value distribution for numerical type to
         the report.

         Args:
             notes(str): Explain the block
             field_name (str): data field name
             field_distribution (:dict of :dict):
                 -key: label_name
                 -value: numeric statistics
                     - key: statistics name
                     - value: statistics value
                 each field_distribution should must have 2 following predefined keys:
                 - histogram (:list of :list): a list of bar specification
                                                (x, y, width, height)
                 - kde (:list of :list, Optional): a list of points which
                                    draw`kernel density estimation` curve.

             force_no_log (bool): whether to change y-scale to logrithmic
                                              scale for a more balanced view
             x_limit (list:): whether x-axis only display the required percentile range.
                             If True, field_distribution should have a
                             key "x_limit" and value of [x_min, x_max].
             colors (list): the list of color code for rendering different class
        """
        pass

    def draw_text_field_distribution(self, notes: str,
                                     field_name: str,
                                     field_distribution: dict):
        """
        Draw information of field value distribution for text type to the
        report.

        Args:
            notes(str): Explain the block
            field_name (str): data field name
            field_distribution (:dict of :dict):
                -key: label_name
                -value: tfidf and placeholder distribution under the `label_name`(dict):
                    {'tfidf': tfidf, 'placeholder': placeholder}
                    - tfidf (:list of :list): each sublist has 2 items: word and tfidf
                    - placeholder (:dict):
                        - key: PATTERN
                        - value: percentage
        """
        pass

    def draw_datetime_field_distribution(self, notes: str,
                                         field_name: str,
                                         field_distribution: dict):
        """
        Draw information of field value distribution for datetime type to the
        report.

        Args:
            notes(str): Explain the block
            field_name (str): data field name
            field_distribution (:dict of :dict):
                -key: label_name
                -value (:dict of :dict):
                    - 1st level key: year_X(int)
                    - 1st level value:
                        - 2nd level key: month_X(int)
                        - 2nd level value: count of sample in month_X of year_X
        """
        pass

    ################################################################################
    ###  Feature Section
    ################################################################################

    def draw_feature_importance(self, notes: str,
                                importance_ranking: List[List],
                                importance_threshold: float,
                                maximum_number_feature=20):
        """
        Add information of feature importance to the report.

        Args:
            notes(str): Explain the block
            importance_ranking(:list of :list): a list of 2-item lists,
                                        item[0]: score, item[1] feature_name
            importance_threshold(float): threshold for displaying the feature
                                        name and score in tables
            maximum_number_feature(int): maximum number of features shown in bar-chart diagram
        """
        pass

    ################################################################################
    ###  Training Section
    ################################################################################

    def draw_hyperparameter_tuning(self, notes: str,
                                   history: dict, best_idx: str,
                                   search_space=None, benchmark_metric=None,
                                   benchmark_threshold=None,
                                   non_hyperopt_score=None):
        """
        Add information of hyperparameter tuning to the report.

        Args:
            notes(str): Explain the block
            history(:dict of dict): a dict of training log dict.
                key: iteration index
                value: hyperparameter tuning information
                        Each dict has two keys:
                            - params: a dict of which key is the parameter name
                                        and value is parameter value
                            - val_scores: a dict of which key is the metric name
                                        and value is metric value
            best_idx(str):
                - the best idx based on benchmark metric, corresponding the `history` dict key
            search_space(:dict): parameter name and the search space for each parameter
            benchmark_metric(:str): the metric used for benchmarking during hyperparameter tuning
            benchmark_threshold(:float, Optional): the benchmarking threshold to accept the training
            non_hyperopt_score(:float, Optional): the training metric without hyperparameter tuning
        """
        pass

    def draw_learning_curve(self, notes: str,
                            history: dict, best_idx: str,
                            benchmark_metric=None, benchmark_threshold=None,
                            training_params=None):
        """
        Add information of learning curve to report.

        Args:
            notes(str): Explain the block
            history(:dict of dict): a dict of training log dict.
                key: epoch index
                value: learning epoch information
                        Each dict has two keys:
                            - params: a dict of params on current epochs (Optional)
                            - val_scores: a dict of which key is the metric name
                                      and value is metric value
            best_idx(str):
                - the best epoch based on benchmark metric, corresponding the `history` dict key
            benchmark_metric(:str): the metric used for benchmarking during learning
            benchmark_threshold(:float, Optional): the benchmarking threshold to accept the training
            training_params(:dict): a dict of which key is training parameter name and
                                    value is training parameter value
        """
        pass

    ################################################################################
    ###  Evaluation Section
    ################################################################################

    def draw_multi_class_evaluation_metric_results(self, notes: str,
                                                   metric_tuple):
        """
        Add information about metric results for multi-class evaluation

        Args:
            notes(str): Explain the block
            *metric_tuple(tuple): (evaluation_header, evaluation_metric_dict)
                - evaluation_header(str): a header for current evaluation,
                                            can be split or round number.
                - evaluation_metric_dict(dict): key-value pair for metric
                    - key: metric name
                    - value: metric dict. The dict should either
                     (1) have a `class` keyword, with key-value pair of class name
                                            and corresponding values, or
                     (2) have a `average` keyword to show a macro-average metric.
        """
        pass

    def draw_binary_class_evaluation_metric_results(self, notes: str,
                                                    metric_tuple: tuple,
                                                    aggregated=True):
        """
        Add information about metric results for binary-class evaluation

        Args:
            notes(str): Explain the block
            metric_tuple(tuple): (evaluation_header, evaluation_metric_dict)
                - evaluation_header(str): a header for current evaluation,
                                    can be split or round number.
                - evaluation_metric_dict(dict): key-value pair for metric
                    - key: metric name
                    - value: metric value
            aggregated(bool): whether to aggregate multiple result tables into one
        """
        pass

    def draw_confusion_matrix_results(self, notes: str,
                                      confusion_matrix_tuple: tuple):
        """
        Add information about confusion matrix to report

        Args:
            notes(str): Explain the block
            confusion_matrix_tuple(tuple): (confusion_matrix_header, confusion_matrix_dict)
                - confusion_matrix_header(str): a header for confusion_matrix,
                                                can be split or round number.
                - confusion_matrix_dict(dict):
                    - `labels`(:list of :str): label of classes
                    - `values`(:list of :list): 2D list for confusion matrix value,
                                            row for predicted, column for true.
        """
        pass

    def draw_multi_class_confidence_distribution(self, notes: str,
                                                 visual_result_tuple: tuple,
                                                 max_num_classes=9):
        """
        Add information about multi class confidence distribution to report

        Args:
            notes(str): Explain the block
            visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
               - visual_result_header(str): a header for confusion_matrix,
                                            can be split or round number.
               - visual_result_dict(dict): key-value
                   - key(str): the predicted class
                   - value(dit): result dict
                        - `gt` (:list of :str): ground truth class label for all samples
                        - `values` (:list of :float): probability for all samples
            max_num_classes(int, Optional): maximum number of classes
                                    displayed for each graph, default 9
        """
        pass

    def draw_binary_class_confidence_distribution(self, notes: str,
                                                  visual_result_tuple: tuple):
        """
        Add information about binary class confidence distribution to report

        Args:
            notes(str): Explain the block
            visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
               - visual_result_header(str): a header for confusion_matrix,
                                                can be split or round number.
               - visual_result_dict(dict): key-value
                    - `gt` (:list of :str): ground truth class label for all samples
                    - `probability` (:list of :list): 2D list (N sample * 2) to
                                    present probability distribution of each sample
        """
        pass

    def draw_binary_class_reliability_diagram(self,
                                              visual_result_tuple: tuple,
                                              notes=None):
        """
        Add information about reliability to report

        Args:
            notes(str): Explain the block
            visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
               - visual_result_header(str): a header for confusion_matrix,
                                        can be split or round number.
               - visual_result_dict(dict): key-value
                    - `gt` (:list of :str): ground truth class label for all samples
                    - `probability` (:list of :list): 2D list (N sample * 2) to
                            present probability distribution of each sample
        """
        pass
