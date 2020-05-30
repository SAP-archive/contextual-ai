#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Basic Content - commonly use """


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from xai.formatter.contents.base import Content
from xai.formatter.writer.base import Writer


################################################################################
###  Basic Key Value Pairs
################################################################################
class BasicKeyValuePairs(Content):
    """
    Basic Key-Value pairs info
    """

    def __init__(self, info: list, notes=None) -> None:
        """
        Add key-value pairs information to the report

        Args:
            info (list): list of tuple / list of (list of tuple))
                multi-level rendering, e.g. to display `model_info`
            notes (str, Optional):
                explain the block
        """
        super(BasicKeyValuePairs, self).__init__(info, notes)
        self._info = info
        self._notes = None
        if not (notes is None):
            self._notes = notes

    @property
    def info(self):
        """Returns key-value pairs information."""
        return self._info

    @property
    def notes(self):
        """Returns block description."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Basic Info (key-value pairs) Paragraph

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_basic_key_value_pairs(notes=self.notes, info=self.info)

################################################################################
###  Basic Table
################################################################################
class BasicTable(Content):
    """
    Basic Table
    """

    def __init__(self, table_header: list, table_data: list,
                 col_width: list, notes=None) -> None:
        """
        Add table to the report

        Args:
            table_header (list): list of str
            table_data (list): list of str
            col_width (list): list of float,
                default: None (evenly divided for the whole page width)
            notes (str, Optional):
                explain the block
        """
        super(BasicTable, self).__init__(table_header, table_data, notes)
        self._table_header = table_header
        self._table_data = table_data
        self._col_width = col_width
        self._notes = None
        if not (notes is None):
            self._notes = notes

    @property
    def table_header(self):
        """Returns table header information."""
        return self._table_header

    @property
    def table_data(self):
        """Returns table data information."""
        return self._table_data

    @property
    def col_width(self):
        """Returns column width information."""
        return self._col_width

    @property
    def notes(self):
        """Returns block description."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Basic Table

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_basic_table(notes=self.notes,
                                table_header=self.table_header,
                                table_data=self.table_data,
                                col_width=self.col_width)


################################################################################
###  Basic Image Grid
################################################################################
class BasicImageGrid(Content):
    """
    Basic Image Grid
    """

    def __init__(self, image_list: list, grid_spec: list, notes=None) -> None:
        """
        Add image blocks with formatted grid specification

        Args:
            image_list (list): the list of image_paths
            grid_spec (dict): indicate image size and position
                - key: image_name, or index if image_set is a list
                - value: (x,y,w,h) position and weight/height of image,
                      with left top corner of the block as (0,0), unit in mm
            notes (str, Optional):
                explain the block
        """
        super(BasicImageGrid, self).__init__(image_list, grid_spec, notes)
        self._image_list = image_list
        self._grid_spec = grid_spec
        self._notes = None
        if not (notes is None):
            self._notes = notes

    @property
    def image_list(self):
        """Returns images path information."""
        return self._image_list

    @property
    def grid_spec(self):
        """Returns images size anf position information."""
        return self._grid_spec

    @property
    def notes(self):
        """Returns block description."""
        return self._notes

    def draw(self, writer: Writer):
        """
        Draw Basic Image Grids

        Args:
            writer (Writer): Report Writer
        """
        writer.draw_basic_images_with_grid_spec(notes=self.notes,
                                                image_list=self.image_list,
                                                grid_spec=self.grid_spec)