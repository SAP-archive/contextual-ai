#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from xai.formatter.contents.base import (
    Content,
    NewPage,
    Header,
    Title,
    SectionTitle,
    Paragraph,
    ParagraphTitle
)
from xai.formatter.contents.basic import (
    BasicKeyValuePairs,
    BasicImageGrid,
    BasicTable
)
from xai.formatter.contents.data import (
    DataMissingValue,
    DataSetDistribution,
    DataAttributes,
    CategoricalFieldDistribution,
    NumericFieldDistribution,
    TextFieldDistribution,
    DateTimeFieldDistribution,
)
from xai.formatter.contents.evaluation import (
    MultiClassEvaluationMetricResult,
    BinaryClassEvaluationMetricResult,
    ConfusionMatrixResult,
    MultiClassConfidenceDistribution,
    BinaryClassConfidenceDistribution,
    BinaryClassReliabilityDiagram
)
from xai.formatter.contents.feature import (
    FeatureImportance,
    FeatureShapValues
)
from xai.formatter.contents.model import (
    ModelInterpreter,
    ErrorAnalysis
)
from xai.formatter.contents.summary import (
    TrainingTiming,
    DataSetSummary,
    EvaluationResultSummary,
    ModelInfoSummary
)
from xai.formatter.contents.training import (
    HyperParameterTuning,
    LearningCurve
)
