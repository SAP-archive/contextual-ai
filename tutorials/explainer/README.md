# XAI Explainer tutorials

This directory houses the Jupyter notebooks which demonstrate how to use each explanation algorithm
found in `xai/explainer`.

* [lime_tabular_explainer.ipynb](lime_tabular_explainer.ipynb):
    * Explanation algorithm: [LIME tabular explainer](https://lime-ml.readthedocs.io/en/latest/lime.html#module-lime.lime_tabular)
    * Target model: RandomForest
    * Dataset: Wisconsin breast cancer
    
* [lime_text_explainer.ipynb](lime_text_explainer.ipynb):
    * Explanation algorithm: [LIME text explainer](https://lime-ml.readthedocs.io/en/latest/lime.html#lime.lime_text.LimeTextExplainer)
    * Target model: Naive Bayes
    * Dataset: 20newsgroups
    
* [shap_tabular_explainer.ipynb](shap_tabular_explainer.ipynb):
    * Explanation algorithm: [SHAP kernel explainer](https://shap.readthedocs.io/en/latest/#shap.KernelExplainer)
    * Target model: RandomForest
    * Dataset: Wisconsin breast cancer
