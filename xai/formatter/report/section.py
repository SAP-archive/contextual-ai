#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""Report Section - Base"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy
from typing import Tuple, Dict, List

from xai.data import explorer
from xai import (
 MODE
)

################################################################################
### Section Strategy
################################################################################
class Section:
    COVER = 10
    CONTENT_TABLE = 20
    DETAIL = 30

    def __init__(self, type: int, contents=None):
        """
        Report Section

        Args:
            type (int): Section Type (cover, detail)
            contents(list) Content List
        """
        self._type = type
        self._contents = contents

    @property
    def type(self):
        """Returns section type."""
        return self._type

    @property
    def contents(self) -> list:
        """Returns section content list."""
        return self._contents

    ################################################################################
    ###  Content Base Section
    ################################################################################

    def add_new_page(self):
        """
        add a new page
        """
        from xai.formatter.contents import NewPage
        self.contents.append(NewPage())

    def add_header_level_1(self, text: str):
        """
        add a header level 1 into the section

        Args:
            text(str): header level 1 in the report
        """
        from xai.formatter.contents import Header
        self.contents.append(Header(text=text, level=Header.LEVEL_1))

    def add_header_level_2(self, text: str):
        """
        add a header level 2 into the section

        Args:
            text(str): header level 2 in the report
        """
        from xai.formatter.contents import Header
        self.contents.append(Header(text=text, level=Header.LEVEL_2))

    def add_header_level_3(self, text: str):
        """
        add a header level 3 into the section

        Args:
            text(str): header level 3 in the report
        """
        from xai.formatter.contents import Header
        self.contents.append(Header(text=text, level=Header.LEVEL_3))

    def add_section_title(self, text: str):
        """
        add a title into the section
        Args:
            text(str): title in the report
        """
        from xai.formatter.contents import SectionTitle
        self.contents.append(SectionTitle(text=text))

    def add_paragraph_title(self, text: str):
        """
        add a title into the paragraph

        Args:
            text(str): title in the report
        """
        from xai.formatter.contents import ParagraphTitle
        self.contents.append(ParagraphTitle(text=text))

    def add_paragraph(self, text: str):
        """
        add a paragraph into the section

        Args:
            text(str): html text to render in the report
        """
        from xai.formatter.contents import Paragraph
        self.contents.append(Paragraph(text=text))

    ################################################################################
    ###  Content Basic Section
    ################################################################################

    def add_key_value_pairs(self, info_list: list, notes=None):
        """
        add key-values info as simple paragraph

        Args:
            info_list(list): list of tuple / list of (list of tuple))
                multi-level rendering, e.g. to display `model_info`
            notes (str): explain the block
        """
        from xai.formatter.contents import BasicKeyValuePairs
        self.contents.append(BasicKeyValuePairs(info=info_list, notes=notes))

    def add_table(self, table_header: list, table_data: list,
                         col_width: list, notes=None):
        """
        add simple table

        Args:
            table_header (list): list of str
            table_data (list): list of str
            col_width (list): list of float,
                default: None (evenly divided for the whole page width)
            notes (str): explain the block
        """
        from xai.formatter.contents import BasicTable
        self.contents.append(BasicTable(table_header=table_header,
                                        table_data=table_data,
                                        col_width=col_width,
                                        notes=notes))

    def add_images_grid(self, image_list: list, grid_spec: list, notes=None):
        """
        add image blocks with formatted grid specification

        Args:
            image_list (list): the list of image_paths
            grid_spec (dict): indicate image size and position
                - key: image_name, or index if image_set is a list
                - value: (x,y,w,h) position and weight/height of image,
                      with left top corner of the block as (0,0), unit in mm
            notes (str): explain the block
        """
        from xai.formatter.contents import BasicImageGrid
        self.contents.append(BasicImageGrid(image_list=image_list,
                                            grid_spec=grid_spec,
                                            notes=notes))

    ################################################################################
    ###  Content Summary Section
    ################################################################################
    def add_training_timing(self, timing: List[Tuple[str, int]], notes=None):
        """
        add information of timing to the report

        Args:
            timing (:obj:`list` of :obj:`tuple`): list of tuple
                        (name, time in second)
            notes (str): explain the block
        """
        from xai.formatter.contents import TrainingTiming
        self.contents.append(TrainingTiming(timing=timing, notes=notes))

    def add_data_set_summary(self, data_summary: List[Tuple[str, int]],
                             notes=None):
        """
        add information of dataset summary to the report

        Args:
            data_summary (:obj:`list` of :obj:`tuple`): list of tuple
                        (dataset_name, dataset_sample_number)
            notes (str, Optional): explain the block
        """
        from xai.formatter.contents import DataSetSummary
        self.contents.append(DataSetSummary(data_summary=data_summary,
                                            notes=notes))

    def add_evaluation_result_summary(self, evaluation_result: dict,
                             notes=None):
        """
        add information of training performance to the result

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
        from xai.formatter.contents import EvaluationResultSummary
        self.contents.append(EvaluationResultSummary(evaluation_result=evaluation_result,
                                                     notes=notes))

    def add_model_info_summary(self, model_info: list, notes=None):
        """
        add information of model info to the report

        Args:
            model_info (:obj:`list` of :obj:
                `tuple`, Optional): list of tuple (model info attribute, model info value).
                Default information include `use case name`, `version`, `use case team`.
            notes (str, Optional):
                explain the block
        """
        from xai.formatter.contents import ModelInfoSummary
        self.contents.append(ModelInfoSummary(model_info=model_info, notes=notes))


    ################################################################################
    ###  Content Data Section
    ################################################################################
    def add_data_missing_value(self, missing_count: dict,
                               total_count: list, ratio=False, notes=None):
        """
        add information of missing value for data fields to the report

        Args:
            missing_count (dict):
                - key: data field name
                - value: the count or the percentage of missing value in the field
            total_count (dict, Optinal):
                - key: data field name
                - value: the count of missing value in the field
            ratio (bool): True if `missing_value` is the percentage
            notes (str, Optional):
                explain the block
        """
        from xai.formatter.contents import DataMissingValue
        self.contents.append(DataMissingValue(missing_count=missing_count,
                                              total_count=total_count,
                                              ratio=ratio, notes=notes))

    def add_data_set_distribution(self,
                                  dataset_distribution: Tuple[str, explorer.CategoricalStats],
                                  max_class_shown=20, notes=None):
        """
        add information of distribution on data set to the report

        Args:
            dataset_distribution (tuple: (str,dict)):
                - tuple[0] str: label/split name
                - tuple[1] dict: key - class_name/split_name,
                - tuple[1] CategoricalStats object: `frequency_count` attribute
                                 key - class_name/split_name,
                                 value - class_count/split_count
            max_class_shown (int, Optional): maximum number of classes shown
            in the figure, default is 20
            notes (str, Optional):
                explain the block
        """
        from xai.formatter.contents import DataSetDistribution
        self.contents.append(DataSetDistribution(
            dataset_distribution=dataset_distribution,
            max_class_shown=max_class_shown, notes=notes))

    def add_data_attributes(self, data_attribute: Dict, notes=None):
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
        from xai.formatter.contents import DataAttributes
        self.contents.append(DataAttributes(data_attribute=data_attribute,
                                            notes=notes))

    def add_categorical_field_distribution(self, field_name: str,
                                           field_distribution: dict,
                                           max_values_display=20,
                                           colors=None, notes=None):
        """
        add information of field value distribution for categorical type to the report.
        Details see analyzers inside `xai.data_explorer.categorical_analyzer`

        Args:
            field_name (str): data field name
            field_distribution (:dict of [a type of stats]):
                -key: label_name
                -value: frequency distribution under the `label_name`(dict)
                    - key: field value
                    - value: field value frequency
            max_values_display (int): maximum number of values displayed
                                default 20
            colors (list): the list of color code for rendering different class
            notes (str, Optional):
                explain the block
        """
        from xai.formatter.contents import CategoricalFieldDistribution
        self.contents.append(CategoricalFieldDistribution(
            field_name=field_name, field_distribution=field_distribution,
            max_values_display=max_values_display, colors=colors, notes=notes))

    def add_numeric_field_distribution(self, field_name: str,
                                       field_distribution: dict,
                                       force_no_log=False, x_limit=False,
                                       colors=None, notes=None):
        """
        add information of field value distribution for numerical type to the report.
        Details see analyzers inside `xai.data_explorer.numerical_analyzer`

        Args:
            field_name (str): data field name
            field_distribution (dict of [a type of stats]):
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
                            If True, field_distribution should have a key
                                    "x_limit" and value of [x_min, x_max].
            colors (list): the list of color code for rendering different class
            notes (str, Optional): explain the block
        """
        from xai.formatter.contents import NumericFieldDistribution
        self.contents.append(NumericFieldDistribution(
            field_name=field_name,
            field_distribution=field_distribution, force_no_log=force_no_log,
            x_limit=x_limit, colors=colors, notes=notes))

    def add_text_field_distribution(self, field_name: str,
                                    field_distribution: dict, notes=None):
        """
        add information of field value distribution for text type to the report.
        Details see analyzers inside `xai.data_explorer.text_analyzer`

        Args:
            field_name (str): data field name
            field_distribution (dict of [a type of TextStats]):
                -key: label_name
                -value: tfidf and placeholder distribution under the `label_name`(dict):
                    {'tfidf': tfidf, 'placeholder': placeholder}
                    - tfidf (:list of :list): each sublist has 2 items: word and tfidf
                    - placeholder (:dict):
                        - key: PATTERN
                        - value: percentage
            notes (str, Optional): explain the block
        """
        from xai.formatter.contents import TextFieldDistribution
        self.contents.append(TextFieldDistribution(
            field_name=field_name,
            field_distribution=field_distribution, notes=notes))

    def add_datetime_field_distribution(self, field_name: str,
                                        field_distribution: dict, notes=None):
        """
        add information of field value distribution for datetime type to the report.
        Details see analyzers inside `xai.data_explorer.datetime_analyzer`

        Args:
            field_name (str): data field name
            field_distribution (dict of [a type of DatetimeStats]):
                -key: label_name
                -value (:dict of :dict):
                    - 1st level key: year_X(int)
                    - 1st level value:
                        - 2nd level key: month_X(int)
                        - 2nd level value: count of sample in month_X of year_X
            notes (str, Optional): explain the block
        """
        from xai.formatter.contents import DateTimeFieldDistribution
        self.contents.append(DateTimeFieldDistribution(
            field_name=field_name,
            field_distribution=field_distribution, notes=notes))

    ################################################################################
    ###  Content Feature Section
    ################################################################################
    def add_feature_importance(self, importance_ranking: List[List],
                               importance_threshold: float,
                               maximum_number_feature=20, notes=None):
        """
        add information of feature importance to the report.

        Args:
            importance_ranking(:list of :list): a list of 2-item lists,
                                        item[0]: score, item[1] feature_name
            importance_threshold(float): threshold for displaying the feature
                                                name and score in tables
            maximum_number_feature(int): maximum number of features shown in bar-chart diagram
            notes(str): text to explain the block
        """
        from xai.formatter.contents import FeatureImportance
        self.contents.append(FeatureImportance(
            importance_ranking=importance_ranking,
            importance_threshold=importance_threshold,
            maximum_number_feature=maximum_number_feature, notes=notes))

    def add_feature_shap_values(self, mode: str, feature_shap_values: List[Tuple[str,List]],
                                class_id: int, train_data: numpy.ndarray, notes=None):
        """
        add information of feature importance to the report.

        Args:
            mode (str): Model Model - classification/regression model
            feature_shap_values(:list of :tuple): a list of 2-item tuple,
                                                  item[0]: feature name, item[1] shap values on each training samples
            class_id(int): the class id for visualization.
            train_data(numpy.dnarray): Optional, training data, row is for samples, column is for features.
            notes(str): text to explain the block
        """
        from xai.formatter.contents import FeatureShapValues
        self.contents.append(FeatureShapValues(mode=mode,
                                               feature_shap_values=feature_shap_values,
                                               class_id=class_id,
                                               train_data=train_data,
                                               notes=notes))

    ################################################################################
    ###  Content Training Section
    ################################################################################
    def add_hyperparameter_tuning(self, history: dict, best_idx: str,
                                  search_space=None, benchmark_metric=None,
                                  benchmark_threshold=None,
                                  non_hyperopt_score=None, notes=None):
        """
        add information of hyperparameter tuning to the report.

        Args:
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
            benchmark_metric(:str): the metric used for benchmarking during hyperparameter tunning
            benchmark_threshold(:float, Optional): the benchmarking threshold to accept the training
            non_hyperopt_score(:float, Optional): the training metric without hyperparameter tuning
            notes(:str): text to explain the block
        """
        from xai.formatter.contents import HyperParameterTuning
        self.contents.append(HyperParameterTuning(
            history=history, best_idx=best_idx, search_space=search_space,
            benchmark_metric=benchmark_metric,
            benchmark_threshold=benchmark_threshold,
            non_hyperopt_score=non_hyperopt_score, notes=notes))

    def add_learning_curve(self, history: dict, best_idx: str,
                           benchmark_metric=None, benchmark_threshold=None,
                           training_params=None, notes=None):
        """
        add information of learning curve to report.

        Args:
            history(:dict of dict): a dict of training log dict.
                key: epoch index
                value: learning epoch information
                        Each dict has two keys:
                            - params: a dict of params on current epochs (Optional)
                            - val_scores: a dict of which key is the metric name and value is metric value
            best_idx(str):
                - the best epoch based on benchmark metric, corresponding the `history` dict key
            benchmark_metric(:str): the metric used for benchmarking during learning
            benchmark_threshold(:float, Optional): the benchmarking threshold to accept the training
            training_params(:dict): a dict of which key is training
                                parameter name and value is training parameter value
            notes(:str): text to explain the block
        """
        from xai.formatter.contents import LearningCurve
        self.contents.append(LearningCurve(
            history=history, best_idx=best_idx,
            benchmark_metric=benchmark_metric,
            benchmark_threshold=benchmark_threshold,
            training_params=training_params, notes=notes))

    ################################################################################
    ###  Content Interpreter Section
    ################################################################################
    def add_model_interpreter(self, *, mode: str, class_stats: dict,
                              total_count: int, stats_type: str, k:int,
                              top: int=15, notes=None):
        """
        add model interpreter for classification

        Args:
            mode (str): Model Model - classification/regression model
            class_stats (dict): A dictionary maps the label to its aggregated statistics
            total_count (int): The total number of explanations to generate the statistics
            stats_type (str): The defined stats_type for statistical analysis
            k (int): The k value of the defined stats_type
            top (int): the number of top explanation to display
            notes(str): text to explain the block
        """
        from xai.formatter.contents import ModelInterpreter
        self.contents.append(ModelInterpreter(mode=mode,
                                              class_stats=class_stats, total_count=total_count,
                                              stats_type=stats_type, k=k, top=top, notes=notes))

    def add_error_analysis(self, *, mode: str, error_stats: dict, stats_type: str,
                                              k:int, top: int=15, notes=None):
        """
        add error analysis by class

        Args:
            mode (str): Model Model - classification/regression model
            error_stats (dict): A dictionary maps the label to its aggregated statistics
            stats_type (str): The defined stats_type for statistical analysis
            k (int): The k value of the defined stats_type
            top (int): the number of top explanation to display
            notes(str): text to explain the block
        """
        from xai.formatter.contents import ErrorAnalysis
        self.contents.append(ErrorAnalysis(mode=mode, error_stats=error_stats,
                                           stats_type=stats_type, k=k,
                                           top=top, notes=notes))

    ################################################################################
    ###  Content Evaluation Section
    ################################################################################
    def add_multi_class_evaluation_metric_results(self, *metric_tuple,
                                                  notes=None):
        """
        add information about metric results for multi-class evaluation

        Args:
            *metric_tuple(tuple): (evaluation_header, evaluation_metric_dict)
                - evaluation_header(str): a header for current evaluation,
                                        can be split or round number.
                - evaluation_metric_dict(dict): key-value pair for metric
                    - key: metric name
                    - value: metric dict. The dict should either
                     (1) have a `class` keyword, with key-value pair of class name
                                    and corresponding values, or
                     (2) have a `average` keyword to show a macro-average metric.
            notes(str): text to explain the block
        """
        from xai.formatter.contents import MultiClassEvaluationMetricResult
        self.contents.append(MultiClassEvaluationMetricResult(
            metric_tuple=metric_tuple, notes=notes))

    def add_binary_class_evaluation_metric_results(self, *metric_tuple: tuple,
                                                   aggregated=True,
                                                   notes=None):
        """
        add information about metric results for binary-class evaluation

        Args:
            metric_tuple(tuple): (evaluation_header, evaluation_metric_dict)
                - evaluation_header(str): a header for current evaluation,
                        can be split or round number.
                - evaluation_metric_dict(dict): key-value pair for metric
                    - key: metric name
                    - value: metric value
            aggregated(bool): whether to aggregate multiple result tables into one
                            default: True
            notes(str): text to explain the block
        """
        from xai.formatter.contents import BinaryClassEvaluationMetricResult
        self.contents.append(BinaryClassEvaluationMetricResult(
            metric_tuple=metric_tuple, aggregated=aggregated, notes=notes))

    def add_confusion_matrix_results(self, *confusion_matrix_tuple: tuple,
                                     notes=None):
        """
        Add information about confusion matrix to report

        Args:
            *confusion_matrix_tuple(tuple): (confusion_matrix_header, confusion_matrix_dict)
                - confusion_matrix_header(str): a header for confusion_matrix,
                                                can be split or round number.
                - confusion_matrix_dict(dict):
                    - `labels`(:list of :str): label of classes
                    - `values`(:list of :list): 2D list for confusion matrix value,
                                row for predicted, column for true.
            notes(str): text to explain the block
        """
        from xai.formatter.contents import ConfusionMatrixResult
        self.contents.append(ConfusionMatrixResult(
            confusion_matrix_tuple=confusion_matrix_tuple, notes=notes))

    def add_multi_class_confidence_distribution(self,
                                                *visual_result_tuple: tuple,
                                                max_num_classes=9,
                                                notes=None):
        """
        add information about multi class confidence distribution to report

        Args:
            *visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
               - visual_result_header(str): a header for confusion_matrix,
                                            can be split or round number.
               - visual_result_dict(dict): key-value
                   - key(str): the predicted class
                   - value(dit): result dict
                        - `gt` (:list of :str): ground truth class label for all samples
                        - `values` (:list of :float): probability for all samples
            max_num_classes(int, Optional): maximum number of classes displayed for each graph
            notes(str,Optional): text to explain the block
        """
        from xai.formatter.contents import MultiClassConfidenceDistribution
        self.contents.append(MultiClassConfidenceDistribution(
            visual_result_tuple=visual_result_tuple,
            max_num_classes=max_num_classes, notes=notes))

    def add_binary_class_confidence_distribution(self,
                                                 *visual_result_tuple: tuple,
                                                 notes=None):
        """
        add information about binary class confidence distribution to report

        Args:
            *visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
               - visual_result_header(str): a header for confusion_matrix,
                                                can be split or round number.
               - visual_result_dict(dict): key-value
                    - `gt` (:list of :str): ground truth class label for all samples
                    - `probability` (:list of :list): 2D list (N sample * 2) to
                                    present probability distribution of each sample
            notes(str,Optional): text to explain the block
        """
        from xai.formatter.contents import BinaryClassConfidenceDistribution
        self.contents.append(BinaryClassConfidenceDistribution(
            visual_result_tuple=visual_result_tuple, notes=notes))

    def add_binary_class_reliability_diagram(self,
                                             *visual_result_tuple: tuple,
                                             notes=None):
        """
        add information about reliability to report

        Args:
            *visual_result_tuple(tuple): (visual_result_header, visual_result_dict)
               - visual_result_header(str): a header for confusion_matrix,
                                        can be split or round number.
               - visual_result_dict(dict): key-value
                    - `gt` (:list of :str): ground truth class label for all samples
                    - `probability` (:list of :list): 2D list (N sample * 2) to
                            present probability distribution of each sample
            notes(str,Optional): text to explain the block
        """
        from xai.formatter.contents import BinaryClassReliabilityDiagram
        self.contents.append(BinaryClassReliabilityDiagram(
            visual_result_tuple=visual_result_tuple, notes=notes))


################################################################################
###  Overview Section
################################################################################
class OverviewSection(Section):
    """
    Overview Section
    """

    def __init__(self) -> None:
        """
        Overview Section
        """
        from xai.formatter.contents.base import NewPage
        contents = list()
        contents.append(NewPage())
        super(OverviewSection, self).__init__(type=Section.COVER,
                                              contents=contents)


################################################################################
###  Detail Section
################################################################################
class DetailSection(Section):
    """
    Details Section
    """

    def __init__(self) -> None:
        """
        Details Section
        """
        contents = list()
        super(DetailSection, self).__init__(type=Section.DETAIL,
                                            contents=contents)