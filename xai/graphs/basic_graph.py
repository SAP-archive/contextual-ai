#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import os
from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from typing import Tuple


################################################################################
### Graph
################################################################################
class Graph(ABC):
    def __init__(self, file_path, data, title: str,
                 figure_size: Tuple[int, int], x_label: str = None,
                 y_label: str = None):
        """
        initialize the graph
        Args:
            file_path (str): figure path to save the generated plot
            data: data used to render the plot, extended classes need to define the data type
            title (str): figure title render on the plot
            figure_size (tuple): figure size in terms of width and height
            x_label (str): x-axis label for the figure
            y_label (str): y-axis label for the figure
        """
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.data = data
        self.figure_size = figure_size
        self.file_path = file_path
        self.label_ax = None

    def draw(self, **kwargs):
        """generate the plot and save to the figure
        """
        if self.figure_size is not None:
            f = plt.figure(figsize=self.figure_size)

        self.draw_core(**kwargs)

        if self.x_label is not None:
            if self.label_ax is None:
                plt.xlabel(xlabel=self.x_label)
            else:
                self.label_ax.set_xlabel(self.x_label)

        if self.y_label is not None:
            if self.label_ax is None:
                plt.xlabel(xlabel=self.x_label)
            else:
                self.label_ax.set_xlabel(self.x_label)

        plt.tight_layout()
        n = 0
        while os.path.exists(self.file_path):
            n+=1
            filename = os.path.splitext(self.file_path)
            self.file_path = '%s_%s.%s' % (filename[0], n, filename[1])
        plt.savefig(self.file_path, transparent=False, bbox_inches='tight')
        plt.close(fig=f)

        return self.file_path

    @abstractmethod
    def draw_core(self, **kwargs):
        '''
        draw images
        :param kwargs:
        :return: image_path
        '''
        raise NotImplementedError("Derived class should implement this")
