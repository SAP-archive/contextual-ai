#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Data Statistics Analysis Generator """

import sys
sys.path.append('../')

import unittest
from xai.compiler import Configuration, Controller
from tests.compiler.util import prepare_template, remove_temp


class TestDataStatisticsAnalysis(unittest.TestCase):
    """
    Test case: Create Report with ONLY Data Analysis (p1)
    """

    def setUp(self) -> None:
        """ Specify Config Files """
        self.json = prepare_template(filename='data-statistics-analysis.json')
        self.yaml = prepare_template(filename='data-statistics-analysis.yml')

    def tearDown(self) -> None:
        """ Remove working temp files """
        remove_temp()

    def test_json_generate_report(self):
        """ Test report rendering with json config file """
        controller = Controller(config=Configuration(self.json))
        controller.render()

    def test_yaml_generate_report(self):
        """ Test report rendering with yaml config file """
        controller = Controller(config=Configuration(self.yaml))
        controller.render()

if __name__ == '__main__':
    unittest.main()
