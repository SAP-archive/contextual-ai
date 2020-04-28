#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Abstract Writer """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from abc import ABC, abstractmethod

from typing import Tuple, Dict, List
import numpy

from xai.data import explorer
from xai.formatter.report.section import OverviewSection, DetailSection


################################################################################
### Writer Visitor
################################################################################
class Writer(ABC):
    """
    The Strategy interface declares operations common to all
    supported report output.
    """

    def __init__(self, *values) -> None:
        """
        Abstract Writer
        """
        self._values = values

    @property
    def values(self):
        """Returns keyword-ed variable."""
        return self._values

    def __str__(self):
        return 'Writer:(' + str(self.values) + ')'

    @abstractmethod
    def out(self):
        """
        Output Report
        """
        pass

    @abstractmethod
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
        pass

    ################################################################################
    ###  Base Section
    ################################################################################
    @abstractmethod
    def add_new_page(self):
        """
        Add new page
        """
        pass

    @abstractmethod
    def draw_header(self, text: str, level: int, *, link=None):
        """
        Draw Header

        Args:
            text(str): header text in the report
            level(int): header level
            link: header link
        """
        pass

    @abstractmethod
    def draw_title(self, text: str, level: int, *, link=None):
        """
        Draw Title

        Args:
            text(str): title in the report
            level(int): title type (section or paragraph)
            link: title link
        """
        pass

    @abstractmethod
    def draw_paragraph(self, text: str):
        """
        Draw Paragraph

        Args:
            text(str): html text to render in the report
        """
        pass

    ################################################################################
    ###  Basic/Reusable Section
    ################################################################################
    @abstractmethod
    def draw_basic_key_value_pairs(self, notes: str, *,
                                   info: list):
        """
        Draw key-value pairs information to the report

        Args:
            notes(str): Explain the block
            info (list): list of tuple / list of (list of tuple))
                multi-level rendering, e.g. to display `model_info`
        """
        pass

    @abstractmethod
    def draw_basic_table(self, notes: str, *,
                         table_header: list, table_data: list,
                         col_width: list):
        """
        Draw table to the report

        Args:
            notes(str): Explain the block
            table_header (list): list of str
            table_data (list): list of str
            col_width: list of float,
                default: None (evenly divided for the whole page width)
        """
        pass

    @abstractmethod
    def draw_basic_images_with_grid_spec(self, notes: str, *,
                                        image_list, grid_spec):
        """
        Draw image blocks with formatted grid specification

        Args
            notes(str): Explain the block
            image_list (list): the list of image_paths
            grid_spec (dict): indicate image size and position
                - key: image_name, or index if image_set is a list
                - value: (x,y,w,h) position and weight/height of image,
                      with left top corner of the block as (0,0), unit in mm

        """
        pass

    ################################################################################
    ###  Summary Section
    ################################################################################
    @abstractmethod
    def draw_training_time(self, notes: str, *, timing: List[Tuple[str, int]]):
        """
        Draw information of timing to the report

        Args:
            notes(str): Explain the block
            timing (:obj:`list` of :obj:`tuple`): list of tuple
                        (name, time in second)
        """
        pass

    @abstractmethod
    def draw_data_set_summary(self, notes: str, *,
                              data_summary: List[Tuple[str, int]]):
        """
        Draw information of dataset summary to the report

        Args:
            notes(str): Explain the block
            data_summary (:obj:`list` of :obj:`tuple`): list of tuple
                        (dataset_name, dataset_sample_number)
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def draw_model_info_summary(self, notes: str, *, model_info: list):
        """
        Draw information of model info to the result

        Args:
            model_info (:obj:`list` of :obj:
              `tuple`, Optional): list of tuple (model info attribute, model info value).
               Default information include `use case name`, `version`, `use case team`.
            notes (str, Optional): explain the block
        """
        pass

    ################################################################################
    ###  Data Section
    ################################################################################
    @abstractmethod
    def draw_data_missing_value(self, notes: str, *, missing_count: dict,
                                total_count: dict, ratio=False):
        """
        Draw Missing Data Value Summary Table

        Args:
            notes(str): Explain the block
            missing_count(dict): Missing Count
            total_count(list): Total Count
            ratio(bool): True if `missing_value` is the percentage
        """
        pass

    @abstractmethod
    def draw_data_set_distribution(self, notes: str, *,
                                   data_set_distribution: Tuple[str, explorer.CategoricalStats],
                                   max_class_shown=20):
        """
        Draw information of distribution on data set

        Args:
            notes(str): Explain the block
            data_set_distribution (tuple: (str,dict)):
                - tuple[0] str: label/split name
                - tuple[1] CategoricalStats object: `frequency_count` attribute
                                 key - class_name/split_name,
                                 value - class_count/split_count
            max_class_shown (int, Optional): maximum number of classes shown
                          in the figure, default is 20
            notes (str, Optional):
                explain the block
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def draw_categorical_field_distribution(self, notes: str, *,
                                            field_name: str,
                                            field_distribution: Dict[str,
                                                                     explorer.CategoricalStats],
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
                -value: CategoricalStats object
            max_values_display (int): maximum number of values displayed
            colors (list): the list of color code for rendering different class
        """
        pass

    @abstractmethod
    def draw_numeric_field_distribution(self, notes: str, *,
                                        field_name: str,
                                        field_distribution: Dict[str,
                                                                 explorer.NumericalStats],
                                        force_no_log=False,
                                        x_limit=False,
                                        colors=None):
        """
         Draw information of field value distribution for numerical type to
         the report.

         Args:
             notes(str): Explain the block
             field_name (str): data field name
             field_distribution (:dict of :NumericalStats):
                 -key: label_name
                 -value: NumericalStats object

             force_no_log (bool): whether to change y-scale to logrithmic
                                              scale for a more balanced view
             x_limit (list:): whether x-axis only display the required percentile range.
                             If True, field_distribution should have a
                             key "x_limit" and value of [x_min, x_max].
             colors (list): the list of color code for rendering different class
        """
        pass

    @abstractmethod
    def draw_text_field_distribution(self, notes: str, *,
                                     field_name: str,
                                     field_distribution: Dict[str,explorer.TextStats]):
        """
        Draw information of field value distribution for text type to the
        report.

        Args:
            notes(str): Explain the block
            field_name (str): data field name
            field_distribution (:dict of :TextStats):
                -key: label_name
                -value: TextStats object
        """
        pass

    @abstractmethod
    def draw_datetime_field_distribution(self, notes: str, *,
                                         field_name: str,
                                         field_distribution: Dict[str,
                                                                  explorer.DatetimeStats]):
        """
        Draw information of field value distribution for datetime type to the
        report.

        Args:
            notes(str): Explain the block
            field_name (str): data field name
            field_distribution (:dict of :dict):
                -key: label_name
                -value (:dict of :DatetimeStats):
                    Note that in order to render it in 2D diagram, the resolution has to be ['YEAR','MONTH'].
                    - 1st level key: year_X(int)
                    - 1st level value:
                        - 2nd level key: month_X(int)
                        - 2nd level value: count of sample in month_X of year_X
        """
        pass

    ################################################################################
    ###  Feature Section
    ################################################################################
    @abstractmethod
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
        pass

    ################################################################################
    ###  Feature Shap Values
    ################################################################################
    @abstractmethod
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
        pass

    ################################################################################
    ###  Training Section
    ################################################################################
    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    ################################################################################
    ###  Interpreter Section
    ################################################################################
    @abstractmethod
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
        pass


    @abstractmethod
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
        pass

    ################################################################################
    ###  Evaluation Section
    ################################################################################
    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass