#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import List, Dict
from xai.data.abstract_stats import AbstractStats
from xai.data.constants import STATSKEY


class ValidationStats(AbstractStats):
    def __init__(self):
        super(ValidationStats).__init__()
        self.column_stats = None
        self.total_count = 0

    def update_stats(self, column_stats, total_count):
        self.column_stats = column_stats
        self.total_count = total_count

    def to_json(self) -> List[Dict]:
        json_obj = dict()
        json_obj[STATSKEY.TOTAL_COUNT] = self.total_count
        json_obj[STATSKEY.DISTRIBUTION] = list()
        for feature_name, count in self.column_stats.items():
            json_column_obj = dict()
            json_column_obj['field'] = feature_name
            json_column_obj['count'] = count
            json_obj[STATSKEY.DISTRIBUTION].append(json_column_obj)

        return json_obj
