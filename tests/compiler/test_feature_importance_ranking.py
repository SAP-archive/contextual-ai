#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Feature Importnace Ranking Generator """

import sys
sys.path.append('../')

import unittest
from xai.compiler import Configuration, Controller
from tests.compiler.util import prepare_template, remove_temp


class TestFeatureImportanceRanking(unittest.TestCase):
    """
    Test case: Create Report using various dataset on pillar 2
    - refer to README in sample_input for more info on dataset
    - please update the config to include other feature in p2
    """

    def setUp(self) -> None:
        """ Specify Config Files """
        self.json = prepare_template(filename='feature-importance-ranking.json')
        self.yaml = prepare_template(filename='feature-importance-ranking.yml')

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
