#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Basic Json Generator """

import sys
sys.path.append('../')

import warnings

import unittest
from xai.compiler import Configuration, Controller, Constant
from tests.compiler.util import prepare_template, remove_temp


class TestReportBasicSkeleton(unittest.TestCase):
    """
    Test case: Create Report with only basic skeleton, such as h1, h2,
    h3 and paragraph
    """

    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        """ Specify Config Files """
        self.basic_json = prepare_template(filename='basic-skeleton.json')
        self.basic_yaml = prepare_template(filename='basic-skeleton.yml')

    def tearDown(self) -> None:
        """ Remove working temp files """
        remove_temp()

    def test_json_load_init(self):
        """ Test json config file loading using __init__ """
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
        """ Test yaml config file loading using __init__ """
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
        """ Test json config file loading using __call__ """
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
        """ Test json config file loading using __call__ """
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
        """ Test report rendering with json config file """
        controller = Controller(config=Configuration(self.basic_json))
        controller.render()

    def test_yml_generate_report(self):
        """ Test report rendering with yaml config file """
        controller = Controller(config=Configuration(self.basic_yaml))
        controller.render()

if __name__ == '__main__':
    unittest.main()
