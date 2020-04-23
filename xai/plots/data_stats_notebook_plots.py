from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from IPython.display import display, Markdown


class NotebookPlots:

    @classmethod
    def plot_categorical_stats(cls, stats, feature_column):
        plt.barh(width=list(stats.frequency_count.values()), y=list(stats.frequency_count.keys()))
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
            p = plt.barh(width=height, y=y, left=left)
            counter.update(Counter(frequency))
            legends.append(_class)
            plots.append(p)
        plt.legend(plots, legends)
        plt.title('Distribution: %s - %s' % (label_column, feature_column))
        plt.ylabel(feature_column)
        plt.show()

        plt.barh(width=list(all_stats.frequency_count.values()), y=list(all_stats.frequency_count.keys()))
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

    @classmethod
    def plot_feature_shap_values(cls, feature_shap_values, class_id, X_train = None):
        feature_name = [n for n, _ in feature_shap_values]
        shap_values = np.array([v for _, v in feature_shap_values]).transpose()
        import shap
        shap.summary_plot(shap_values[class_id, ::], X_train, feature_names=feature_name)

    @classmethod
    def plot_labelled_text_stats(cls, labelled_stats, all_stats):
        import operator
        labelled_stats_table = []

        for _class in list(labelled_stats.keys())[:5]:
            record = {'class': _class}
            _stats = labelled_stats[_class]
            record['total count'] = _stats.total_count
            plt.figure(figsize=(16, 4))
            plt.subplot(121)
            tfidf = sorted(_stats.tfidf.items(), key=operator.itemgetter(1), reverse=True)[:20]
            words = [item[0] for item in tfidf][::-1]
            scores = [item[1] for item in tfidf][::-1]
            plt.barh(width=scores, y=words)
            plt.title('Average TFIDF\nclass:%s' % _class)
            plt.subplot(122)
            tf = sorted(_stats.term_frequency.items(), key=operator.itemgetter(1), reverse=True)[:20]
            words = [item[0] for item in tf][::-1]
            count = [item[1] for item in tf][::-1]
            plt.barh(width=count, y=words)
            plt.title('Overall Term Frequency\nclass: %s' % _class)
            for pattern, count in _stats.pattern_stats.items():
                record['%s (term count)' % pattern] = count[0]
                record['%s (doc count)' % pattern] = count[1]
            record['longest doc'] = max(list(_stats.word_count.keys()))
            labelled_stats_table.append(record)

        plt.figure(figsize=(16, 4))
        plt.subplot(121)
        tfidf = sorted(all_stats.tfidf.items(), key=operator.itemgetter(1), reverse=True)[:20]
        words = [item[0] for item in tfidf][::-1]
        scores = [item[1] for item in tfidf][::-1]
        plt.barh(width=scores, y=words)
        plt.title('Average TFIDF\nall class')
        plt.subplot(122)
        tf = sorted(all_stats.term_frequency.items(), key=operator.itemgetter(1), reverse=True)[:20]
        words = [item[0] for item in tf][::-1]
        count = [item[1] for item in tf][::-1]
        plt.barh(width=count, y=words)
        plt.title('Overall Term Frequency\nall class')
        plt.show()
        record = {'class': 'all'}
        record['total count'] = all_stats.total_count
        for pattern, count in all_stats.pattern_stats.items():
            record['%s (term count)' % pattern] = count[0]
            record['%s (doc count)' % pattern] = count[1]
        record['longest doc'] = max(list(all_stats.word_count.keys()))
        labelled_stats_table.append(record)

        _stats_df = pd.DataFrame.from_records(labelled_stats_table)
        display(_stats_df)
