from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from IPython.display import display, Markdown


class NotebookPlots:

    @classmethod
    def plot_categorical_stats(cls, stats, feature_column):
        plt.hbar(height=stats.frequency_count.values(), x=stats.frequency_count.keys())
        plt.ylabel(feature_column)
        plt.show()

    @classmethod
    def plot_labelled_categorical_stats(cls, labelled_stats, all_stats, label_column, feature_column):
        y = list(all_stats.frequency_count.keys())
        counter = Counter({label: 0 for label in y})
        legends = []
        plots = []

        for _class, _stats in labelled_stats.items():
            frequency = _stats.frequency_count
            left = [dict(counter)[key] for key in y]
            height = [frequency[key] for key in y]
            p = plt.hbar(width=height, y=y, left=left)
            counter.update(Counter(frequency))
            legends.append(_class)
            plots.append(p)
        plt.legend(plots, legends)
        plt.title('Distribution: %s - %s' % (label_column, feature_column))
        plt.ylabel(feature_column)
        plt.show()

        plt.hbar(width=all_stats.frequency_count.values(), y=all_stats.frequency_count.keys())
        plt.title('All Distribution - %s' % feature_column)
        plt.ylabel(feature_column)
        plt.show()

    @classmethod
    def plot_numerical_stats(cls, _stats, feature_column):
        labelled_stats_table = []
        plt.figure(figsize=(16, 4))
        plt.subplot(121)
        hist = _stats.histogram
        x = [i[0] for i in hist]
        w = [(i[1] - i[0]) for i in hist]
        h = [i[2] for i in hist]
        x_ticks = ["%.2f-%.2f" % (i[0], i[1]) for i in hist[1:-1]]
        x_tick_locs = [(i[0] + i[1]) * 0.5 for i in hist[1:-1]]
        plt.xticks(x_tick_locs, x_ticks, rotation=45)

        plt.bar(x=x, height=h, width=w, align='edge', alpha=0.4)
        labelled_stats_table.append(
            {'min': _stats.min, 'max': _stats.max, 'mean': _stats.mean, 'median': _stats.sd,
             'sd': _stats.max, 'total_count': _stats.total_count})
        plt.title('Distribution: %s' % (feature_column))
        plt.xlabel(feature_column)

        plt.subplot(122)
        kde = np.array([[x, y] for (x, y) in _stats.kde])

        plt.plot(kde[:, 0], kde[:, 1], '--')
        plt.title('KDE: %s' % feature_column)

        plt.show()

        _stats_df = pd.DataFrame.from_records(labelled_stats_table)
        display(_stats_df)

    @classmethod
    def plot_labelled_numerical_stats(cls, labelled_stats, all_stats, label_column, feature_column):
        display(Markdown('### %s' % feature_column))
        labelled_stats_table = []
        plt.figure(figsize=(16, 4))
        plt.subplot(131)
        legends = []
        plots = []
        for _class, _stats in labelled_stats.items():
            hist = _stats.histogram
            x = [i[0] for i in hist]
            w = [(i[1] - i[0]) for i in hist]
            h = [i[2] for i in hist]
            p = plt.bar(x=x, height=h, width=w, align='edge', alpha=0.4)
            legends.append(_class)
            plots.append(p)
            labelled_stats_table.append(
                {'class': _class, 'min': _stats.min, 'max': _stats.max, 'mean': _stats.mean, 'median': _stats.sd,
                 'sd': _stats.max, 'total_count': _stats.total_count})
        plt.legend(plots, legends)
        plt.title('Distribution: %s - %s' % (label_column, feature_column))
        plt.xlabel(feature_column)
        plt.subplot(132)

        hist = all_stats.histogram
        x = [i[0] for i in hist]
        w = [(i[1] - i[0]) * 0.9 for i in hist]
        h = [i[2] for i in hist]
        x_ticks = ["%.2f-%.2f" % (i[0], i[1]) for i in hist]
        x_tick_locs = [(i[0] + i[1]) * 0.5 for i in hist]
        plt.bar(x=x, height=h, width=w, align='edge', alpha=0.8)
        plt.xticks(x_tick_locs, x_ticks, rotation=90)
        plt.title('All Distribution')
        plt.xlabel(feature_column)
        labelled_stats_table.append(
            {'class': 'all', 'min': all_stats.min, 'max': all_stats.max, 'mean': all_stats.mean, 'median': all_stats.sd,
             'sd': all_stats.max, 'total_count': all_stats.total_count})
        plt.subplot(133)

        legends = []
        plots = []
        for _class, _stats in labelled_stats.items():
            kde = np.array([[x, y] for (x, y) in _stats.kde])
            plt.plot(kde[:, 0], kde[:, 1])
            legends.append(_class)
            plots.append(p)
        plt.xlabel(feature_column)

        kde = np.array([[x, y] for (x, y) in all_stats.kde])
        plt.plot(kde[:, 0], kde[:, 1], '--')
        legends.append('all')
        plt.legend(legends)
        plt.title('KDE: %s - %s' % (label_column, feature_column))

        plt.show()

        _stats_df = pd.DataFrame.from_records(labelled_stats_table)
        display(_stats_df)

    @classmethod
    def plot_correlation_heatmap(self, types, values):
        plt.figure(figsize=(12, 12))
        type_enums = np.unique(types.values)
        for type_enum in type_enums:
            display(Markdown('#### Correlation Type: %s' % type_enum))
            heat_map = values[types == type_enum]
            sns.heatmap(heat_map, annot=False, fmt='g', cbar=True, cmap='YlGnBu')

    @classmethod
    def plot_feature_importance_ranking(cls, feature_importance_ranking):
        plt.figure(figsize=(12, 8))

        features = np.array([a for a, _ in feature_importance_ranking])
        scores = np.array([b for _, b in feature_importance_ranking])

        ax = sns.barplot(x=scores, y=features, palette=sns.color_palette("Blues_d"), orient='h')
        plt.autoscale(enable=True, axis='both', tight=True)
        plt.show()
