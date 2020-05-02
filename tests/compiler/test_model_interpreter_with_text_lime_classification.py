#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Model Interpreter Generator """

import sys
sys.path.append('../')

import warnings

import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer

from PyPDF2 import PdfFileReader
from datetime import datetime

import unittest
import xai
from xai.compiler import Configuration, Controller
from xai.explainer import ExplainerFactory
from tests.compiler.util import (
    prepare_template,
    read_json_source,
    prepare_input_path,
    prepare_output_path,
    time_in_range,
    remove_temp
)


class TestModelInterpreter(unittest.TestCase):
    """
    Test case: Create Report using various dataset on pillar 2
    - refer to README in sample_input for more info on dataset
    - please update the config to include other feature in p2

              "domain": "text",
              "method": "lime",
              "mode": "classification"
    """

    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        """ Specify Config Files """
        self.json = prepare_template(filename='model-interpreter-nb-classification.json')
        json_obj = read_json_source(self.json)
        self.json_report_name = json_obj["name"]
        json_writers = json_obj["writers"]
        for writer in json_writers:
            if writer["class"] == "Pdf":
                self.json_writer_pdf_name = writer["attr"]["name"]
        self.json_writer_pdf_page_number = 4

        self.out_path = prepare_output_path(working_path='sample_output')

    def tearDown(self) -> None:
        """ Remove working temp files """
        remove_temp()

    def test_json_generate_report(self):
        # Set seed for reproducibility
        np.random.seed(123456)
        """ Test report rendering with json config file """
        # -- Train on a subset of categories --
        categories = [
            'rec.sport.baseball',
            'soc.religion.christian',
            'sci.med'
        ]

        raw_train = datasets.fetch_20newsgroups(data_home=prepare_input_path(working_path='sample_input/20news'),
                                                subset='train',
                                                categories=categories)
        print(list(raw_train.keys()))
        print(raw_train.target_names)
        print(raw_train.target[:10])
        raw_test = datasets.fetch_20newsgroups(subset='test',
                                               categories=categories)

        vectorizer = TfidfVectorizer()
        X_train = vectorizer.fit_transform(raw_train.data)
        y_train = raw_train.target

        X_test = vectorizer.transform(raw_test.data)
        y_test = raw_test.target

        clf = MultinomialNB(alpha=0.1)
        clf.fit(X_train, y_train)
        clf.score(X_test, y_test)
        print(clf.predict_proba)

        def predict_fn(instance):
            vec = vectorizer.transform(instance)
            return clf.predict_proba(vec)

        # -- Instantiate the explainer --
        explainer = ExplainerFactory.get_explainer(domain=xai.DOMAIN.TEXT)
        explainer.build_explainer(predict_fn)

        feature_names = []
        clf_fn = predict_fn
        target_names_list = []

        start_time = datetime.now().replace(microsecond=0)
        controller = Controller(config=Configuration(self.json, locals()))
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
        print("{} {} {}".format(start_time, report_time, end_time))
        self.assertTrue(time_in_range(start_time, end_time, report_time))

        print(number_of_pages)
        self.assertEqual(number_of_pages, self.json_writer_pdf_page_number)


if __name__ == '__main__':
    unittest.main()
