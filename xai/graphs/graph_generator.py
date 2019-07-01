import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import xai.constants as Const
from wordcloud import WordCloud
from xai.graphs.basic_graph import Graph
from typing import List


class ReliabilityDiagram(Graph):
    def __init__(self, data, title):
        super(ReliabilityDiagram, self).__init__(data, title, figure_size=(5, 5),
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


class HeatMap(Graph):
    def __init__(self, data, title, x_label=None, y_label=None):
        if len(data) < 3:
            fig_size = (5, 5)
        elif len(data) < 10:
            fig_size = (10, 10)
        else:
            fig_size = (15, 15)
        super(HeatMap, self).__init__(data, title, figure_size=fig_size, x_label=x_label, y_label=y_label)

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
            self.label_ax = sns.heatmap(df_data, annot=annot, annot_kws=annot_kws, fmt='g', cbar=color_bar, cmap='Greys')  # font size
        else:
            self.label_ax = sns.heatmap(df_data, annot=annot, annot_kws=annot_kws, fmt='g', cbar=color_bar)  # font size


class ResultProbability(Graph):
    def __init__(self, data, title):
        super(ResultProbability, self).__init__(data=data, title=title, figure_size=(6, 6),
                                                x_label='Class',
                                                y_label='Probability')

    def draw_core(self, limit_size=Const.DEFAULT_LIMIT_SIZE):
        prob = np.array(self.data[Const.KEY_PROBABILITY])
        gt = np.array(self.data[Const.KEY_GROUNDTRUTH])
        num_sample = len(prob)
        if num_sample > limit_size:
            idx = np.random.rand(num_sample) < limit_size / num_sample
            prob = prob[idx, 1]
            gt = gt[idx]
        else:
            prob = prob[:, 1]

        data_frame = {'predict_prob': prob, 'gt': gt}
        df = pd.DataFrame(data_frame)
        self.label_ax = sns.swarmplot(x="gt", y="predict_prob", data=df)


class KdeDistribution(Graph):
    def __init__(self, data, title, x_label=None, y_label=None):
        super(KdeDistribution, self).__init__(data=data, title=title, figure_size=(10, 5), x_label=x_label,
                                              y_label=y_label)

    def draw_core(self, color, force_no_log, x_limit):
        data = self.data
        xywh = data['histogram']
        line_data = np.array(data['kde'])

        if len(xywh) == 0:
            print("Error: no values in xywh for current data. %s" % data)
            return

        sum_perc = 0
        max_height = 0
        for i in xywh:
            sum_perc += i[3]
            max_height = max(i[3], max_height)

        perc = [i[3] / sum_perc for i in xywh]

        sorted_perc = sorted(perc)

        x = [i[0] for i in xywh]
        w = [i[2] for i in xywh]
        h = [i[3] for i in xywh]
        if force_no_log:
            plt.bar(x=x, height=h, width=w, align='edge', color=color)
        else:
            if len(sorted_perc) < 2 or sorted_perc[-1] - sorted_perc[-2] > 0.5:
                plt.bar(x=x, height=h, width=w, align='edge', log=True, color=color)
            else:
                plt.bar(x=x, height=h, width=w, align='edge', color=color)
                plt.plot(line_data[:, 0], line_data[:, 1])
        if x_limit:
            plt.xlim(data['x_limit'])


class EvaluationLinePlot(Graph):
    def __init__(self, data, title, x_label=None, y_label=None):
        super(EvaluationLinePlot, self).__init__(data=data, title=title, figure_size=(14, 7), x_label=x_label,
                                                 y_label=y_label)

    def draw_core(self, benchmark_metric, benchmark_value):
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

        ax = sns.lineplot(x=iterations, y=[benchmark_value] * len(iterations), color='red', dashes=True)
        ax.lines[-1].set_linestyle("--")

        metric_keys.append('benchmark (%s)' % benchmark_metric)

        ax.legend(handles=ax.lines[::len(iterations) + 1], labels=metric_keys, bbox_to_anchor=(1, 1))
        self.label_ax = ax


class FeatureImportance(Graph):
    def __init__(self, data, title):
        super(FeatureImportance, self).__init__(data=data, title=title, figure_size=(10, 5), x_label="Importance Score",
                                                y_label="Features")

    def draw_core(self, limit_length=None, color_palette="Blues_d"):
        if type(self.data) == 'dict':
            data = sorted(self.data.items(), key=lambda kv: int(kv[1]), reverse=True)
        if limit_length is not None:
            data = data[:limit_length]

        features = np.array([a for a, _ in data])
        scores = np.array([b for _, b in data])

        plt.figure(figsize=(10, 5))

        ax = sns.barplot(x=scores, y=features, palette=sns.color_palette(color_palette), orient='h')
        for index, score_value in enumerate(scores.tolist()):
            ax.text(score_value, index, score_value, color='black', ha="left")
        plt.autoscale(enable=True, axis='both', tight=True)
        self.label_ax = ax


class WordCloudGraph(Graph):
    def __init__(self, data, title):
        super(WordCloudGraph, self).__init__(data=data, title=title, figure_size=(10, 10), x_label=None, y_label=None)

    def draw_core(self, limit_words=None):
        if limit_words is None:
            limit_words = 200
        wc = WordCloud(background_color="white", max_words=limit_words)
        # generate word cloud
        if type(self.data) == list:
            data = {word: freq for (word, freq) in self.data}
        wc.generate_from_frequencies(data)
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")


class BarPlot(Graph):
    def __init__(self, data, title, x_label=None, y_label=None):
        if len(data) < 5:
            figsize = (6, 3)
        else:
            figsize = (10, 5)
        super(BarPlot, self).__init__(data=data, title=title, figure_size=figsize, x_label=x_label, y_label=y_label)

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
                ax.text(values[0], 0, "%s%%" % round(percentage[0] * 100, 2), color='black', ha="left")
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
