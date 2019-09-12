from .constants import DOMAIN, ALG
from .tabular.lime_tabular_explainer import LimeTabularExplainer
from .tabular.shap_tabular_explainer import SHAPTabularExplainer
from .text.lime_text_explainer import LimeTextExplainer

DICT_DOMAIN_TO_CLASS = {
    DOMAIN.TEXT: {
        ALG.LIME: LimeTextExplainer
    },
    DOMAIN.TABULAR: {
        ALG.LIME: LimeTabularExplainer,
        ALG.SHAP: SHAPTabularExplainer
    }
}

DICT_DOMAIN_TO_DEFAULT_ALG = {
    DOMAIN.TEXT: ALG.LIME,
    DOMAIN.TABULAR: ALG.LIME
}
