from .tabular.lime_tabular_explainer import LimeTabularExplainer
from .text.lime_text_explainer import LimeTextExplainer

DICT_DOMAIN_TO_CLASS = {
    'text': {
        'lime': LimeTextExplainer
    },
    'tabular': {
        'lime': LimeTabularExplainer
    }
}

DICT_DOMAIN_TO_DEFAULT_ALG = {
    'text': 'lime',
    'tabular': 'lime'
}
