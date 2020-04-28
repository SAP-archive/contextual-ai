#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""HTML Report Formatter - Base"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import copy
import os
import tempfile
import warnings

import shutil
from typing import Tuple, Dict, List
import numpy


from xai import (
 MODE
)

from xai.data.explorer import (
    CategoricalStats,
    NumericalStats,
    TextStats,
    DatetimeStats
)
from xai.formatter.contents import (
    Header,
    Title,
    SectionTitle
)
from xai.formatter.hypertext_markup.publisher import CustomHtml, Div
from xai.formatter.report.section import OverviewSection, DetailSection
from xai.formatter.writer import Writer


################################################################################
### HTML Writer Visitor
################################################################################
class HtmlWriter(Writer):

    def __init__(self, name='training_report',
                 path='./',
                 style=None,
                 script=None
                 ) -> None:
        """
        Generate HTML report

        Args:
            name (str, Optional): filename of report,
                        default is 'training_report'
            path (str, Optional): output path (default current dict './')
            style (str, Optional): css style file path
                       (default to same as 'path')
            script (str, Optional): jsp script file path
                       (default to same as 'path')
        """
        super(HtmlWriter, self).__init__()
        self._path = path
        self._name = name
        self._html = CustomHtml(name=name, path=path, style=style, script=script)

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

    def build(self, title: str, overview: OverviewSection,
              detail: DetailSection, *, content_table=False):
        """
        Build Report

        Args:
            title(str): header title
            overview(OverviewSection): Cover Section of report
            detail(DetailSection): Details Section of report
            content_table (bool): is content table enabled
                            default False
        """
        # -- Create HTML Body Section Header --
        self.html.header.append(self.html.add_header(text=title, heading='h1'))

        # -- Create HTML Body Section Article --
        if len(overview.contents) > 1:
            for content in overview.contents:
                content.draw(writer=self)

        _h1_count = 0
        _h2_count = 0
        _h3_count = 0
        dc_contents = copy.deepcopy(detail.contents)
        for content in dc_contents:
            if isinstance(content, SectionTitle) and \
                    content.level == Title.SECTION_TITLE:
                _h1_count += 1
                _h2_count = 0
                _h3_count = 0
                content.text = '%s %s' % (_h1_count, content.text)
            elif isinstance(content, Header):
                if content.level == Header.LEVEL_1:
                    _h2_count += 1
                    _h3_count = 0
                    content.text = '%s.%s %s' % (_h1_count, _h2_count,
                                                 content.text)
                elif content.level == Header.LEVEL_2:
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

    def draw_header(self, text: str, level: int, *, link=None):
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

    def draw_title(self, text: str, level: int, *, link=None):
        """
        Draw Title

        Args:
            text(str): title in the report
            level(int): title type (section or paragraph)
            link: title link
        """
        if level == Title.SECTION_TITLE:
            self.html.article[-1].title = text
            self.html.article[-1].items.append(
                self.html.add_header(text=text, heading='h2',
                                     link=link, style=True))
        elif level == Title.PARAGRAPH_TITLE:
            self.html.article[-1].items.append(
                self.html.add_paragraph(text=text, style='BI'))

    def draw_paragraph(self, text: str):
        """
        Draw Paragraph

        Args:
            text(str): html text to render in the report
        """
        self.html.article[-1].items.append(self.html.add_paragraph(text=text))

    ################################################################################
    ###  Basic/Reusable Section
    ################################################################################
    def draw_basic_key_value_pairs(self, notes: str, *,
                                   info: list):
        """
        Draw key-value pairs information to the report

        Args:
            notes(str): Explain the block
            info (list): list of tuple / list of (list of tuple))
                multi-level rendering, e.g. to display `model_info`
        """
        # -- Draw Content --
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        self.html.article[-1].items.append(
            self.html.add_basic_nested_info(data=info))

    def draw_basic_table(self, notes: str, *,
                         table_header: list, table_data: list,
                         col_width=None):
        """
        Draw table to the report

        Args:
            notes(str): Explain the block
            table_header (list): list of str
            table_data (list): list of str
            col_width: Not use in HTML - default None
        """
        # -- Draw Content --
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        self.html.article[-1].items.append(
            self.html.add_table(header=table_header, data=table_data))

    def draw_basic_images_with_grid_spec(self, notes: str, *,
                                        image_list: list, grid_spec=None):
        """
        Draw image blocks with formatted grid specification

        Args
            notes(str): Explain the block
            image_list (list): the list of image_paths
            grid_spec (dict): Not use in HTML - default None

        """
        # -- Draw Content --
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        for figure_path in image_list:
            self.html.article[-1].items.append(
                self.html.add_image(src=figure_path))


    ################################################################################
    ###  Summary Section
    ################################################################################

    def draw_training_time(self, notes: str, *, timing: List[Tuple[str, int]]):
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
            self.html.add_overview_table(data=timing))

    def draw_data_set_summary(self, notes: str, *,
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
            self.html.add_overview_table(data=data_summary))

    def draw_evaluation_result_summary(self, notes: str, *,
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
                        warnings.warn(message='No defined keys (`class`,`average`) found in metric value: %s' % (
                                metric_value.keys()))
                        continue

                elif type(metric_value) == float:
                    key = "%s" % metric_name.capitalize()
                    value = "%.4f" % metric_value
                elif type(metric_value) == str:
                    key = "%s" % metric_name.capitalize()
                    value = metric_value
                else:
                    warnings.warn(message='Unsupported metric value type for metric (%s): %s' % (
                        metric_name, type(metric_value)))
                    continue
                if key not in items:
                    items[key] = list()
                items.get(key).append(value)

        self.html.article[-1].items.append(
            self.html.add_overview_table_with_dict(data=items))

    def draw_model_info_summary(self, notes: str, *, model_info: list):
        """
        Draw information of model info to the result

        Args:
            notes (str, Optional): explain the block
            model_info (:obj:`list` of :obj:
              `tuple`, Optional): list of tuple (model info attribute, model info value).
               Default information include `use case name`, `version`, `use case team`.
        """
        # -- Draw Content --
        self.html.article[-1].items.append(self.html.add_header(text=notes,
                                                                heading='h3'))
        self.html.article[-1].items.append(
            self.html.add_overview_table(data=model_info))

    ################################################################################
    ###  Data Section
    ################################################################################

    def draw_data_missing_value(self, notes: str, *, missing_count: dict,
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

    def draw_data_set_distribution(self, notes: str, *,
                                   data_set_distribution: Tuple[str, Dict],
                                   max_class_shown=20):
        """
        Draw information of distribution on data set

        Args:
            notes(str): Explain the block
            data_set_distribution (tuple: (str,dict)):
                - tuple[0] str: label/split name
                - tuple[1] dict: key: class name, value: class count
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

    def draw_data_attributes(self, notes: str, *, data_attribute: Dict):
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

    def draw_categorical_field_distribution(self, notes: str, *,
                                            field_name: str,
                                            field_distribution: Dict[str, CategoricalStats],
                                            max_values_display=20,
                                            colors=None):
        """
        Draw information of field value distribution for categorical type to
        the report.

        Args:
            notes(str): Explain the block
            field_name (str): data field name
            field_distribution (:dict of :CategoricalStats):
                -key: label_name
                -value: frequency distribution under the `label_name`(dict)
                    - key: field value
                    - value: CategoricalStats object
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
        for idx, (label_name, cat_stats) in enumerate(
                field_distribution.items()):
            frequency_distribution = cat_stats.frequency_count
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

    def draw_numeric_field_distribution(self, notes: str, *,
                                        field_name: str,
                                        field_distribution: Dict[str, NumericalStats],
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
                 -value: numeric statistics object

             force_no_log (bool): whether to change y-scale to logrithmic
                                              scale for a more balanced view
             x_limit (list:): whether x-axis only display the required percentile range.
                             If True, field_distribution should have a
                             key "x_limit" and value of [x_min, x_max].
             colors (list): the list of color code for rendering different class
        """
        from xai.graphs import graph_generator
        if colors is None:
            colors = ["#3498db", "#2ecc71", "#e74c3c"]
        # -- Draw Content --
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        for idx, (label_name, num_stats) in enumerate(
                field_distribution.items()):
            title = 'Distribution for %s' % label_name
            self.html.article[-1].items.append(
                self.html.add_header(text=title, heading='h5'))
            figure_path = '%s/%s_%s_field_distribution.png' % (
                self.figure_path, field_name, label_name)
            figure_path = graph_generator.KdeDistribution(
                figure_path=figure_path,
                data=num_stats,
                title=title,
                x_label=field_name,
                y_label="").draw(
                color=colors[idx % len(colors)],
                force_no_log=force_no_log,
                x_limit=x_limit)
            table_header = ['Statistical Field', 'Value']
            table_values = list()
            table_values.append(['Total valid count', "%d" % int(num_stats.total_count)])
            table_values.append(['Min', "%d" % int(num_stats.min)])
            table_values.append(['Max', "%d" % int(num_stats.max)])
            table_values.append(['Mean', "%d" % int(num_stats.mean)])
            table_values.append(['Median', "%d" % int(num_stats.median)])
            table_values.append(['Standard deviation', "%d" % int(num_stats.sd)])
            table_values.append(['NAN count', "%d" % int(num_stats.nan_count)])

            self.html.article[-1].items.append(self.html.add_table_image_group(
                header=table_header, data=table_values,
                src=figure_path, alt=title))

    def draw_text_field_distribution(self, notes: str, *,
                                     field_name: str,
                                     field_distribution: Dict[str, TextStats]):
        """
        Draw information of field value distribution for text type to the
        report.

        Args:
            notes(str): Explain the block
            field_name (str): data field name
            field_distribution (:dict of :dict):
                -key: label_name
                -value: TextStats
        """
        from xai.graphs import graph_generator
        # -- Draw Content --
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        for idx, (label_name, text_stats) in enumerate(
                field_distribution.items()):
            tfidf = text_stats.tfidf
            pattern_stats = text_stats.pattern_stats

            title = 'Distribution for %s' % label_name
            self.html.article[-1].items.append(
                self.html.add_header(text=title, heading='h5'))
            figure_path = '%s/%s_%s_field_distribution.png' % (
                self.figure_path, field_name, label_name)
            figure_path = graph_generator.WordCloudGraph(
                figure_path=figure_path,
                data=tfidf,
                title=title).draw()
            table_header = ['Placeholder', 'Percentage(%)']
            table_values = []
            for w, v in pattern_stats.items():
                table_values.append([w, '%.2f%%' % (v * 100)])

            if len(table_values) == 0:
                self.html.article[-1].items.append(self.html.add_image(
                    src=figure_path, alt=title))
            else:
                self.html.article[-1].items.append(self.html.add_table_image_group(
                    header=table_header, data=table_values,
                    src=figure_path, alt=title))

    def draw_datetime_field_distribution(self, notes: str, *,
                                         field_name: str,
                                         field_distribution: Dict[str, DatetimeStats]):
        """
        Draw information of field value distribution for datetime type to the
        report.

        Args:
            notes(str): Explain the block
            field_name (str): data field name
            field_distribution (:dict of :dict):
                -key: label_name
                -value (:dict of :DatetimeStats): only support resolution_list size of 2
                    - 1st level key: year_X(int)
                    - 1st level value:
                        - 2nd level key: month_X(int)
                        - 2nd level value: count of sample in month_X of year_X
        """
        from xai.graphs import graph_generator
        # -- Draw Content --
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        for idx, (label_name, datetime_stats) in enumerate(
                field_distribution.items()):
            title = 'Datetime distribution for %s (for %s samples) ' % (
                field_name,
                label_name)
            self.html.article[-1].items.append(
                self.html.add_header(text=title, heading='h5'))
            figure_path = '%s/%s_%s_field_distribution.png' % (
                self.figure_path, field_name, label_name)
            figure_path = graph_generator.DatePlot(figure_path=figure_path,
                                                   data=datetime_stats.frequency_count,
                                                   title=title,
                                                   x_label="",
                                                   y_label="").draw()
            self.html.article[-1].items.append(
                self.html.add_image(src=figure_path, alt=title))

    ################################################################################
    ###  Feature Section
    ################################################################################

    def draw_feature_importance(self, notes: str, *,
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
        from xai.graphs import graph_generator
        # -- Draw Content --
        if not (notes is None):
            modified_notes = notes
        elif maximum_number_feature < len(importance_ranking):
            modified_notes = (
                    "The figure below shows the top %s important features for the trained model."
                    % maximum_number_feature)
        else:
            modified_notes = "The figure below shows importance ranking for all features from the trained model."
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=modified_notes))

        image_path = '%s/feature_importance.png' % self.figure_path
        image_path = graph_generator.FeatureImportance(figure_path=image_path,
                                                       data=importance_ranking,
                                                       title='feature_importance').draw(
            limit_length=maximum_number_feature)

        self.html.article[-1].items.append(
            self.html.add_image(src=image_path, alt='feature_importance'))

        self.html.article[-1].items.append(self.html.add_paragraph(
            text="The features which have an importance score larger "
                 "than %s are listed in the below table." % importance_threshold))

        header = ['Feature', 'Importance']
        data = []
        for feature_name, importance in importance_ranking:
            if float(importance) < importance_threshold:
                break
            data.append([feature_name, round(importance, 10)])
        self.html.article[-1].items.append(
            self.html.add_table(header=header, data=data))

    def draw_feature_shap_values(self, notes: str, *, mode: str,
                                 feature_shap_values: List[Tuple[str, List]],
                                 class_id: int,
                                 train_data: numpy.ndarray = None):
        """
        Add information of feature shap values to the report.

        Args:
            notes(str): Explain the block
            mode (str): Model Model - classification/regression model
            feature_shap_values(:list of :tuple): a list of 2-item tuple,
                                        item[0]: feature name, item[1] shap values on each training samples
            class_id(int): the class id for visualization.
            train_data(numpy.dnarray): Optional, training data, row is for samples, column is for features.
        """
        from xai.graphs import graph_generator
        image_path = '%s/feature_shap_values_%s.png' % (self.figure_path, class_id)
        image_path = graph_generator.FeatureShapValues(figure_path=image_path,
                                                       shap_values=feature_shap_values,
                                                       class_id=class_id,
                                                       train_data=train_data,
                                                       title=None).draw()

        # -- Draw Content --
        if not (notes is None):
            self.html.article[-1].items.append(
                self.html.add_paragraph(text=notes))

        if mode == MODE.CLASSIFICATION:
            self.html.article[-1].items.append(self.html.add_paragraph(
                text="The figure below shows an overview of which features are most important class %s,"
                     " by plotting SHAP values of every feature for every sample." % class_id))
        else:
            self.html.article[-1].items.append(self.html.add_paragraph(
                text="The figure below shows an overview of which features are most important in regression model,"
                     " by plotting SHAP values of every feature for every sample."))
        self.html.article[-1].items.append(
            self.html.add_image(src=image_path, alt='feature_shap'))


    ################################################################################
    ###  Training Section
    ################################################################################

    def draw_hyperparameter_tuning(self, notes: str, *,
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
        from xai.graphs import graph_generator
        # -- Draw Content --
        if not (notes is None):
            self.html.article[-1].items.append(
                self.html.add_paragraph(text=notes))
        # tuning search space
        self.html.article[-1].items.append(self.html.add_paragraph(
            text='Hyperparameter Tuning Search Space', style='BI'))
        self.html.article[-1].items.append(
            self.html.add_table_with_dict(data=search_space))
        # tuning history result
        self.html.article[-1].items.append(self.html.add_paragraph(
            text='Hyperparameter Tuning History Result', style='BI'))
        self.html.article[-1].items.append(
            self.html.add_paragraph(
                text="The metric results from hyperparameter tuning are "
                     "shown in the figure."))
        benchmark_dict = dict()
        benchmark_dict["Benchmark metric"] = benchmark_metric
        benchmark_dict["Benchmark value"] = benchmark_threshold
        self.html.article[-1].items.append(
            self.html.add_table_with_dict(data=benchmark_dict))
        image_path = "%s/hyperopt_history.png" % self.figure_path
        image_path = graph_generator.EvaluationLinePlot(figure_path=image_path,
                                                        data=history,
                                                        title='hyper_history',
                                                        x_label='Iterations',
                                                        y_label='Metrics Score').draw(
            benchmark_metric=benchmark_metric,
            benchmark_value=benchmark_threshold)
        self.html.article[-1].items.append(
            self.html.add_image(src=image_path, alt='hyper_history'))

        # best result for hyperopt
        self.html.article[-1].items.append(self.html.add_paragraph(
            text='Best Result from Hyperparameter Tuning', style='BI'))
        self.html.article[-1].items.append(self.html.add_paragraph(
            text='The best iteration is %s' % best_idx))
        self.html.article[-1].items.append(self.html.add_paragraph(
            text='Parameters:', style='B'))
        self.html.article[-1].items.append(
            self.html.add_table_with_dict(data=history[best_idx]['params']))

        # validation result
        self.html.article[-1].items.append(self.html.add_paragraph(
            text='Validation Results:', style='B'))
        final_metric_value = 0
        validation_result = dict()
        for param_name, param_value in history[best_idx]['val_scores'].items():
            if param_name == benchmark_metric:
                validation_result[param_name.capitalize()] = \
                    '%s (benchmarking metric)' % param_value
                final_metric_value = param_value
            else:
                validation_result[param_name.capitalize()] = param_value
        self.html.article[-1].items.append(
            self.html.add_table_with_dict(data=validation_result))

        # Tuning final conclusion
        self.html.article[-1].items.append(self.html.add_paragraph(
            text='Hyperparameter Tuning Final Conclusion', style='BI'))
        if non_hyperopt_score is None:
            self.html.article[-1].items.append(self.html.add_paragraph(
                text='There is no benchmarking conducted in this training. '
                     'We will accept the best result from hyperparameter '
                     'tuning as final parameter set.'))
        else:
            if final_metric_value > non_hyperopt_score:
                if final_metric_value > benchmark_threshold:
                    text = 'and it is better than acceptance benchmark ' \
                           'scoring (%.4f). We accept it as the final ' \
                           'parameter setting for the trained model.' % \
                           benchmark_threshold
                else:
                    text = 'but it fails to meet the acceptance benchmark ' \
                           'scoring (%.4f). ' \
                           'We still accept it as the final parameter setting for the trained model, ' \
                           'but will continue to improve it.' % benchmark_threshold
                self.html.article[-1].items.append(self.html.add_paragraph(
                    text='Hyperparameter tuning best result (%.4f) is better than benchmark score (%.4f), %s' % (
                        final_metric_value, non_hyperopt_score, text)))
            else:
                if final_metric_value > benchmark_threshold:
                    text = 'and benchmarking result is better than ' \
                           'acceptance benchmark scoring (%.4f). We accept ' \
                           'default parameters the final solution for the trained model.' % benchmark_threshold
                else:
                    text = 'but it fails to meet the acceptance benchmark ' \
                           'scoring (%.4f). We still accept default ' \
                           'parameters as the final solution ' \
                           'for the trained model, but will continue to improve it.' % benchmark_threshold
                self.html.article[-1].items.append(self.html.add_paragraph(
                    text='Hyperparameter tuning best result (%.4f) is worse '
                         'than benchmark score (%.4f), %s' % (
                             final_metric_value, non_hyperopt_score, text)))

    def draw_learning_curve(self, notes: str, *,
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
        from xai.graphs import graph_generator
        # -- Draw Content --
        if not (notes is None):
            self.html.article[-1].items.append(
                self.html.add_paragraph(text=notes))
        if training_params is not None:
            self.html.article[-1].items.append(self.html.add_paragraph(
                text='Training Parameters', style='BI'))
            self.html.article[-1].items.append(
                self.html.add_table_with_dict(data=training_params))

        self.html.article[-1].items.append(self.html.add_paragraph(
            text='Learning Curve', style='BI'))
        self.html.article[-1].items.append(self.html.add_paragraph(
            text='The metric results from several training epochs are shown '
                 'in the figure.'))
        benchmark_dict = dict()
        benchmark_dict["Benchmark metric"] = benchmark_metric
        benchmark_dict["Benchmark value"] = benchmark_threshold
        self.html.article[-1].items.append(
            self.html.add_table_with_dict(data=benchmark_dict))

        image_path = "%s/deep_learning_curve.png" % self.figure_path
        image_path = graph_generator.EvaluationLinePlot(figure_path=image_path,
                                                        data=history,
                                                        title='training_history',
                                                        x_label='Steps',
                                                        y_label='Metrics Score').draw(
            benchmark_metric=benchmark_metric,
            benchmark_value=benchmark_threshold)
        self.html.article[-1].items.append(
            self.html.add_image(src=image_path, alt='hyper_history'))

        self.html.article[-1].items.append(self.html.add_paragraph(
            text='Best Epoch from Training', style='BI'))
        self.html.article[-1].items.append(self.html.add_paragraph(
            text='The best iteration is %s' % str(best_idx)))

        self.html.article[-1].items.append(self.html.add_paragraph(
            text='Validation Results:', style='BI'))
        if best_idx not in history:
            best_idx = str(best_idx)
        validation_result = dict()
        for param_name, param_value in history[best_idx]['val_scores'].items():
            if param_name == benchmark_metric:
                validation_result[param_name.capitalize()] = \
                    '%s (benchmarking metric)' % param_value
            else:
                validation_result[param_name.capitalize()] = param_value
        self.html.article[-1].items.append(
            self.html.add_table_with_dict(data=validation_result))

    ################################################################################
    ###  Interpreter Section
    ################################################################################
    def draw_model_interpreter(self, notes: str, *,
                               mode: str, class_stats: dict,
                               total_count: int, stats_type: str,
                               k:int, top: int=15):
        """
        Add model interpreter for classification

        Args:
            mode (str): Model Model - classification/regression model
            class_stats (dict): A dictionary maps the label to its aggregated statistics
            total_count (int): The total number of explanations to generate the statistics
            stats_type (str): The defined stats_type for statistical analysis
            k (int): The k value of the defined stats_type
            top (int): the number of top explanation to display
            notes(str): text to explain the block
        """
        from xai.graphs import graph_generator

        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        self.html.article[-1].items.append(
            self.html.add_paragraph(
                text="Statistical type: %s with K value: %d" % (stats_type, k)))
        for _class, _explanation_ranking in class_stats.items():
            if mode == MODE.CLASSIFICATION:
                title = 'Interpretation for Class %s' % _class
            else:
                title = 'Interpretation for Regression'
            self.html.article[-1].items.append(
                self.html.add_paragraph(text=title, style='BI'))
            image_path = '%s/model_interpreter_%s.png' % (self.figure_path, _class)
            importance_ranking = [(key, value) for key, value in _explanation_ranking.items()][: top]
            image_path = graph_generator.FeatureImportance(
                figure_path=image_path,
                data=importance_ranking,
                title=title).draw()
            self.html.article[-1].items.append(
                self.html.add_image(src=image_path, alt=title))

    def draw_error_analysis(self, notes: str, *, mode: str, error_stats: dict,
                            stats_type: str, k: int, top: int=15):
        """
        Add error analysis for classification

        Args:
            mode (str): Model Model - classification/regression model
            error_stats (dict): A dictionary maps the label to its aggregated statistics
            stats_type (str): The defined stats_type for statistical analysis
            k (int): The k value of the defined stats_type
            top (int): the number of top explanation to display
            notes(str): text to explain the block
        """
        from xai.graphs import graph_generator

        # -- Draw Content --
        self.html.article[-1].items.append(
            self.html.add_paragraph(text=notes))
        self.html.article[-1].items.append(
            self.html.add_paragraph(
                text="Statistical type: %s with K value: %d" % (stats_type, k)))
        for (gt_class, predict_class), (
        _explanation_dict, num_sample) in error_stats.items():
            if mode == MODE.CLASSIFICATION:
                title = '%s sample from class [%s] is wrongly classified as class[%s]' % (
                num_sample, gt_class, predict_class)
                self.html.article[-1].items.append(
                    self.html.add_paragraph(text=title, style='BI'))
                reason = ' - Top reasons that they are predicted as class[%s]' % predict_class
                self.html.article[-1].items.append(
                    self.html.add_paragraph(text=reason, style='BI'))
            else:
                title = 'sample for regression model'
                self.html.article[-1].items.append(
                    self.html.add_paragraph(text=title, style='BI'))
                reason = ' - Top reasons in regression prediction'
                self.html.article[-1].items.append(
                    self.html.add_paragraph(text=reason, style='BI'))
            image_path = '%s/feature_importance_%s.png' % (
            self.figure_path, predict_class)
            importance_ranking = [(key, value) for key, value in
                                  _explanation_dict[predict_class].items()][
                                 :top]
            image_path = graph_generator.FeatureImportance(
                figure_path=image_path,
                data=importance_ranking,
                title=title).draw()
            self.html.article[-1].items.append(
                self.html.add_image(src=image_path, alt=title))

    ################################################################################
    ###  Evaluation Section
    ################################################################################

    def draw_multi_class_evaluation_metric_results(self, notes: str, *,
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
        from xai.model.evaluation.multi_classification_result import \
            MultiClassificationResult
        # -- Draw Content --
        if not (notes is None):
            self.html.article[-1].items.append(
                self.html.add_paragraph(text=notes))
        name = ''
        header = list()
        data = list()
        for eval_name, eval_metric_dict in metric_tuple:
            cr = MultiClassificationResult()
            cr.load_results_from_meta(eval_metric_dict)
            name, header, data, layout = cr.convert_metrics_to_table()

        self.html.article[-1].items.append(
            self.html.add_paragraph(text=name, style='BI'))
        self.html.article[-1].items.append(
            self.html.add_table(header=header, data=data))

    def draw_binary_class_evaluation_metric_results(self, notes: str, *,
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
        from collections import defaultdict
        from xai.model.evaluation.binary_classification_result import \
            BinaryClassificationResult
        # -- Draw Content --
        if not (notes is None):
            self.html.article[-1].items.append(
                self.html.add_paragraph(text=notes))

        combined_table_dict = defaultdict(list)
        combined_table_header = ["Split/Round"]
        name = ''
        for eval_name, eval_metric_dict in metric_tuple:
            combined_table_header.append(eval_name)
            cr = BinaryClassificationResult()
            cr.load_results_from_meta(eval_metric_dict)
            name, header, data, table_layout = cr.convert_metrics_to_table()
            if aggregated:
                table_data_dict = {row[0]: row[1] for row in data}
                for metric_name, metric_value in table_data_dict.items():
                    combined_table_dict[metric_name].append(metric_value)
            else:
                self.html.article[-1].items.append(self.html.add_paragraph(
                    text='For split/round %s' % eval_name, style='B'))
                self.html.article[-1].items.append(
                    self.html.add_table(header=header, data=data))

        if aggregated:
            combined_table_values = []
            for metric_name, metric_value_list in combined_table_dict.items():
                combined_table_values.append([metric_name] + metric_value_list)

            self.html.article[-1].items.append(
                self.html.add_paragraph(text=name, style='BI'))
            self.html.article[-1].items.append(
                self.html.add_table(header=combined_table_header,
                                    data=combined_table_values))

    def draw_confusion_matrix_results(self, notes: str, *,
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
        from xai.graphs import graph_generator
        # -- Draw Content --
        if not (notes is None):
            self.html.article[-1].items.append(
                self.html.add_paragraph(text=notes))

        images = dict()
        for idx, (eval_name, confusion_matrix_mat) in enumerate(
                confusion_matrix_tuple):
            figure_path = '%s/%s_%s_cm.png' % (
                self.figure_path, idx, eval_name)
            image_path = graph_generator.HeatMap(figure_path=figure_path,
                                                 data=confusion_matrix_mat[
                                                     'values'],
                                                 title=eval_name,
                                                 x_label='Predict',
                                                 y_label='True').draw(
                x_tick=confusion_matrix_mat['labels'],
                y_tick=confusion_matrix_mat['labels'],
                color_bar=True)
            images[eval_name] = image_path
        self.html.article[-1].items.append(
            self.html.add_grid_image(srcs=images))

    def draw_multi_class_confidence_distribution(self, notes: str, *,
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
        import operator
        from xai.graphs import graph_generator
        # -- Draw Content --
        if not (notes is None):
            self.html.article[-1].items.append(
                self.html.add_paragraph(text=notes))

        top_classes = list()
        for eval_name, eval_vis_result in visual_result_tuple:
            predicted_class_count = dict()
            label = ''
            for label in eval_vis_result.keys():
                data = eval_vis_result[label]
                num_sample = len(data['gt'])
                predicted_class_count[label] = num_sample

                sorted_class_size = sorted(predicted_class_count.items(),
                                           key=operator.itemgetter(1))[::-1]
                top_classes = [a for (a, _) in sorted_class_size]

            images = dict()
            for class_label in top_classes:
                data = eval_vis_result[class_label]
                num_sample = len(data['gt'])
                if num_sample > 0:
                    image_path = '%s/%s_%s_conf_dist.png' % (
                        self.figure_path, label, class_label)
                    sw_image_path = graph_generator.ResultProbabilityForMultiClass(
                        image_path, data,
                        'Predicted as %s' % label).draw()
                    images[class_label] = sw_image_path
                if len(images) >= max_num_classes:
                    break
            self.html.article[-1].items.append(
                self.html.add_grid_image(srcs=images))

    def draw_binary_class_confidence_distribution(self, notes: str, *,
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
        from xai.graphs import graph_generator
        # -- Draw Content --
        if not (notes is None):
            self.html.article[-1].items.append(
                self.html.add_paragraph(text=notes))

        images = dict()
        for eval_name, eval_vis_result in visual_result_tuple:
            image_path = "%s/%s_prob_dist.png" % (self.figure_path, eval_name)
            image_path = graph_generator.ResultProbability(
                figure_path=image_path,
                data=eval_vis_result,
                title='Probability Distribution').draw()
            images[eval_name] = image_path
        self.html.article[-1].items.append(
            self.html.add_grid_image(srcs=images))

    def draw_binary_class_reliability_diagram(self, notes: str, *,
                                              visual_result_tuple: tuple):
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
        from xai.graphs import graph_generator
        # -- Draw Content --
        if not (notes is None):
            self.html.article[-1].items.append(
                self.html.add_paragraph(text=notes))

        images = dict()
        for eval_name, eval_vis_result in visual_result_tuple:
            image_path = "%s/%s_reliability_diagram.png" % (
                self.figure_path, eval_name)
            image_path = graph_generator.ReliabilityDiagram(
                figure_path=image_path,
                data=eval_vis_result,
                title='Reliability Diagram').draw()
            images[eval_name] = image_path

        self.html.article[-1].items.append(
            self.html.add_grid_image(srcs=images))