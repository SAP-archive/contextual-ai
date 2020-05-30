# Model Module

This module provides feature analysis and model interpretation functions.


<span style="font-size:1.5em;font-weight: bold;">Feature Interpreter</span>

:py:meth:`FeatureInterpreter <model.interpreter.feature_interpreter.FeatureInterpreter>` is a class 
that helps to generate the following information:
- feature distribution based on feature types
- feature correlation based on feature types
- feature importance ranking for a trained model



<span style="font-size:1.5em;font-weight: bold;">Model Interpreter</span>

:py:meth:`ModelInterpreter <model.interpreter.model_interpreter.ModelInterpreter>` is a class 
that helps to understand the model performance with a model-agnostic explainer by aggregating 
explanation either 
- on training sample to interpret the model, or 
- on validation samples for error analysis.