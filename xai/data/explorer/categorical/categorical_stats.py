#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import Dict

from xai.data.abstract_stats import AbstractStats
from xai.data.constants import STATSKEY
from xai.data.exceptions import InvalidTypeError


class CategoricalStats(AbstractStats):
    """
    CategoricalStats contains following basic information:
        - _total_count: total count of values
        - _frequency_count: a dictionary maps categorical value to its frequency count
    """

    def __init__(self, frequency_count: Dict[str or int, int]):
        super(CategoricalStats).__init__()
        self._frequency_count = frequency_count

    @property
    def frequency_count(self):
        return self._frequency_count

    @frequency_count.setter
    def frequency_count(self, frequency: Dict[str, int]):
        if type(frequency) != dict:
            raise InvalidTypeError('frequency_count', type(frequency), '<dict>')
        for key, value in self._frequency_count.items():
            if type(key) not in [str, int]:
                raise InvalidTypeError('frequency_count:key', type(key), '<str> or <int>')
            if type(value) != int:
                raise InvalidTypeError('frequency_count:value', type(value), '<int>')
        self._frequency_count = frequency
        self._total_count = sum(list(self._frequency_count.values()))

    def to_json(self) -> Dict:
        """
        Map stats information into a json object

        Returns:
            A json that represents frequency count and total count
        """

        json_obj = dict()
        json_obj[STATSKEY.TOTAL_COUNT] = self._total_count
        json_obj[STATSKEY.DISTRIBUTION] = []

        for attribute_name, attribute_count in self._frequency_count.items():
            json_obj[STATSKEY.DISTRIBUTION].append({STATSKEY.DISTRIBUTION_KEY.ATTRIBUTE_NAME: attribute_name,
                                                    STATSKEY.DISTRIBUTION_KEY.ATTRIBUTE_COUNT: attribute_count})

        return json_obj
