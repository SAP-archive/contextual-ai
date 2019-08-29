# XAI Explainer Module

This module houses all algorithms which are used to generate explanations for model predictions.

### Development

If you are developing your own XAI-compatible explanation algorithm, you should do the following:
* Extend the `AbstractExplainer` found in [abstract_explainer.py](abstract_explainer.py) and implement
all the abstract methods.
* Assign a particular domain to your explanation algorithm as well as a unique name. Place the module
in the appropriate directory (e.g. `xai/explainer/tabular`) and create constants accordingly in
[constants.py](constants.py).
* Map the domain to your algorithm in [config.py](config.py).
* Create unittests in the [tests](../tests) directory.
