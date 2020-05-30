#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
""" Graph Generator """

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xai.constants as Const
from wordcloud import WordCloud
import shap
from xai.graphs.basic_graph import Graph
from typing import List
from collections import Counter
import operator
from xai.data.exceptions import NoItemsError


class ReliabilityDiagram(Graph):
    def __init__(self, figure_path, data, title):
        super(ReliabilityDiagram, self).__init__(file_path=figure_path, data=data, title=title, figure_size=(5, 5),
                                                 x_label="Accuracy",
                                                 y_label="Confidence")

    def draw_core(self):
        prob = np.array(self.data[Const.KEY_PROBABILITY])
        gt = np.array(self.data[Const.KEY_GROUNDTRUTH])

        m = Const.RELIABILITY_BINSIZE
        # process input
        conf = np.max(prob, axis=1)
        pred = np.argmax(prob, axis=1)

        accuracy = np.zeros((prob.shape[0], 1))
        accuracy[np.where(gt == pred)] = 1

        # generate confidence/accuracy
        reliability = []
        for i in range(m):
            lower = 1 / m * i
            upper = 1 / m * (1 + i)
            condition = (conf >= lower) & (conf < upper)
            sample_num = accuracy[condition].shape[0]
            ave_acc = np.sum(accuracy[condition]) / sample_num
            ave_conf = np.mean(conf[condition])
            reliability.append((lower, upper, ave_conf, ave_acc, sample_num))

        for item in reliability:
            lower, upper, conf, acc, sample_num = item
            x = plt.bar(lower, height=acc, width=upper - lower, bottom=0, align='edge', color='b')
            ece = conf - acc
            if ece > 0:
                y = plt.bar(lower, height=conf - acc, width=upper - lower, bottom=acc, align='edge', color='r',
                            alpha=0.5)
            else:
                y = plt.bar(lower, height=acc - conf, width=upper - lower, bottom=conf, align='edge', color='r',
                            alpha=0.5)
        plt.legend((x, y), ('accuracy', 'gap'))


class ReliabilityDiagramForMultiClass(Graph):
    def __init__(self, data, title):
        super(ReliabilityDiagramForMultiClass, self).__init__(data, title, figure_size=(5, 5),
                                                              x_label="Accuracy",
                                                              y_label="Confidence")

    def draw_core(self, current_class_label):
        conf = np.array(self.data[Const.KEY_PROBABILITY])
        gt = np.array(self.data[Const.KEY_GROUNDTRUTH])

        m = Const.RELIABILITY_BINSIZE
        # process input
        accuracy = np.zeros(conf.shape)
        accuracy[np.where(gt == current_class_label)] = 1

        # generate confidence/accuracy
        reliability = []
        for i in range(m):
            lower = 1 / m * i
            upper = 1 / m * (1 + i)
            condition = (conf >= lower) & (conf < upper)
            sample_num = accuracy[condition].shape[0]
            ave_acc = np.sum(accuracy[condition]) / sample_num
            ave_conf = np.mean(conf[condition])
            reliability.append((lower, upper, ave_conf, ave_acc, sample_num))

        for item in reliability:
            lower, upper, conf, acc, sample_num = item
            x = plt.bar(lower, height=acc, width=upper - lower, bottom=0, align='edge', color='b')
            ece = conf - acc
            if ece > 0:
                y = plt.bar(lower, height=conf - acc, width=upper - lower, bottom=acc, align='edge', color='r',
                            alpha=0.5)
            else:
                y = plt.bar(lower, height=acc - conf, width=upper - lower, bottom=conf, align='edge', color='r',
                            alpha=0.5)
        plt.legend((x, y), ('accuracy', 'gap'))
        plt.title('Reliability for Class %s' % current_class_label)


class HeatMap(Graph):
    def __init__(self, figure_path, data, title, x_label=None, y_label=None):
        if len(data) < 3:
            fig_size = (5, 5)
        else:
            fig_size = (10, 10)
        super(HeatMap, self).__init__(file_path=figure_path, data=data, title=title, figure_size=fig_size,
                                      x_label=x_label, y_label=y_label)

    def draw_core(self, x_tick: List[str] = None, y_tick: List[str] = None, color_bar=False, grey_scale=False):
        data = np.array(self.data)
        df_data = pd.DataFrame(data, x_tick, y_tick)
        sns.set(font_scale=1.5)  # label size
        if len(x_tick) > 30:
            annot = False
            annot_kws = None
        elif len(x_tick) > 10:
            annot = True
            annot_kws = {}
        else:
            annot = True
            annot_kws = {"size": 25}
        if grey_scale:
            self.label_ax = sns.heatmap(df_data, annot=annot, annot_kws=annot_kws, fmt='g', cbar=color_bar,
                                        cmap='Greys')  # font size
        else:
            self.label_ax = sns.heatmap(df_data, annot=annot, annot_kws=annot_kws, fmt='g', cbar=color_bar)  # font size


class ResultProbability(Graph):
    def __init__(self, figure_path, data, title):
        super(ResultProbability, self).__init__(file_path=figure_path, data=data, title=title,
                                                figure_size=(6, 6),
                                                x_label='Class',
                                                y_label='Probability')

    def draw_core(self, limit_size=Const.DEFAULT_LIMIT_SIZE):
        prob = np.array(self.data['probability'])
        gt = np.array(self.data['gt'])
        num_sample = len(prob)
        if num_sample > limit_size:
            idx = np.random.rand(num_sample) < limit_size / num_sample
            prob = prob[idx, 1]
            gt = gt[idx]
        else:
            prob = prob[:, 1]

        data_frame = {'predict_prob': prob, 'gt': gt}
        df = pd.DataFrame(data_frame)
        self.label_ax = sns.violinplot(x="gt", y="predict_prob", data=df)


class ResultProbabilityForMultiClass(Graph):
    def __init__(self, figure_path, data, title):
        super(ResultProbabilityForMultiClass, self).__init__(file_path=figure_path, data=data, title=title,
                                                             figure_size=(12, 6),
                                                             x_label='Ground Truth Class',
                                                             y_label='Confidence')

    def draw_core(self, limit_size=Const.DEFAULT_LIMIT_SIZE, TOP_K_CLASS=10):
        conf = np.array(self.data[Const.KEY_PROBABILITY])
        gt = np.array(self.data[Const.KEY_GROUNDTRUTH])
        num_sample = len(conf)
        if num_sample > limit_size:
            idx = np.random.rand(num_sample) < limit_size / num_sample
            conf = conf[idx]
            gt = gt[idx]
        else:
            conf = conf
        dict_counter = dict(Counter(gt))
        sorted_dict_counter = sorted(dict_counter.items(), key=operator.itemgetter(1))[::-1]
        label_top_k = [a for (a, b) in sorted_dict_counter[:TOP_K_CLASS]]
        data_frame = {'predict_prob': conf, 'gt': gt}
        df = pd.DataFrame(data_frame)
        self.label_ax = sns.violinplot(x="gt", y="predict_prob", data=df, order=label_top_k)
        plt.title(self.title)


class KdeDistribution(Graph):
    def __init__(self, figure_path, data, title, x_label=None, y_label=None):
        super(KdeDistribution, self).__init__(file_path=figure_path, data=data, title=title, figure_size=(10, 5),
                                              x_label=x_label, y_label=y_label)

    def draw_core(self, color, force_no_log, x_limit):
        data = self.data
        lrh = data.histogram
        line_data = np.array(data.kde)

        if len(lrh) == 0:
            raise NoItemsError('NumericalStats')

        sum_perc = 0
        max_height = 0
        for i in lrh:
            sum_perc += i[2]
            max_height = max(i[2], max_height)

        perc = [i[2] / sum_perc for i in lrh]

        sorted_perc = sorted(perc)

        x = [i[0] for i in lrh]
        w = [(i[1] - i[0]) * 0.95 for i in lrh]
        h = [i[2] for i in lrh]
        if force_no_log:
            plt.bar(x=x, height=h, width=w, align='edge', color=color)
            plt.plot(line_data[:, 0], line_data[:, 1], color='k')
        else:
            if len(sorted_perc) < 2 or sorted_perc[-1] - sorted_perc[-2] > 0.5:
                plt.bar(x=x, height=h, width=w, align='edge', log=True, color=color)
            else:
                plt.bar(x=x, height=h, width=w, align='edge', color=color)
                plt.plot(line_data[:, 0], line_data[:, 1])
        if x_limit:
            plt.xlim((data.mean - data.sd * 2, data.mean + data.sd * 2))


class EvaluationLinePlot(Graph):
    def __init__(self, figure_path, data, title, x_label=None, y_label=None):
        super(EvaluationLinePlot, self).__init__(file_path=figure_path, data=data, title=title, figure_size=(14, 7),
                                                 x_label=x_label,
                                                 y_label=y_label)

    def draw_core(self, benchmark_metric=None, benchmark_value=None):
        sample_index = list(self.data.keys())
        sample_index = sample_index[0]
        metric_keys = list(self.data[sample_index][Const.KEY_HISTORY_EVALUATION].keys())

        metrics = {metric: [] for metric in metric_keys}

        iterations = []
        for num_iter, history_scores in self.data.items():
            iterations.append(num_iter)
            for metric_key in metric_keys:
                metrics[metric_key].append(history_scores[Const.KEY_HISTORY_EVALUATION][metric_key])

        # plot each metric line
        for idx, metric in enumerate(metric_keys):
            values = metrics[metric]
            ax = sns.pointplot(x=iterations, y=values, color=Const.PLOT_LINE_COLORS[idx], scale=0.5)
        if benchmark_value is not None:
            ax = sns.lineplot(x=iterations, y=[benchmark_value] * len(iterations), color='red', dashes=True)
            ax.lines[-1].set_linestyle("--")
            if benchmark_metric is not None:
                metric_keys.append('benchmark (%s)' % benchmark_metric)

        ax.legend(handles=ax.lines[::len(iterations) + 1], labels=metric_keys, bbox_to_anchor=(1, 1))
        self.label_ax = ax


class FeatureImportance(Graph):
    def __init__(self, figure_path, data, title):
        super(FeatureImportance, self).__init__(file_path=figure_path, data=data, title=title, figure_size=(10, 5),
                                                x_label="Importance Score",
                                                y_label="Features")

    def draw_core(self, limit_length=None, color_palette="Blues_d"):
        if type(self.data) == 'dict':
            data = sorted(self.data.items(), key=lambda kv: int(kv[1]), reverse=True)
        else:
            data = self.data
        if limit_length is not None:
            data = data[:limit_length]

        features = np.array([a for a, _ in data])
        scores = np.array([round(b, 10) for _, b in data])

        ax = sns.barplot(x=scores, y=features, palette=sns.color_palette(color_palette), orient='h')
        for index, score_value in enumerate(scores.tolist()):
            ax.text(score_value, index, score_value, color='black', ha="left")
        plt.autoscale(enable=True, axis='both', tight=True)
        self.label_ax = ax


class FeatureShapValues(Graph):
    def __init__(self, figure_path, shap_values, class_id, title, train_data = None):
        data = dict()
        data['shap_values'] = shap_values
        data['class_id'] = class_id
        data['train_data'] = train_data
        super(FeatureShapValues, self).__init__(file_path=figure_path, data=data, title=title, figure_size=(10, 10),
                                                x_label=None,
                                                y_label=None)

    def draw_core(self, max_display=None):
        feature_shap_values = self.data['shap_values']
        shap_values = np.array([v for _, v in feature_shap_values]).transpose()[self.data['class_id'], ::]
        train_data = self.data['train_data']
        feature_names = [n for n, _ in feature_shap_values]
        shap.summary_plot(shap_values, train_data, feature_names=feature_names, max_display=max_display, show=False)


class WordCloudGraph(Graph):
    def __init__(self, figure_path, data, title):
        super(WordCloudGraph, self).__init__(file_path=figure_path, data=data, title=title, figure_size=(10, 10),
                                             x_label=None, y_label=None)

    def draw_core(self, limit_words=None):
        if limit_words is None:
            limit_words = 200
        wc = WordCloud(background_color="white", max_words=limit_words)
        # generate word cloud
        if type(self.data) == list:
            data = {word: freq for (word, freq) in self.data if freq > 0}
        else:
            data = self.data
        wc.generate_from_frequencies(data)
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")


class DatePlot(Graph):
    def __init__(self, figure_path, data, title, x_label=None, y_label=None):
        figsize = (10, 5)
        super(DatePlot, self).__init__(file_path=figure_path, data=data, title=title, figure_size=figsize,
                                       x_label=x_label, y_label=y_label)

    def draw_core(self):
        data_dist = {k: v for (k, v) in sorted(self.data.items())}
        min_year = list(data_dist.keys())[0]
        max_year = list(data_dist.keys())[-1]

        earliest = (min_year, min([int(month) for month in data_dist[min_year].keys()]))
        latest = (max_year, max([int(month) for month in data_dist[max_year].keys()]))

        line_num = len(data_dist)
        data_frame = []
        for year in data_dist:
            year_data = [0] * 13
            year_data[0] = year
            for month in data_dist[year]:
                year_data[int(month)] = int(data_dist[year][month])
            data_frame.append(year_data)
        data_frame = np.array(data_frame).astype(int)
        bars = []
        colors = ['#1abc9c', '#2ecc71', '#3498db', '#7f8c8d', '#9b59b6', '#34495e', '#f1c40f', '#e67e22', '#e74c3c',
                  '#95a5a6', '#d35400', '#bdc3c7']
        legends = ['Jan', 'Feb', 'Mar', 'April', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        current_sum = np.zeros(line_num)
        for month in range(1, 13):
            p = plt.barh(y=list(range(0, line_num)), width=data_frame[:, month].tolist(), left=current_sum.tolist(),
                         color=colors[month - 1])
            bars.append(p)
            current_sum = data_frame[:, month] + current_sum
        for idx in range(line_num):
            plt.text(current_sum[idx], idx, int(current_sum[idx]), color='black', ha="left")

        plt.yticks(list(range(0, line_num)), list(data_dist.keys()))
        plt.legend(bars, legends, bbox_to_anchor=(1.04, 1), loc="upper left")
        plt.title(
            'Date Range: %s.%s - %s.%s' % (earliest[0], legends[earliest[1] - 1], latest[0], legends[latest[1] - 1]))


class BarPlot(Graph):
    def __init__(self, file_path, data, title, x_label=None, y_label=None):
        figsize = (10, 5)
        super(BarPlot, self).__init__(file_path=file_path, data=data, title=title, figure_size=figsize, x_label=x_label,
                                      y_label=y_label)

    def draw_core(self, caption=None, limit_length=None, color_palette="Blues_d", ratio=False):
        sns.set(font_scale=1)
        data = self.data
        if type(data) == list:
            data = {v: f for v, f in self.data}
        total_amount = sum(self.data.values())
        data = sorted(data.items(), key=lambda kv: int(kv[1]), reverse=True)
        percentage = [v / total_amount for k, v in data]

        if limit_length is not None:
            data = data[:limit_length]
            percentage = percentage[:limit_length]

        items = np.array([a for a, _ in data])
        values = np.array([b for _, b in data])
        ax = sns.barplot(x=values, y=items, palette=sns.color_palette(color_palette), orient='h', order=items)
        if len(data) > 3 and percentage[0] - percentage[1] > 0.3:  # the top item is quite dominant
            xlimit = values[1] * 1.2
            plt.xlim([0, xlimit])
            if ratio:
                ax.text(xlimit, 0, "%s%%" % round(percentage[0] * 100, 2), color='black', ha="left")
            else:
                ax.text(xlimit, 0, round(values[0], 4), color='red', ha="left")
            plt.autoscale(enable=True, axis='y', tight=True)

        else:
            if ratio:
                ax.text(values[0], 0, "%s%%" % round(percentage[0] * 100, 2), color='black', ha="left")
            else:
                ax.text(values[0], 0, round(values[0], 4), color='black', ha="left")
            plt.autoscale(enable=True, axis='both', tight=True)

        for index in range(1, len(values)):
            if ratio:
                ax.text(values[index], index, "%s%%" % round(percentage[index] * 100, 2), color='black', ha="left")
            else:
                ax.text(values[index], index, round(values[index], 4), color='black', ha="left")
        if caption is not None:
            plt.title(caption)
        self.label_ax = ax
