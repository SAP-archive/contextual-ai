#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Data Statistics Analysis Generator NZa """

import sys
sys.path.append('../')

import warnings

from PyPDF2 import PdfFileReader
from datetime import datetime

import unittest
from xai.compiler import Configuration, Controller
from tests.compiler.util import (
    prepare_template,
    prepare_output_path,
    read_json_source,
    time_in_range,
    remove_temp
)


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
        json_obj = read_json_source(self.json)
        self.json_report_name = json_obj["name"]
        json_writers = json_obj["writers"]
        for writer in json_writers:
            if writer["class"] == "Pdf":
                self.json_writer_pdf_name = writer["attr"]["name"]
        self.json_writer_pdf_page_number = 8

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

if __name__ == '__main__':
    unittest.main()
