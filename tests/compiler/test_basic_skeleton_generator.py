#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Basic Json Generator """

import sys
sys.path.append('../')

import unittest
from xai.compiler.base import Configuration, Controller, Constant


class TestReportBasicSkeleton(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_json = 'sample_template/basic-skeleton.json'
        self.basic_yaml = 'sample_template/basic-skeleton.yml'

    def test_json_load_init(self):
        conf = Configuration(config=self.basic_json)
        conf = conf()
        self.assertIn(Constant.NAME.value, conf, msg="Section Title missing")
        name = conf[Constant.NAME.value]
        self.assertEqual(name, 'Sample Report', msg="Report name mis-match")
        self.assertIn(Constant.ENABLE_CONTENT_TABLE.value, conf,
                      msg="Content Table Flag missing")
        enable_content_table = conf[Constant.ENABLE_CONTENT_TABLE.value]
        self.assertTrue(enable_content_table, msg="Report name mis-match")

        self.assertIn(Constant.CONTENT_LIST.value, conf, msg="Section Content "
                                                           "missing")
        contents = conf[Constant.CONTENT_LIST.value]
        self.assertTrue(len(contents), 2)

    def test_yml_load_init(self):
        conf = Configuration(config=self.basic_yaml)
        conf = conf()
        self.assertIn(Constant.NAME.value, conf, msg="Section Title missing")
        name = conf[Constant.NAME.value]
        self.assertEqual(name, 'Sample Report', msg="Report name mis-match")
        self.assertIn(Constant.ENABLE_CONTENT_TABLE.value, conf,
                      msg="Content Table Flag missing")
        enable_content_table = conf[Constant.ENABLE_CONTENT_TABLE.value]
        self.assertTrue(enable_content_table, msg="Report name mis-match")

        self.assertIn(Constant.CONTENT_LIST.value, conf, msg="Section Content "
                                                           "missing")
        contents = conf[Constant.CONTENT_LIST.value]
        self.assertTrue(len(contents), 2)

    def test_json_load_call(self):
        call = Configuration()
        conf = call(config=self.basic_json)
        self.assertIn(Constant.NAME.value, conf, msg="Section Title missing")
        name = conf[Constant.NAME.value]
        self.assertEqual(name, 'Sample Report', msg="Report name mis-match")
        self.assertIn(Constant.ENABLE_CONTENT_TABLE.value, conf,
                      msg="Content Table Flag missing")
        enable_content_table = conf[Constant.ENABLE_CONTENT_TABLE.value]
        self.assertTrue(enable_content_table, msg="Report name mis-match")

        self.assertIn(Constant.CONTENT_LIST.value, conf, msg="Section Content "
                                                           "missing")
        contents = conf[Constant.CONTENT_LIST.value]
        self.assertTrue(len(contents), 2)

    def test_yml_load_call(self):
        call = Configuration()
        conf = call(config=self.basic_yaml)
        self.assertIn(Constant.NAME.value, conf, msg="Section Title missing")
        name = conf[Constant.NAME.value]
        self.assertEqual(name, 'Sample Report', msg="Report name mis-match")
        self.assertIn(Constant.ENABLE_CONTENT_TABLE.value, conf,
                      msg="Content Table Flag missing")
        enable_content_table = conf[Constant.ENABLE_CONTENT_TABLE.value]
        self.assertTrue(enable_content_table, msg="Report name mis-match")

        self.assertIn(Constant.CONTENT_LIST.value, conf, msg="Section Content "
                                                           "missing")
        contents = conf[Constant.CONTENT_LIST.value]
        self.assertTrue(len(contents), 2)

    def test_json_generate_report(self):
        controller = Controller(config=Configuration(self.basic_json))
        controller.render()

    def test_yml_generate_report(self):
        controller = Controller(config=Configuration(self.basic_yaml))
        controller.render()

if __name__ == '__main__':
    unittest.main()
