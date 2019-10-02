#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Feature Importnace Ranking Generator """

import sys
sys.path.append('../')

import unittest
from xai.compiler.base import Configuration, Controller


class TestReportBasicSkeleton(unittest.TestCase):

    def setUp(self) -> None:
        self.json = 'sample_template/feature-importance-ranking.json'

    def test_json_generate_report(self):
        controller = Controller(config=Configuration(self.json))
        controller.render()

if __name__ == '__main__':
    unittest.main()
