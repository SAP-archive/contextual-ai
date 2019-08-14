from xai.explainer.lime_tabular_explainer import LimeTabularExplainer

DEFAULT_ALGORITHM = 'lime'
DICT_DOMAIN_TO_CLASS = {
    'text': {
        DEFAULT_ALGORITHM: ''
    },
    'tabular': {
        DEFAULT_ALGORITHM: LimeTabularExplainer
    }
}
