#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Model Interpreter Generator with Random Forest Regression """

import sys
sys.path.append('../')

import warnings

import shap
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingRegressor
from PyPDF2 import PdfFileReader
from datetime import datetime

import unittest
from xai.compiler import Configuration, Controller
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
    """

    def setUp(self) -> None:
        warnings.simplefilter("ignore", ResourceWarning)
        """ Specify Config Files """
        self.json = prepare_template(filename='feature-importance-ranking-gb-regression.json')
        json_obj = read_json_source(self.json)
        self.json_report_name = json_obj["name"]
        json_writers = json_obj["writers"]
        for writer in json_writers:
            if writer["class"] == "Pdf":
                self.json_writer_pdf_name = writer["attr"]["name"]
        self.json_writer_pdf_page_number = 3
        self.limit_size = 50
        self.out_path = prepare_output_path(working_path='sample_output')

    def tearDown(self) -> None:
        """ Remove working temp files """
        remove_temp()

    def test_json_generate_report(self):
        # Set seed for reproducibility
        np.random.seed(123456)
        """ Test report rendering with json config file """
        # Load the dataset and prepare training and test sets
        train_file = prepare_input_path(working_path='sample_input/housing_price/train.csv')
        data = pd.read_csv(train_file)
        data.dropna(axis=0, subset=['SalePrice'], inplace=True)
        y = data.SalePrice

        X = data.drop(['SalePrice', 'Id'], axis=1).select_dtypes(
            exclude=['object'])
        train_X, test_X, train_y, test_y = train_test_split(X.values, y.values,
                                                            test_size=0.25)

        my_imputer = SimpleImputer()
        train_X = my_imputer.fit_transform(train_X)
        test_X = my_imputer.transform(test_X)

        my_model = GradientBoostingRegressor(n_estimators=1000,
                                             max_depth=5,
                                             learning_rate=0.1,
                                             subsample=0.7,
                                             random_state=42)
        hist = my_model.fit(train_X, train_y)

        X.columns.tolist()
        train_X_df = pd.DataFrame(data=train_X, columns=X.columns.tolist())
        train_X_km = shap.kmeans(train_X_df, 10)
        clf = my_model
        clf_fn = my_model.predict
        y_train = []
        feature_names = X.columns.tolist()
        target_names_list = ['SalePrice']

        print('Subseting training data to %s speed up...'%self.limit_size)
        train_X_df = train_X_df[:self.limit_size]
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
