#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from collections import defaultdict

from typing import Dict
import math
import numpy as np
from xai.data.exceptions import AttributeNotFound
from xai.data.validator.abstract_validator import AbstractValidator
from xai.data.validator.validation_stats import ValidationStats


class MissingValidator(AbstractValidator):

    def __init__(self, schema: Dict):
        super(MissingValidator, self).__init__(schema=schema)
        self._column_count = defaultdict(int)
        self._total_count = 0

    def validate(self, sample: Dict):
        keys_not_found = list()
        validate_result = dict()
        for feature_name in self.schema.keys():
            if feature_name not in sample:
                keys_not_found.append(feature_name)
        if len(keys_not_found) > 0:
            raise AttributeNotFound(attribute_name=keys_not_found, sample=sample)

        for feature_name, missing_values in self.schema.items():
            x = sample[feature_name]
            if x is None:
                missing = True
            elif type(x) == float and math.isnan(x):
                missing = True
            elif x in missing_values:
                missing = True
            else:
                missing = False

            if missing:
                validate_result[feature_name] = True
                self._column_count[feature_name] += 1
            else:
                validate_result[feature_name] = False

        self._total_count += 1
        return validate_result

    def get_statistics(self) -> ValidationStats:
        stats = ValidationStats()
        stats.update_stats(column_stats=self._column_count, total_count=self._total_count)
        return stats
