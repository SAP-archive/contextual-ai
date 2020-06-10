# Contextual AI Explainer tutorials

This directory houses the Jupyter notebooks which demonstrate how to use each explanation algorithm
found in :ref:doc:`xai.explainer <explainer/explainer>`.

* :ref:doc:`lime_tabular_explainer.ipynb <tutorials/explainer/tutorial_lime_tabular_explainer>`:
    * Explanation algorithm: [LIME tabular explainer](https://lime-ml.readthedocs.io/en/latest/lime.html#module-lime.lime_tabular)
    * Target model: RandomForest
    * Dataset: Wisconsin breast cancer
    
* :ref:doc:`lime_text_explainer.ipynb <tutorials/explainer/tutorial_lime_text_explainer>`:
    * Explanation algorithm: [LIME text explainer](https://lime-ml.readthedocs.io/en/latest/lime.html#lime.lime_text.LimeTextExplainer)
    * Target model: Naive Bayes
    * Dataset: 20newsgroups
    
* :ref:doc:`lime_text_explainer_with_keras.ipynb <tutorials/explainer/tutorial_lime_text_explainer_with_keras>`:
    * Explanation algorithm: [LIME text explainer](https://lime-ml.readthedocs.io/en/latest/lime.html#lime.lime_text.LimeTextExplainer)
    * Target model: Convolutional Neural Network
    * Dataset: 20newsgroups

* :ref:doc:`shap_tabular_explainer.ipynb <tutorials/explainer/tutorial_shap_tabular_explainer>`:
    * Explanation algorithm: [SHAP kernel explainer](https://shap.readthedocs.io/en/latest/#shap.KernelExplainer)
    * Target model: RandomForest
    * Dataset: Wisconsin breast cancer
