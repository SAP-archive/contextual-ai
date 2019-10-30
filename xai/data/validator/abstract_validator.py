#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import Iterator, Dict
from abc import ABC, abstractmethod


class AbstractValidator(ABC):

    def __init__(self, schema: Dict):
        self.schema = schema

    @abstractmethod
    def validate(self, sample: Dict) -> Dict:
        raise NotImplementedError('The derived helper needs to implement it.')

    def validate_all(self, sample_list: Iterator[dict]):
        result = []
        for item in sample_list:
            result.append(self.validate(item))

    def get_statistics(self):
        raise NotImplementedError('The derived helper needs to implement it.')
