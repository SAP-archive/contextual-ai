#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Data Statistics Analysis Generator NZa """

import sys
sys.path.append('../')

import warnings

import unittest
from xai.compiler import Configuration, Controller
from tests.compiler.util import prepare_template, remove_temp


class TestDataStatisticsAnalysisNZa(unittest.TestCase):
    """
    Test case: Create Report using nza dataset with ONLY Data Analysis (p1)
    - refer to README in sample_input for more info on dataset
    - please update the config to include other feature in p1
    """

    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        """ Specify Config Files """
        self.json = prepare_template(
            filename='data-statistics-analysis_nza.json')

    def tearDown(self) -> None:
        """ Remove working temp files """
        remove_temp()

    def test_json_generate_report(self):
        """ Test report rendering with json config file """
        controller = Controller(config=Configuration(self.json))
        controller.render()

if __name__ == '__main__':
    unittest.main()
