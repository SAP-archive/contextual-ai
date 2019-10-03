#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Data Content  """

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from typing import Tuple, Dict

from xai.data import explorer
from xai.formatter.contents.base import Content
from xai.formatter.writer.base import Writer


################################################################################
###  Data Missing Content
################################################################################
class DataMissingValue(Content):
    """
    Missing Data Value
    """

    def __init__(self,
                 missing_count: dict, total_count: dict,
                 ratio=False, notes=None) -> None:
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
            notes (str, Optional): explain the block
        """
        super(DataMissingValue, self).__init__(missing_count, total_count,
                                               ratio, notes)
        self._missing_count = missing_count
        self._total_count = total_count
        self._ratio = ratio
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "This section shows the percentage of sample data with missing values."

    @property
    def missing_count(self):
        """Returns missing data count number."""
        return self._missing_count

    @property
    def total_count(self):
        """Returns total data count number."""
        return self._total_count

    @property
    def ratio(self):
        """Returns missing data ratio."""
        return self._ratio

    @property
    def notes(self):
        """Returns missing data info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Missing Data Value

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_data_missing_value(notes=self.notes,
                                       missing_count=self.missing_count,
                                       total_count=self.total_count,
                                       ratio=self.ratio)

################################################################################
###  Data Set Distribution
################################################################################
class DataSetDistribution(Content):
    """
    DataSet Distribution
    """

    def __init__(self,
                 dataset_distribution: Tuple[str, explorer.CategoricalStats],
                 max_class_shown=20,
                 notes=None) -> None:
        """
        add information of distribution on data set to the report

        Args:
            dataset_distribution (tuple: (str,dict)):
                - tuple[0] str: label/split name
                - tuple[1] CategoricalStats object: `frequency_count` attribute
                                 key - class_name/split_name,
                                 value - class_count/split_count
            max_class_shown (int, Optional): maximum number of classes shown
            in the figure, default is 20
            notes (str, Optional):
                explain the block
        """
        super(DataSetDistribution, self).__init__(dataset_distribution,
                                                  max_class_shown, notes)
        self._dataset_distribution = dataset_distribution
        self._max_class_shown = max_class_shown
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "This section shows the distribution of dataset on the label/split."

    @property
    def dataset_distribution(self):
        """Returns data set distribution."""
        return self._dataset_distribution

    @property
    def max_class_shown(self):
        """Returns maximum number of classes shown."""
        return self._max_class_shown

    @property
    def notes(self):
        """Returns dataset distribution info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Data Set Distribution

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_data_set_distribution(notes=self.notes,
                                          data_set_distribution=self.dataset_distribution,
                                          max_class_shown=self.max_class_shown)

################################################################################
###  Data Attributes
################################################################################
class DataAttributes(Content):
    """
    Data Attributes
    """
    def __init__(self,
                 data_attribute: Dict, notes=None) -> None:
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
        super(DataAttributes, self).__init__(data_attribute, notes)
        self._data_attribute = data_attribute
        if not (notes is None):
            self._notes = notes
        else:
            self._notes = "This section shows the attributes of fields in the dataset."

    @property
    def data_attribute(self):
        """Returns data attribute."""
        return self._data_attribute


    @property
    def notes(self):
        """Returns data attributes info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Data Attributes

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_data_attributes(notes=self.notes,
                                    data_attribute=self.data_attribute)

################################################################################
###  Categorical Field Distribution
################################################################################
class CategoricalFieldDistribution(Content):
    """
    Categorical Field Distribution
    """
    def __init__(self, field_name: str,
                 field_distribution: Dict[str, explorer.CategoricalStats],
                max_values_display=20, colors=None, notes=None) -> None:
       """
       add information of field value distribution for categorical type to the report.
       Details see analyzers inside `xai.data_explorer.categorical_analyzer`

       Args:
           field_name (str): data field name
           field_distribution (:dict of :dict):
               -key: label_name
               -value: frequency distribution under the `label_name`(dict)
                   - key: label_name
                   - value: CategoricalStats object
           max_values_display (int): maximum number of values displayed
           colors (list): the list of color code for rendering different class
           notes (str, Optional):
               explain the block
       """
       super(CategoricalFieldDistribution, self).__init__(field_name,
                                                          field_distribution,
                                                          max_values_display,
                                                          colors,
                                                          notes)
       self._field_name = field_name
       self._field_distribution = field_distribution
       self._max_values_display = max_values_display
       self._colors = colors
       if not (notes is None):
           self._notes = notes
       else:
           self._notes = "Distribution for %s" % self.field_name

    @property
    def field_name(self):
        """Returns field name."""
        return self._field_name

    @property
    def field_distribution(self):
        """Returns field distribution."""
        return self._field_distribution

    @property
    def max_values_display(self):
        """Returns max values display."""
        return self._max_values_display

    @property
    def colors(self):
        """Returns color code list."""
        return self._colors

    @property
    def notes(self):
        """Returns categorical field distribution info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Categorical Field Distribution

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_categorical_field_distribution(field_name=self.field_name,
                                                   field_distribution=self.field_distribution,
                                                   max_values_display=self.max_values_display,
                                                   colors=self.colors,
                                                   notes=self.notes)

################################################################################
###  Numeric Field Distribution
################################################################################
class NumericFieldDistribution(Content):
    """
    Numeric Field Distribution
    """
    def __init__(self, field_name: str,
                 field_distribution: Dict[str, explorer.NumericalStats],
                 force_no_log=False, x_limit=False, colors=None,
                 notes=None) -> None:
        """
        add information of field value distribution for numerical type to the report.
        Details see analyzers inside `xai.data_explorer.numerical_analyzer`

        Args:
            field_name (str): data field name
            field_distribution (:dict of :NumericalStats):
                -key: label_name
                -value: NumericalStats

            force_no_log (bool): whether to change y-scale to logrithmic
                                               scale for a more balanced view
            x_limit (list:): whether x-axis only display the required percentile range.
                            If True, field_distribution should have a key "x_limit"
                            and value of [x_min, x_max].
            colors (list): the list of color code for rendering different class
            notes (str, Optional): explain the block
        """
        super(NumericFieldDistribution, self).__init__(field_name,
                                                       field_distribution,
                                                       force_no_log,
                                                       x_limit,
                                                       colors,
                                                       notes)
        self._field_name = field_name
        self._field_distribution = field_distribution
        self._force_no_log = force_no_log
        self._x_limit = x_limit
        self._colors = colors
        if not (notes is None):
           self._notes = notes
        else:
           self._notes = "Distribution for %s" % self.field_name

    @property
    def field_name(self):
        """Returns field name."""
        return self._field_name

    @property
    def field_distribution(self):
        """Returns field distribution."""
        return self._field_distribution

    @property
    def force_no_log(self):
        """Returns whether to change y-scale to logrithmic."""
        return self._force_no_log

    @property
    def x_limit(self):
        """Returns whether x-axis only display percentile range."""
        return self._x_limit

    @property
    def colors(self):
        """Returns color code list."""
        return self._colors

    @property
    def notes(self):
        """Returns numeric field distribution info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Numeric Field Distribution

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_numeric_field_distribution(field_name=self.field_name,
                                               field_distribution=self.field_distribution,
                                               force_no_log=self.force_no_log,
                                               x_limit=self.x_limit,
                                               colors=self.colors,
                                               notes=self.notes)

################################################################################
###  Text Field Distribution
################################################################################
class TextFieldDistribution(Content):
    """
    Text Field Distribution
    """
    def __init__(self, field_name: str,
                 field_distribution: Dict[str,explorer.TextStats],
                 notes=None) -> None:
        """
            add information of field value distribution for text type to the report.
            Details see analyzers inside `xai.data_explorer.text_analyzer`

            Args:
                field_name (str): data field name
                field_distribution (:dict of :dict):
                    -key: label_name
                    -value: TextStats object
                notes (str, Optional):  explain the block
        """
        super(TextFieldDistribution, self).__init__(field_name,
                                                    field_distribution,
                                                    notes)
        self._field_name = field_name
        self._field_distribution = field_distribution
        if not (notes is None):
           self._notes = notes
        else:
           self._notes = "Distribution for %s" % self.field_name

    @property
    def field_name(self):
        """Returns field name."""
        return self._field_name

    @property
    def field_distribution(self):
        """Returns field distribution."""
        return self._field_distribution

    @property
    def notes(self):
        """Returns text field distribution info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Text Field Distribution

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_text_field_distribution(field_name=self.field_name,
                                            field_distribution=self.field_distribution,
                                            notes=self.notes)

################################################################################
###  Date Time Field Distribution
################################################################################
class DateTimeFieldDistribution(Content):
    """
    Date Time Field Distribution
    """
    def __init__(self, field_name: str,
                 field_distribution: Dict[str, explorer.DatetimeStats],
                 notes=None) -> None:
        """
        add information of field value distribution for datetime type to the report.
        Details see analyzers inside `xai.data_explorer.datetime_analyzer`

        Args:
            field_name (str): data field name
            field_distribution (:dict of :dict):
                -key: label_name
                -value (:dict of :DatetimeStats):
                    Note that in order to render it in 2D diagram, the resolution has to be ['YEAR','MONTH'].
                    - 1st level key: year_X(int)
                    - 1st level value:
                        - 2nd level key: month_X(int)
                        - 2nd level value: count of sample in month_X of year_X
            notes (str, Optional):
                explain the block
        """
        super(DateTimeFieldDistribution, self).__init__(field_name,
                                                    field_distribution,
                                                    notes)
        self._field_name = field_name
        self._field_distribution = field_distribution
        if not (notes is None):
           self._notes = notes
        else:
           self._notes = "Distribution for %s" % self.field_name

    @property
    def field_name(self):
        """Returns field name."""
        return self._field_name

    @property
    def field_distribution(self):
        """Returns field distribution."""
        return self._field_distribution

    @property
    def notes(self):
        """Returns date time field distribution info."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Date Time Field Distribution

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_datetime_field_distribution(field_name=self.field_name,
                                                field_distribution=self.field_distribution,
                                                notes=self.notes)
