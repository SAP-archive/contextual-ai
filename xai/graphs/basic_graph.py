from abc import ABC, abstractmethod
import xai.constants as Const
import matplotlib.pyplot as plt
from typing import Tuple


class Graph(ABC):
    def __init__(self, data, title: str, figure_size: Tuple[int, int], x_label: str = None, y_label: str = None):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.data = data
        self.figure_size = figure_size
        self.file_path = '%s/%s.png' % (Const.FIGURE_PATH, self.title.replace('/', '-'))
        self.label_ax = None

    def draw(self, **kwargs):
        if self.figure_size is not None:
            f = plt.figure(figsize=self.figure_size)

        self.draw_core(**kwargs)

        if self.label_ax is None:
            plt.xlabel(xlabel=self.x_label)
            plt.ylabel(ylabel=self.y_label)
        else:
            self.label_ax.set_xlabel(self.x_label)
            self.label_ax.set_ylabel(self.y_label)
        plt.tight_layout()
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
