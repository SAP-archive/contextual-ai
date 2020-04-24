#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
"""  Model Interpreter Generator with Random Forest Regression """

import sys
sys.path.append('../')

import warnings

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor
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
        self.json = prepare_template(filename='feature-importance-racking-xgb-regression.json')
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

        my_model = XGBRegressor(n_estimators=1000,
                                max_depth=5,
                                learning_rate=0.1,
                                subsample=0.7,
                                colsample_bytree=0.8,
                                colsample_bylevel=0.8,
                                base_score=train_y.mean(),
                                random_state=42, seed=42)
        hist = my_model.fit(train_X, train_y,
                            early_stopping_rounds=5,
                            eval_set=[(test_X, test_y)], eval_metric='rmse',
                            verbose=100)

        X.columns.tolist()
        train_X_df = pd.DataFrame(data=train_X, columns=X.columns.tolist())
        clf = my_model
        clf_fn = my_model.predict
        y_train = []
        feature_names = X.columns.tolist()
        target_names_list = ['SalePrice']

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
        # self.assertEqual(number_of_pages, self.json_writer_pdf_page_number)
        #
        # # -- HTML Report --
        # output = "%s/%s.html" % (self.out_path, self.json_writer_html_name)
        # print("JSON-HTML report generated %s:" % output)
        #
        # with open(output) as f:
        #     read_data = f.read()
        #
        # index = read_data.find(self.json_report_name)
        # # -- the header start at index 1279 --
        # self.assertEqual(index, 1279)
        #
        # index = read_data.find('created on')
        # create_date = read_data[index+11: index+30]
        # print(create_date)
        # report_time = datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S')
        # print("{} {} {}".format(start_time, report_time, end_time))
        # self.assertTrue(time_in_range(start_time, end_time, report_time))
        #
        # number_of_tags = read_data.count('class="tab_contents"')
        # # print(number_of_tags)
        # self.assertEqual(number_of_tags, self.json_writer_html_tag_number)


if __name__ == '__main__':
    unittest.main()
