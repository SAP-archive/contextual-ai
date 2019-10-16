#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Data Statistics Analysis Generator NZa """

import sys
sys.path.append('../')

import unittest
from xai.compiler import Configuration, Controller
from tests.compiler.util import prepare_template, remove_temp


class TestDataStatisticsAnalysisNZa(unittest.TestCase):

    def setUp(self) -> None:
        self.json = prepare_template(
            filename='data-statistics-analysis_nza.json')

    def tearDown(self) -> None:
        remove_temp()

    def test_json_generate_report(self):
        controller = Controller(config=Configuration(self.json))
        controller.render()

if __name__ == '__main__':
    unittest.main()
