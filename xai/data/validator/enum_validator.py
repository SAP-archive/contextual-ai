#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from collections import defaultdict

from typing import Dict
from xai.data.exceptions import AttributeNotFound
from xai.data.validator.abstract_validator import AbstractValidator
from xai.data.validator.validation_stats import ValidationStats


class EnumValidator(AbstractValidator):

    def __init__(self, schema: Dict):
        super(EnumValidator, self).__init__(schema=schema)
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

        for feature_name, enum_values in self.schema.items():
            if sample[feature_name] in enum_values:
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
