# XAI Model Interpreter Module

This module provides feature analysis and model interpretation functions.


## Feature Interpreter

`FeatureInterpreter` is a class that helps to generate the following information:
- feature distribution based on feature types
- feature correlation based on feature types
- feature importance ranking for a trained model


## Model Interpreter

`ModelInterpreter` is a class that helps to understand the model performance with a model-agnostic explainer by aggregating 
explanation either (1) on training sample to interpret the model, or (2) on validation samples for error analysis.