from xai.formatter.pdf_report.base_report import ReportWriter

import tempfile
import datetime
import shutil
import logging
import os
import inspect
import numpy as np
from collections import defaultdict
from xai.graphs import format_contants as gg_constants
from xai.graphs import graph_generator as gg
from xai.evaluation.multi_classification_result import MultiClassificationResult
from xai.evaluation.binary_classification_result import BinaryClassificationResult
from typing import Tuple, Dict, List

LOGGER = logging.getLogger(__name__)


class TrainingReport(ReportWriter):
    """Training report class for a standard report covers both data and training/evaluation.

        Attributes:

            figure_path (str):
                the temperary folder path for generated images.

        """

    def __init__(self, usecase_name: str, version: str, usecase_team: str):
        """

        Args:
            usecase_name (str): the name of use case, appeared in the title of the report
            version (str): the version of service, appeared in the title of the report
            usecase_team (str): the name of use case develop team, appeared as the author of the report
        """

        super(TrainingReport, self).__init__(usecase_name=usecase_name,
                                             version=version,
                                             author=usecase_team,
                                             report_name='Training Report')
        LOGGER.info('Training report initialized.')

        # set up temporary image folder
        self.figure_path = tempfile.TemporaryDirectory().name

        os.mkdir(self.figure_path)

        LOGGER.info('Temporary figure path created: %s' % self.figure_path)

        # initialize content_table
        self.__content_table = []
        self.__content_buffer = []

        self.__current_section_level = 0
        self.__current_subsection_level = 0
        self.__current_subsubsection_level = 0

    def output_report(self, output_path: str, report_name='training_report'):
        """
        generate pdf report and output to defined path, clean up the figure path
        Args:
            output_path (str): output path for generated report
            report_name (str, Optional): filename of report, default is ``training_report``

        """

        for func_sig in self.__content_buffer:
            if len(func_sig) == 2:
                func, kwargs = func_sig
                func(**kwargs)
            if len(func_sig) == 3:
                func, kwargs, args = func_sig
                func(*args, **kwargs)

        report_path = '%s/%s.pdf' % (output_path, report_name)
        self.output(report_path)
        LOGGER.info('Report generated: %s' % report_path)
        # clean up temp folder
        if os.path.exists(self.figure_path):
            shutil.rmtree(self.figure_path)

    def add_content_to_report_buffer(self, title='', section_level=None, content=None, add_to_content_table=False):
        """
        add a section with title and content
        Args:
            title (str): section title
            section_level (int, Optional): level of section,
                Level 0: section (1 xxx)
                Level 1: subsection (1.1 xxx)
                Level 2: subsubsection (1.1.1 xxx)
            content (tuple): report component that want to render in terms of tuple (func, params)
            add_to_content_table (bool): whether to add to content table.
                If True, a link will be attached to the section and corresponding title will be added into content table.
                ignored if section_level is not set to predefined level,
        """
        if section_level not in [0, 1, 2]:
            add_to_content_table = False

        if add_to_content_table:
            link = self.add_link()
            if section_level == 0:
                self.__current_section_level += 1
                self.__current_subsection_level = 0
                self.__current_subsubsection_level = 0

                content_table_title = '<B>%s   %s</B>' % (self.__current_section_level,
                                                          title)
                self.__content_table.append((content_table_title, link))
                self.__content_buffer.append((self.add_section, {'title': title, 'link': link}))

            elif section_level == 1:
                self.__current_subsection_level += 1
                self.__current_subsubsection_level = 0
                content_table_title = '........ %s.%s   %s' % (self.__current_section_level,
                                                               self.__current_subsection_level,
                                                               title)
                self.__content_table.append((content_table_title, link))
                self.__content_buffer.append((self.add_subsection, {'title': title, 'link': link}))


            elif section_level == 2:
                self.__current_subsubsection_level += 1
                content_table_title = '.............. <I>%s.%s.%s   %s</I>' % (self.__current_section_level,
                                                                               self.__current_subsection_level,
                                                                               self.__current_subsubsection_level,
                                                                               title)
                self.__content_table.append((content_table_title, link))
                self.__content_buffer.append((self.add_subsubsection, {'title': title, 'link': link}))
        else:
            if title != '':
                self.__content_buffer.append((self.add_new_line, {'line': title, 'style': 'BI'}))
        if content is not None:
            self.__content_buffer.append(content)

    def __component_content_table(self):
        def func():
            """
            add content table based on current __content_table title and link
            """
            self.add_ribbon('Content Table')
            for table_content_title, link in self.__content_table:
                self.add_new_line(line=table_content_title, link=link)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_paragraph_in_html(self, text: str):
        def func(text: str):
            """
            add a paragraph into the report
            Args:
                text(str): html text to render in the report
            """
            self.add_new_line(text, style='')
            self.ln()

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, values[
                varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    """ Data section
    """

    def component_data_missing_value(self, missing_count: dict, total_count={}, ratio=False, notes=None):
        def func(missing_count: dict, total_count={}, ratio=False, notes=None):
            """
            add information of missing value for data fields to the report
            Args:
                missing_count (dict):
                    - key: data field name
                    - value: the count or the percentage of missing value in the field
                total_value (dict, Optinal):
                    - key: data field name
                    - value: the count of missing value in the field
                ratio (bool): True if `missing_value` is the percentage
                notes (str, Optional):
                    explain the block

            """

            if notes is not None:
                self.add_new_line(notes)
            else:
                self.add_new_line("This section shows the percentage of sample data with missing values.")

            data_dict = defaultdict(dict)
            field_set = set(total_count.keys())
            field_set.update(set(missing_count.keys()))
            for feature_name in field_set:
                if feature_name not in total_count:
                    data_dict[feature_name]['total_count'] = '-'
                else:
                    data_dict[feature_name]['total_count'] = total_count[feature_name]

                if feature_name not in missing_count:
                    data_dict[feature_name]['missing_value_count'] = 0
                    data_dict[feature_name]['percentage'] = 0
                else:
                    if ratio:
                        data_dict[feature_name]['percentage'] = missing_count[feature_name]
                        data_dict[feature_name]['missing_value_count'] = '-'
                    else:
                        data_dict[feature_name]['missing_value_count'] = missing_count[feature_name]
                        if data_dict[feature_name]['total_count'] != '-':
                            data_dict[feature_name]['percentage'] = data_dict[feature_name]['missing_value_count'] / \
                                                                    data_dict[feature_name]['total_count']
            if len(total_count) > 0:
                table_header = ['Feature', 'Missing Value Count', 'Percentage']
                table_data = []
                for field_name, field_data in data_dict.items():
                    table_data.append(
                        [field_name, "%s / %s" % (field_data['missing_value_count'], field_data['total_count']),
                         "%.2f%%" % field_data['percentage']])
                col_width = [70, 50, 50]
            else:
                if ratio:
                    table_header = ['Feature', 'Missing Value Percentage']
                    table_data = []
                    for field_name, field_data in data_dict.items():
                        table_data.append([field_name, field_data['percentage']])
                else:
                    table_header = ['Feature', 'Missing Value Count']
                    table_data = []
                    for field_name, field_data in data_dict.items():
                        table_data.append([field_name, field_data['missing_value_count']])
                col_width = [80, 70]

            if len(table_data) > 0:
                self.add_table(table_header, table_data, col_width=col_width)
                self.add_new_line()
            LOGGER.info('Add info: Missing Value Info')

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_dataset_distribution(self, *dataset_distribution: Tuple[str, dict], max_class_shown=20, notes=None):
        def func(*dataset_distribution: Tuple[str, dict], max_class_shown=20, notes=None):
            """
            add information of distribution on data set to the report
            Args:
                dataset_distribution (tuple: (str,dict)):
                    - tuple[0] str: label/split name
                    - tuple[1] dict: key - class_name/split_name, value - class_count/split_count
                max_class_shown (int, Optional): maximum number of classes shown in the figure, default is 20
                notes (str, Optional):
                    explain the block
            """

            if notes is not None:
                self.add_new_line(notes)
            else:
                self.add_new_line("This section shows the distribution of dataset on the label/split.")

            table_header = ['', 'Count', 'Distribution']
            table_data = []
            for dataset_name, dataset_dist in dataset_distribution:
                table_data.append(
                    [dataset_name, sum(list(dataset_dist.values())), 'See below graphs'])

            self.ln()
            self.add_table(table_header, table_data, [80, 40, 60])

            for dataset_name, dataset_dist in dataset_distribution:
                self.add_new_line('Distribution for <B>%s</B>' % dataset_name)
                if len(dataset_dist) > max_class_shown:
                    self.add_new_line('(Only %s shown amoung %s classes)' % (max_class_shown, len(dataset_dist)))
                image_path = gg.BarPlot(file_path='%s/%s_data_distribution.png' % (self.figure_path, dataset_name),
                                        data=dataset_dist,
                                        title="Data Distribution for %s" % (dataset_name),
                                        x_label='Number of samples', y_label='Category').draw(
                    caption=dataset_name,
                    ratio=True,
                    limit_length=max_class_shown)
                self.add_large_image(image_path)

            LOGGER.info('Add info: Dataset Distribution Info')

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_data_attributes(self, data_attribute: Dict, notes=None):
        def func(data_attribute, notes=None):
            """
            add information of data attribute for data fields to the report
            Args:
                data_attribute (:dict of :dict):
                    -key: data field name
                    -value: attributes (dict)
                        - key: attribute name
                        - value: attribute value
                notes (str, Optional):
                    explain the block
            """

            if notes is not None:
                self.add_new_line(notes)
            else:
                self.add_new_line("This section shows the attributes of fields in the dataset")

            attribute_list = list(
                set().union(*[set(attribute_dict.keys()) for attribute_dict in data_attribute.values()]))
            table_header = ['Field Name'] + [attribute.capitalize() for attribute in attribute_list]

            table_data = []
            for field_name, field_attributes in data_attribute.items():
                row = [field_name]
                for attribute_name in attribute_list:
                    if attribute_name in field_attributes.keys():
                        row.append(field_attributes[attribute_name])
                    else:
                        row.append('-')
                table_data.append(row)

            self.ln()
            self.add_table(table_header, table_data)
            self.add_new_line()
            LOGGER.info('Add info: Data Field Attribute Info')

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_categorical_field_distribution(self, field_name: str, field_distribution: dict, max_values_display=20,
                                                 colors=None, notes=None):
        def func(field_name: str, field_distribution: dict, max_values_display=20, colors=None, notes=None):
            """
            add information of field value distribution for categorical type to the report.
            Details see analyzers inside `xai.data_explorer.categorical_analyzer`
            Args:
                field_name (str): data field name
                field_distribution (:dict of :dict):
                    -key: label_name
                    -value: frequency distribution under the `label_name`(dict)
                        - key: field value
                        - value: field value frequency
                max_values_display (int): maximum number of values displayed
                colors (list): the list of color code for rendering different class
                notes (str, Optional):
                    explain the block
            """
            if notes is not None:
                self.add_new_line(notes)
            if colors is None:
                colors = ["Blues_d", "Reds_d", "Greens_d", "Purples_d", "Oranges_d"]
            self.start_itemize(' - ')
            for idx, (label_name, frequency_distribution) in enumerate(field_distribution.items()):
                if len(frequency_distribution) / sum(frequency_distribution.values()) > 0.5:
                    LOGGER.warning('%s is probably a unique feature, ignore in visualization.' % field_name)
                    self.start_itemize('-')
                    self.add_new_line('Warning: %s unique values found in %s samples.' % (
                        len(frequency_distribution), sum(frequency_distribution.values())))
                    self.end_itemize()
                    break

                if len(field_distribution) > max_values_display:
                    self.add_new_line('%s of %s are displayed)' % (max_values_display, len(field_distribution)))

                figure_path = '%s/%s_%s_field_distribution.png' % (self.figure_path, field_name, label_name)
                image_path = gg.BarPlot(file_path=figure_path,
                                        data=frequency_distribution,
                                        title="",
                                        x_label="", y_label=field_name).draw(limit_length=max_values_display,
                                                                             color_palette=colors[idx % len(colors)])
                self.add_large_image(image_path=image_path, caption='For %s samples' % label_name, style='I')
            self.end_itemize()
            LOGGER.info('Add info: Categorical Data Field [%s] Info' % field_name)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, \
                   values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_numeric_field_distribution(self, field_name: str, field_distribution: dict, force_no_log=False,
                                             x_limit=False, colors=None, notes=None):
        def func(field_name, field_distribution, force_no_log=False, x_limit=False, colors=None, notes=None):
            """
            add information of field value distribution for numerical type to the report.
            Details see analyzers inside `xai.data_explorer.numerical_analyzer`
            Args:
                field_name (str): data field name
                field_distribution (:dict of :dict):
                    -key: label_name
                    -value: numeric statistics
                        - key: statistics name
                        - value: statistics value
                    each field_distribution should must have 2 following predefined keys:
                    - histogram (:list of :list): a list of bar specification (x, y, width, height)
                    - kde (:list of :list, Optional): a list of points which draw`kernel density estimation` curve.

                force_no_log (bool): whether to change y-scale to logrithmic scale for a more balanced view
                x_limit (list:): whether x-axis only display the required percentile range.
                                If True, field_distribution should have a key "x_limit" and value of [x_min, x_max].
                colors (list): the list of color code for rendering different class
                notes (str, Optional): explain the block
            """
            if notes is not None:
                self.add_new_line(notes)
            if colors is None:
                colors = ["#3498db", "#2ecc71", "#e74c3c"]
            self.start_itemize(' - ')
            for idx, (label_name, data_distribution) in enumerate(field_distribution.items()):

                figure_path = '%s/%s_%s_field_distribution.png' % (self.figure_path, field_name, label_name)
                figure_path = gg.KdeDistribution(figure_path=figure_path,
                                                 data=data_distribution,
                                                 title="",
                                                 x_label=field_name, y_label="").draw(color=colors[idx % len(colors)],
                                                                                      force_no_log=force_no_log,
                                                                                      x_limit=x_limit)
                table_header = ['Statistical Field', 'Value']
                table_values = []
                for key, value in data_distribution.items():
                    if key in ['kde', 'histogram', 'x_limit']:
                        continue
                    table_values.append([key, "%d" % int(value)])

                self.add_table_image_group(image_path=figure_path, table_header=table_header,
                                           table_content=table_values, grid_spec=gg_constants.IMAGE_TABLE_GRID_SPEC_NEW,
                                           caption='Distribution for %s' % label_name, style='I')
            self.end_itemize()
            LOGGER.info('Add info: Numeric Data Field [%s] Info' % field_name)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_text_field_distribution(self, field_name: str, field_distribution: dict, notes=None):
        def func(field_name, field_distribution, notes=None):
            """
            add information of field value distribution for text type to the report.
            Details see analyzers inside `xai.data_explorer.text_analyzer`
            Args:
                field_name (str): data field name
                field_distribution (:dict of :dict):
                    -key: label_name
                    -value: tfidf and placeholder distribution under the `label_name`(dict):
                        {'tfidf': tfidf, 'placeholder': placeholder}
                        - tfidf (:list of :list): each sublist has 2 items: word and tfidf
                        - placeholder (:dict):
                            - key: PATTERN
                            - value: percentage
                notes (str, Optional):
                    explain the block
            """
            if notes is not None:
                self.add_new_line(notes)
            self.start_itemize(' - ')
            for idx, (label_name, data_distribution) in enumerate(field_distribution.items()):

                figure_path = '%s/%s_%s_field_distribution.png' % (self.figure_path, field_name, label_name)
                figure_path = gg.WordCloudGraph(figure_path=figure_path,
                                                data=data_distribution['tfidf'],
                                                title='').draw()
                table_header = ['Placeholder', 'Doc Percentage ']
                table_values = []
                for w, v in data_distribution['placeholder'].items():
                    table_values.append([w, '%.2f%%' % (v * 100)])

                self.add_table_image_group(image_path=figure_path, table_header=table_header,
                                           table_content=table_values, grid_spec=gg_constants.IMAGE_TABLE_GRID_SPEC_NEW,
                                           caption='Distribution for %s' % label_name, style='I')
            self.end_itemize()
            LOGGER.info('Add info: Text Data Field [%s] Info' % field_name)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_datetime_field_distribution(self, field_name: str, field_distribution: Dict, notes=None):
        def func(field_name: str, field_distribution: Dict, notes=None):
            """
            add information of field value distribution for datetime type to the report.
            Details see analyzers inside `xai.data_explorer.datetime_analyzer`
            Args:
                field_name (str): data field name
                field_distribution (:dict of :dict):
                    -key: label_name
                    -value (:dict of :dict):
                        - 1st level key: year_X(int)
                        - 1st level value:
                            - 2nd level key: month_X(int)
                            - 2nd level value: count of sample in month_X of year_X
                notes (str, Optional):
                    explain the block
            """
            if notes is not None:
                self.add_new_line(notes)
            self.start_itemize(' - ')
            for idx, (label_name, data_distribution) in enumerate(field_distribution.items()):
                figure_path = '%s/%s_%s_field_distribution.png' % (self.figure_path, field_name, label_name)
                figure_path = gg.DatePlot(figure_path=figure_path,
                                          data=data_distribution,
                                          title='Datetime distribution for %s (for %s samples) ' % (
                                              field_name, label_name),
                                          x_label="", y_label="").draw()

                self.add_large_image(image_path=figure_path,
                                     caption='Distribution for %s' % label_name, style='I')
            self.end_itemize()
            LOGGER.info('Add info: Text Data Field [%s] Info' % field_name)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, \
                   values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    """ Feature section
    """

    def component_feature_importance(self, importance_ranking: List[List], importance_threshold: float,
                                     maximum_number_feature=20, notes=None):
        def func(importance_ranking, importance_threshold,
                 maximum_number_feature=20, notes=None):
            """
            Add information of feature importance to the report.
            Args:
                importance_ranking(:list of :list): a list of 2-item lists, item[0]: score, item[1] feature_name
                importance_threshold(float): threshold for displaying the feature name and score in tables
                maximum_number_feature(int): maximum number of features shown in bar-chart diagram
                notes(str): text to explain the block
            """
            if notes is not None:
                self.add_new_line(notes)
            feature_ranking = [(score, name) for name, score in importance_ranking]
            image_path = '%s/feature_importance.png' % self.figure_path
            image_path = gg.FeatureImportance(figure_path=image_path, data=feature_ranking,
                                              title='feature_importance').draw(limit_length=maximum_number_feature)

            if maximum_number_feature < len(feature_ranking):
                self.add_new_line(
                    "The figure below shows the top %s important features for the trained model." % maximum_number_feature)
            else:
                self.add_new_line(
                    "The figure below shows importance ranking for all features from the trained model.")

            self.ln()

            self.add_large_image(image_path)

            self.add_new_line(
                "The features which have an importance score larger than %s are listed in the below table." %
                importance_threshold)
            self.ln()

            table_header = ['Feature', 'Importance']
            table_data = []

            for feature_name, importance in feature_ranking:
                if float(importance) < importance_threshold:
                    break
                table_data.append([feature_name, importance])

            self.add_table(header=table_header, data=table_data, col_width=[140, 30])

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, \
                   values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    """Training part
    """

    def component_hyperparameter_tuning(self, history: dict, best_idx: str, search_space=None, benchmark_metric=None,
                                        benchmark_threshold=None, non_hyperopt_score=None, notes=None):
        def func(history, best_idx, search_space=None,
                 benchmark_metric=None,
                 benchmark_threshold=None,
                 non_hyperopt_score=None,
                 notes=None):

            """
            Add information of hyperparameter tuning to the report.
            Args:
                history(:dict of dict): a dict of training log dict.
                    key: iteration index
                    value: hyperparameter tuning information
                            Each dict has two keys:
                                - params: a dict of which key is the parameter name and value is parameter value
                                - val_scores: a dict of which key is the metric name and value is metric value
                best_idx(str):
                    - the best idx based on benchmark metric, corresponding the `history` dict key
                search_space(:dict): parameter name and the search space for each parameter
                benchmark_metric(:str): the metric used for benchmarking during hyperparameter tunning
                benchmark_threshold(:float, Optional): the benchmarking threshold to accept the training
                non_hyperopt_score(:float, Optional): the training metric without hyperparameter tuning
                notes(:str): text to explain the block
            """
            # search space
            if notes is not None:
                self.add_new_line(notes)
            self.add_new_line("Hyperparameter Tuning Search Space", style='B')
            self.start_itemize()
            for params, params_search_space in search_space.items():
                self.add_key_value_pair(params, params_search_space)
            self.end_itemize()

            self.ln(5)

            self.add_new_line("Hyperparameter Tuning History Result", style='B')
            self.add_new_line("The metric results from hyperparameter tuning are shown in the figure.")
            self.start_itemize()
            self.add_key_value_pair("Benchmark metric", benchmark_metric)
            self.add_key_value_pair("Benchmark value", benchmark_threshold)
            self.end_itemize()
            self.ln()

            image_path = "%s/hyperopt_history.png" % self.figure_path
            image_path = gg.EvaluationLinePlot(figure_path=image_path, data=history, title='hyper_history',
                                               x_label='Iterations',
                                               y_label='Metrics Score').draw(benchmark_metric=benchmark_metric,
                                                                             benchmark_value=benchmark_threshold)

            self.add_large_image(image_path)
            self.ln()

            # best result for hyperopt

            self.add_new_line("Best Result from Hyperparameter Tuning", style="B")
            self.add_new_line("The best iteration is ", best_idx)
            self.add_new_line("Parameters:", 'B')

            self.start_itemize()
            for param_name, param_value in history[best_idx]['params'].items():
                self.add_key_value_pair("%s" % param_name, param_value)
            self.end_itemize()
            self.ln()

            self.add_new_line("Validation Results:", 'B')

            self.start_itemize()
            for param_name, param_value in history[best_idx]['val_scores'].items():
                if param_name == benchmark_metric:
                    self.add_key_value_pair("%s" % param_name.capitalize(), "%s (benchmarking metric)" % param_value)
                    final_metric_value = param_value
                else:
                    self.add_key_value_pair("%s" % param_name.capitalize(), "%s" % param_value)
            self.end_itemize()

            self.ln(5)

            self.add_subsection("Hyperparameter Tuning Final Conclusion")

            if non_hyperopt_score is None:
                self.add_new_line("There is no benchmarking conducted in this training. ")
                self.add_new_line("We will accept the best result from hyperparameter tuning as final parameter set.")
            else:
                if final_metric_value > non_hyperopt_score:
                    self.add_text("Hyperparameter tuning best result (%.4f) is better than benchmark score (%.4f)," % (
                        final_metric_value, non_hyperopt_score))
                    if final_metric_value > benchmark_threshold:
                        self.add_new_line(
                            ' and it is better than acceptance benchmark scoring (%.4f).' % benchmark_threshold)
                        self.add_new_line('<BR>We accept it as the final parameter setting for the trained model.')
                    else:
                        self.add_new_line(
                            ' but it fails to meet the acceptance benchmark scoring (%.4f).' % benchmark_threshold)
                        self.add_new_line('We still accept it as the final parameter setting for the trained model, ' \
                                          'but will continue to improve it.')

                else:
                    self.add_text("Hyperparameter tuning best result (%.4f) is worse than benchmark score (%.4f), " % (
                        final_metric_value, non_hyperopt_score))

                    if final_metric_value > benchmark_threshold:
                        self.add_new_line(
                            'and benchmarking result is better than acceptance benchmark scoring (%.4f).' % benchmark_threshold)
                        self.add_new_line('We accept default parameters as the final solution for the trained model.')
                    else:
                        self.add_new_line(
                            'but it fails to meet the acceptance benchmark scoring (%.4f).' % benchmark_threshold)
                        self.add_new_line(
                            'We still accept default parameters as the final solution for the trained model, ' \
                            'but will continue to improve it.')
                        self.ln(5)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, \
                   values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_learning_curve(self, history, best_idx, benchmark_metric=None,
                                 benchmark_threshold=None, training_params=None, notes=None):
        def func(history, best_idx, training_params=None, benchmark_metric=None,
                 benchmark_threshold=None, notes=None):
            """
            Add information of learning curve to report.
            Args:
                history(:dict of dict): a dict of training log dict.
                    key: epoch index
                    value: learning epoch information
                            Each dict has two keys:
                                - params: a dict of params on current epochs (Optional)
                                - val_scores: a dict of which key is the metric name and value is metric value
                training_params(:dict): a dict of which key is training parameter name and value is training parameter value
                best_idx(str):
                    - the best epoch based on benchmark metric, corresponding the `history` dict key
                benchmark_metric(:str): the metric used for benchmarking during learning
                benchmark_threshold(:float, Optional): the benchmarking threshold to accept the training
                notes(:str): text to explain the block

            Returns:

            """
            if notes is not None:
                self.add_new_line(notes)
            image_path = "%s/deep_learning_curve.png" % self.figure_path
            image_path = gg.EvaluationLinePlot(figure_path=image_path, data=history, title='training_history',
                                               x_label='Steps',
                                               y_label='Metrics Score').draw(benchmark_metric=benchmark_metric,
                                                                             benchmark_value=benchmark_threshold)
            if training_params is not None:
                self.add_new_line("Training Parameters", style='B')
                self.start_itemize()
                for param_name, param_value in training_params.items():
                    self.add_key_value_pair(param_name, param_value)
                self.end_itemize()
                self.ln()

            self.add_new_line("Learning Curve", style='B')
            self.add_new_line("The metric results from several training epochs are shown in the figure.")

            self.start_itemize()
            self.add_key_value_pair("Benchmark metric", benchmark_metric)
            self.add_key_value_pair("Benchmark value", benchmark_threshold)
            self.end_itemize()

            self.ln()
            self.add_large_image(image_path)

            self.ln()
            self.add_new_line("Best Epoch from Training", style='B')
            self.add_key_value_pair("The best iteration is ", best_idx)
            self.ln()

            self.add_new_line("Validation Results:", style='B')
            self.start_itemize()
            if best_idx not in history:
                best_idx = str(best_idx)
            for param_name, param_value in history[best_idx]['val_scores'].items():
                if param_name == benchmark_metric:
                    self.add_key_value_pair(param_name.capitalize(), "%s (benchmarking metric)" % param_value)
                else:
                    self.add_key_value_pair(param_name.capitalize(), param_value)
            self.end_itemize()
            self.ln(5)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, \
                   values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    """Evaluation
    """

    def component_multi_class_evaluation_metric_results(self, *metric_tuple, notes=None):
        def func(*metric_tuple, notes=None):
            """
            add information about metric results for multi-class evaluation
            Args:
                label_name(str): the label name for current evaluation result
                *metric_tuple(tuple): (evaluation_header, evaluation_metric_dict)
                    - evaluation_header(str): a header for current evaluation, can be split or round number.
                    - evaluation_metric_dict(dict): key-value pair for metric
                        - key: metric name
                        - value: metric dict. The dict should either
                         (1) have a `class` keyword, with key-value pair of class name and corresponding values, or
                         (2) have a `average` keyword to show a macro-average metric.
                notes(str): text to explain the block

            """
            if notes is not None:
                self.add_new_line(notes)
            for eval_name, eval_metric_dict in metric_tuple:
                cr = MultiClassificationResult()
                cr.load_results_from_meta(eval_metric_dict)
                table_name, table_header, table_data, table_layout = cr.convert_metrics_to_table()

                self.add_new_line(table_name, 'B')
                self.add_table(table_header, table_data, table_layout)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, \
                   values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_binary_class_evaluation_metric_results(self, *metric_tuple, notes=None, aggregated=True):
        def func(*metric_tuple, notes=None, aggregated=True):
            """
            add information about metric results for binary-class evaluation
            Args:
                *metric_tuple(tuple): (evaluation_header, evaluation_metric_dict)
                    - evaluation_header(str): a header for current evaluation, can be split or round number.
                    - evaluation_metric_dict(dict): key-value pair for metric
                        - key: metric name
                        - value: metric value
                notes(str): text to explain the block
                aggregated(bool): whether to aggregate multiple result tables into one

            """
            if notes is not None:
                self.add_new_line(notes)

            combined_table_dict = defaultdict(list)
            combined_table_header = ["Split/Round"]
            for eval_name, eval_metric_dict in metric_tuple:
                combined_table_header.append(eval_name)
                cr = BinaryClassificationResult()
                cr.load_results_from_meta(eval_metric_dict)
                table_name, table_header, table_data, table_layout = cr.convert_metrics_to_table()
                if aggregated:
                    table_data_dict = {row[0]: row[1] for row in table_data}
                    for metric_name, metric_value in table_data_dict.items():
                        combined_table_dict[metric_name].append(metric_value)
                else:
                    self.add_new_line('For split/round <B>%s</B>' % eval_name)
                    self.add_table(table_header, table_data)

            if aggregated:
                combined_table_values = []
                for metric_name, metric_value_list in combined_table_dict.items():
                    combined_table_values.append([metric_name] + metric_value_list)

                self.add_new_line(table_name, 'B')
                self.add_table(combined_table_header, combined_table_values)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, \
                   values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_confusion_matrix(self, *confusion_matrix_tuple, notes=None):
        def func(*confusion_matrix_tuple, notes=None):
            """
            add information about confusion matrix to report
            Args:
                *confusion_matrix_tuple(tuple): (confusion_matrix_header, confusion_matrix_dict)
                    - confusion_matrix_header(str): a header for confusion_matrix, can be split or round number.
                    - confusion_matrix_dict(dict):
                        - `labels`(:list of :str): label of classes
                        - `values`(:list of :list): 2D list for confusion matrix value, row for predicted, column for true.
                notes(str): text to explain the block
            """
            if notes is not None:
                self.add_new_line(notes)
            image_list = []
            for idx, (eval_name, confusion_matrix_mat) in enumerate(confusion_matrix_tuple):
                figure_path = '%s/%s_%s_cm.png' % (self.figure_path, idx, eval_name)
                image_path = gg.HeatMap(figure_path=figure_path, data=confusion_matrix_mat['values'],
                                        title=eval_name, x_label='Predict',
                                        y_label='True').draw(x_tick=confusion_matrix_mat['labels'],
                                                             y_tick=confusion_matrix_mat['labels'],
                                                             color_bar=True)
                image_list.append(image_path)
            if len(image_list) == 1:
                self.add_grid_images(image_set=image_list, grid_spec={0: (0, 0, 80, 80)})
            else:
                column_width = 180 / (len(image_list) + 1)
                cur_w = column_width
                spec_list = dict()
                for i in range(len(image_list)):
                    spec_list[i] = (cur_w, 0, column_width, column_width)
                    cur_w += column_width
                self.add_list_of_grid_images(image_list, spec_list)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, \
                   values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_multi_class_confidence_distribution(self, *visual_result_tuple, max_num_classes=9, notes=None):
        def func(*visual_result_tuple, max_num_classes=9, notes=None):
            """
            add information about confusion matrix to report
            Args:
                *visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
                   - visual_result_header(str): a header for confusion_matrix, can be split or round number.
                   - visual_result_dict(dict): key-value
                       - key(str): the predicted class
                       - value(dit): result dict
                            - `gt` (:list of :str): ground truth class label for all samples
                            - `values` (:list of :float): probability for all samples
                max_num_classes(int, Optional): maximum number of classes displayed for each graph
                notes(str,Optional): text to explain the block
           """
            import operator
            for eval_name, eval_vis_result in visual_result_tuple:
                predicted_class_count = dict()
                for label in eval_vis_result.keys():
                    data = eval_vis_result[label]
                    num_sample = len(data['gt'])
                    predicted_class_count[label] = num_sample

                    sorted_class_size = sorted(predicted_class_count.items(), key=operator.itemgetter(1))[::-1]
                    top_classes = [a for (a, _) in sorted_class_size]

                image_path_list = []
                for class_label in top_classes:
                    data = eval_vis_result[class_label]
                    num_sample = len(data['gt'])
                    if num_sample > 0:
                        image_path = '%s/%s_%s_conf_dist.png' % (self.figure_path, label, class_label)
                        sw_image_path = gg.ResultProbabilityForMultiClass(image_path, data,
                                                                          'Predicted as %s' % label).draw()
                        image_path_list.append(sw_image_path)
                    if len(image_path_list) >= max_num_classes:
                        break
                self.add_list_of_grid_images(image_set=image_path_list,
                                             grid_spec=gg_constants.ABSOLUTE_3_EQUAL_GRID_SPEC)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, \
                   values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_binary_class_confidence_distribution(self, *visual_result_tuple, notes=None):
        def func(*visual_result_tuple, notes=None):
            """
            add information about confusion matrix to report
            Args:
                *visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
                   - visual_result_header(str): a header for confusion_matrix, can be split or round number.
                   - visual_result_dict(dict): key-value
                        - `gt` (:list of :str): ground truth class label for all samples
                        - `probability` (:list of :list): 2D list (N sample * 2) to present probability distribution of each sample
                max_num_classes(int, Optional): maximum number of classes displayed for each graph
                notes(str,Optional): text to explain the block
            """
            if notes is not None:
                self.add_new_line(notes)
            image_list = []
            for eval_name, eval_vis_result in visual_result_tuple:
                image_path = "%s/%s_prob_dist.png" % (self.figure_path, eval_name)
                image_path = gg.ResultProbability(figure_path=image_path, data=eval_vis_result,
                                                  title='Probability Distribution').draw()
                image_list.append(image_path)

            if len(image_list) == 1:
                self.add_grid_images(image_set=image_list, grid_spec={0: (0, 0, 80, 80)})
            else:
                column_width = 180 / (len(image_list) + 1)
                cur_w = column_width
                spec_list = dict()
                for i, _ in enumerate(image_list):
                    spec_list[i] = (cur_w, 0, column_width, column_width)
                    cur_w += column_width
                self.add_list_of_grid_images(image_list, spec_list)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, \
                   values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_binary_class_reliability_diagram(self, *visual_result_tuple, notes=None):
        def func(*visual_result_tuple, notes=None):
            """
            add information about reliability to report
            Args:
                *visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
                   - visual_result_header(str): a header for confusion_matrix, can be split or round number.
                   - visual_result_dict(dict): key-value
                        - `gt` (:list of :str): ground truth class label for all samples
                        - `probability` (:list of :list): 2D list (N sample * 2) to present probability distribution of each sample
                notes(str,Optional): text to explain the block
            """
            if notes is not None:
                self.add_new_line(notes)
            image_list = []
            for eval_name, eval_vis_result in visual_result_tuple:
                image_path = "%s/%s_reliability_diagram.png" % (self.figure_path, eval_name)
                image_path = gg.ReliabilityDiagram(figure_path=image_path, data=eval_vis_result,
                                                   title='Reliability Diagram').draw()
                image_list.append(image_path)

            if len(image_list) == 1:
                self.add_grid_images(image_set=image_list, grid_spec={0: (0, 0, 80, 80)})
            else:
                column_width = 180 / (len(image_list) + 1)
                cur_w = column_width
                spec_list = dict()
                for i, _ in enumerate(image_list):
                    spec_list[i] = (cur_w, 0, column_width, column_width)
                    cur_w += column_width
                self.add_list_of_grid_images(image_list, spec_list)

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, \
                   values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    """ Cover page section
    """

    def component_training_timing(self, timing: List[Tuple[str, int]], notes=None):
        def func(timing, notes=None):
            """
            add information of timing to the report
            Args:
                timing（:obj:`list` of :obj:`tuple`): list of tuple (name, time in second)
                notes (str): explain the block
            """

            if notes is not None:
                self.add_new_line(notes)

            self.start_itemize()
            for name, time_in_sec in timing:
                self.add_key_value_pair(key=name, value=datetime.timedelta(seconds=time_in_sec))
            self.end_itemize()
            self.ln()
            LOGGER.info('Add info: Timing')

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_dataset_summary(self, data_summary: List[Tuple[str, int]], notes=None):
        def func(data_summary, notes=None):
            """
            add information of dataset summary to the report
            Args:
                data_summary (:obj:`list` of :obj:`tuple`): list of tuple (dataset_name, dataset_sample_number)
                notes (str, Optional): explain the block

            """

            if notes is not None:
                self.add_new_line(notes)

            self.start_itemize()
            for name, quantity in data_summary:
                self.add_key_value_pair(key="Number of %s samples" % name,
                                        value=quantity)
            self.end_itemize()
            self.ln()
            LOGGER.info('Add info: Dataset Summary')

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_evaluation_result_summary(self, *evaluation_result, notes=None):
        def func(*evaluation_result, notes=None):
            """
            add information of training performance to the result

            Args:
                evaluation_result (dict): evaluation metric
                    - key: metric_name
                    - value: metric_value: single float value for average/overall metric, list for class metrics

                    sample input 1: {'precision': 0.5}, report value directly
                    sample input 2: {'precision': {'class':[0.5,0.4,0.3],'average':0.5}}, report "average" value
                    sample input 3: {'precision': {'class':[0.5,0.4,0.3]}, report unweighted average for "class" value
                notes (str, Optional): explain the block

            """
            if notes is not None:
                self.add_new_line(notes)
            for result in evaluation_result:
                self.start_itemize()
                for metric_name, metric_value in result.items():
                    if type(metric_value) == dict:
                        if 'average' in metric_value.keys():
                            key = "%s (average)" % metric_name.capitalize()
                            if type(metric_value['average']) == float or type(metric_value['average']) == str:
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
                            value = "%.4f" % np.mean(np.array(metric_value['class']))
                        else:
                            LOGGER.error(
                                'No defined keys (`class`,`average`) found in metric value: %s' % (metric_value.keys()))
                            continue

                    elif type(metric_value) == float:
                        key = "%s" % metric_name.capitalize()
                        value = "%.4f" % metric_value
                    elif type(metric_value) == str:
                        key = "%s" % metric_name.capitalize()
                        value = metric_value
                    else:
                        LOGGER.error(
                            'Unsupported metric value type for metric (%s): %s' % (metric_name, type(metric_value)))
                        continue
                    self.add_key_value_pair(key, value)
                self.end_itemize()
                self.ln()

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def component_model_info_summary(self, model_info=None, notes=None):
        def func(model_info, notes=None):
            """
            add information of dataset summary to the report
            Args:
                model_info (:obj:`list` of :obj:
                    `tuple`, Optional): list of tuple (model info attribute, model info value).
                    Default information include `use case name`, `version`, `use case team`.
                notes (str, Optional):
                    explain the block

            """
            if model_info is None:
                model_info = []
                model_info.append(('Use case name', self.usecase_name))
                model_info.append(('Version', self.version))
                model_info.append(('Use case team', self.author))

            if notes is not None:
                self.add_new_line(notes)

            self.start_itemize()
            for attribute, value in model_info:
                self.add_key_value_pair(key=attribute, value=value)
            self.end_itemize()
            self.ln()
            LOGGER.info('Add info: Model Info')

        frame = inspect.currentframe()
        kwargs, varargs, _, values = inspect.getargvalues(frame)
        if varargs is not None:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}, values[varargs]
        else:
            return func, {kvar: values[kvar] for kvar in kwargs if kvar != 'self'}

    def generate_cover_page(self, summary_notes=None, model_info=None, data_summary=None, timing=None,
                            evaluation_result=None):
        """
        add a summary cover page for the report
        Args:
            summary_notes: html component, see `component_paragraph_in_html`
            model_info: model_info component, see `component_model_info`
            data_summary: data_summary component, see `component_data_summary`
            timing: timing component, see `component_timing`
            evaluation_result: list of evaluation_result component (to be compatible for multi-label issue), see `evaluation_result`
        """
        self.add_page()
        self.add_ribbon('Report Summary')

        ## create content page buffer
        cover_page_content = []
        if summary_notes is not None:
            cover_page_content.append((self.add_new_line, {'line': 'Summary Note', 'style': 'B'}))
            cover_page_content.append(summary_notes)

        if model_info is not None:
            cover_page_content.append((self.add_new_line, {'line': 'Model Information', 'style': 'B'}))
            cover_page_content.append(model_info)

        if data_summary is not None:
            cover_page_content.append((self.add_new_line, {'line': 'Data Summary', 'style': 'B'}))
            cover_page_content.append(data_summary)

        if timing is not None:
            cover_page_content.append((self.add_new_line, {'line': 'Training Timing', 'style': 'B'}))
            cover_page_content.append(timing)

        if evaluation_result is not None:
            cover_page_content.append((self.add_new_line, {'line': 'Evaluation Result', 'style': 'B'}))
            cover_page_content.append(evaluation_result)

        cover_page_content.append((self.add_page, {}))
        cover_page_content.append(self.__component_content_table())

        ## add cover_page_content at the beginning of the report
        self.__content_buffer = cover_page_content + self.__content_buffer
