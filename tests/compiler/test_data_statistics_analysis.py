#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Data Statistics Analysis Generator """

import sys
sys.path.append('../')

import warnings

from PyPDF2 import PdfFileReader
from datetime import datetime

import unittest
from xai.compiler import Configuration, Controller
from tests.compiler.util import (
    prepare_template,
    read_json_source,
    read_yaml_source,
    prepare_output_path,
    time_in_range,
    remove_temp
)


class TestDataStatisticsAnalysis(unittest.TestCase):
    """
    Test case: Create Report with ONLY Data Analysis (p1)
    """

    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        """ Specify Config Files """
        self.json = prepare_template(filename='data-statistics-analysis.json')
        json_obj = read_json_source(self.json)
        self.json_report_name = json_obj["name"]
        json_writers = json_obj["writers"]
        for writer in json_writers:
            if writer["class"] == "Pdf":
                self.json_writer_pdf_name = writer["attr"]["name"]
            if writer["class"] == "Html":
                self.json_writer_html_name = writer["attr"]["name"]
        self.json_writer_pdf_page_number = 26
        self.json_writer_html_tag_number = 1

        self.yaml = prepare_template(filename='data-statistics-analysis.yml')
        yaml_obj = read_yaml_source(self.yaml)
        self.yaml_report_name = yaml_obj["name"]
        yaml_writers = yaml_obj["writers"]
        for writer in yaml_writers:
            if writer["class"] == "Pdf":
                self.yaml_writer_pdf_name = writer["attr"]["name"]
            if writer["class"] == "Html":
                self.yaml_writer_html_name = writer["attr"]["name"]
        self.yaml_writer_pdf_page_number = 26
        self.yaml_writer_html_tag_number = 1

        self.out_path = prepare_output_path(working_path='sample_output')

    def tearDown(self) -> None:
        """ Remove working temp files """
        remove_temp()

    def test_json_generate_report(self):
        """ Test report rendering with json config file """
        start_time = datetime.now().replace(microsecond=0)
        controller = Controller(config=Configuration(self.json))
        controller.render()
        end_time = datetime.now().replace(microsecond=0)

        # -- PDF Report --
        output = "%s/%s.pdf" % (self.out_path, self.json_writer_pdf_name)
        print("JSON-PDF report generated %s:" % output)

        with open(output, 'rb') as f:
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
            number_of_pages = pdf.getNumPages()

        print(info)
        self.assertEqual(info['/Title'], self.json_report_name)

        # print(info['/CreationDate'])
        report_time = datetime.strptime(
            info['/CreationDate'], 'D:%Y%m%d%H%M%S')
        self.assertTrue(time_in_range(start_time, end_time, report_time))

        print(number_of_pages)
        self.assertEqual(number_of_pages, self.json_writer_pdf_page_number)

        # -- HTML Report --
        output = "%s/%s.html" % (self.out_path, self.json_writer_html_name)
        print("JSON-HTML report generated %s:" % output)

        with open(output) as f:
            read_data = f.read()

        index = read_data.find(self.json_report_name)
        # -- the header start at index 1279 --
        self.assertEqual(index, 1279)

        index = read_data.find('created on')
        create_date = read_data[index+11: index+30]
        # print(create_date)
        report_time = datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S')
        print("{} {} {}".format(start_time, report_time, end_time))
        self.assertTrue(time_in_range(start_time, end_time, report_time))

        number_of_tags = read_data.count('class="tab_contents"')
        # print(number_of_tags)
        self.assertEqual(number_of_tags, self.json_writer_html_tag_number)


    def test_yaml_generate_report(self):
        """ Test report rendering with yaml config file """
        start_time = datetime.now().replace(microsecond=0)
        controller = Controller(config=Configuration(self.yaml))
        controller.render()
        end_time = datetime.now().replace(microsecond=0)

        # -- PDF Report --
        output = "%s/%s.pdf" % (self.out_path, self.yaml_writer_pdf_name)
        print("YAML-PDF report generated %s:" % output)

        with open(output, 'rb') as f:
            pdf = PdfFileReader(f)
            info = pdf.getDocumentInfo()
            number_of_pages = pdf.getNumPages()

        print(info)
        self.assertEqual(info['/Title'], self.yaml_report_name)

        # print(info['/CreationDate'])
        report_time = datetime.strptime(
            info['/CreationDate'], 'D:%Y%m%d%H%M%S')
        self.assertTrue(time_in_range(start_time, end_time, report_time))

        print(number_of_pages)
        self.assertEqual(number_of_pages, self.yaml_writer_pdf_page_number)

        # -- HTML Report --
        output = "%s/%s.html" % (self.out_path, self.yaml_writer_html_name)
        print("YAML-HTML report generated %s:" % output)

        with open(output) as f:
            read_data = f.read()

        index = read_data.find(self.yaml_report_name)
        # -- the header start at index 1279 --
        self.assertEqual(index, 1279)

        index = read_data.find('created on')
        create_date = read_data[index+11: index+30]
        # print(create_date)
        report_time = datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S')
        print("{} {} {}".format(start_time, report_time, end_time))
        self.assertTrue(time_in_range(start_time, end_time, report_time))

        number_of_tags = read_data.count('class="tab_contents"')
        # print(number_of_tags)
        self.assertEqual(number_of_tags, self.yaml_writer_html_tag_number)

if __name__ == '__main__':
    unittest.main()
