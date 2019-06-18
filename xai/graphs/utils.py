from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from xai import constants

def adjust_xtick_labels(ticks_length):
    ticks_params = dict()
    if ticks_length < 5:
        ticks_params['rotation'] = 0
        ticks_params['fontsize'] = 20
    elif ticks_length < 10:
        ticks_params['rotation'] = 15
        ticks_params['fontsize'] = 18
    elif ticks_length < 20:
        ticks_params['rotation'] = 30
        ticks_params['fontsize'] = 16
    else:
        ticks_params['rotation'] = 90
        ticks_params['fontsize'] = 16
    return ticks_params


def adjust_ytick_labels(ticks_length):
    ticks_params = dict()
    if ticks_length < 5:
        ticks_params['fontsize'] = 20
    elif ticks_length < 10:
        ticks_params['fontsize'] = 18
    elif ticks_length < 15:
        ticks_params['fontsize'] = 16
    else:
        ticks_params['fontsize'] = 14
    return ticks_params


def make_ticklabels_invisible(fig):
    for i, ax in enumerate(fig.axes):
        ax.tick_params(labelbottom=False, labelleft=False)
        ax.grid(False)


def dimreduce_visualization(data, mode='pca'):
    if mode == 'tsne':
        tsne = TSNE(n_components=2)
        d_data = tsne.fit_transform(data)
    else:
        pca = PCA(n_components=2)
        d_data = pca.fit_transform(data)
    return d_data

def map_code_to_text_metric(metric_code):
    for text, value_codes in constants.METRIC_MAPPING.items():
        if metric_code in value_codes:
            return text

