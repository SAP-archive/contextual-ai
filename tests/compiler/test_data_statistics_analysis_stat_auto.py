#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Data Statistics Analysis Generator Stat auto """

import sys
sys.path.append('../')

import unittest
from xai.compiler import Configuration, Controller


class TestDataStatisticsAnalysisStatAuto(unittest.TestCase):

    def setUp(self) -> None:
        self.json = 'sample_template/data-statistics-analysis_stat-auto.json'

    def test_json_generate_report(self):
        controller = Controller(config=Configuration(self.json))
        controller.render()

if __name__ == '__main__':
    unittest.main()
