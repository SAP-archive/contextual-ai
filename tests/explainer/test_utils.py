#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import unittest

import numpy as np

from xai.explainer.utils import explanation_to_json
from xai.explainer.constants import MODE

class DummyExplanation(object):

    def as_list(self, label):
        explanations = {
            0: [('worst perimeter <= 83.79', -0.10275161028167702),
                ('worst area <= 509.25', -0.09479442043867894),
                ('worst radius <= 12.93', -0.060148145614287524),
                ('worst texture <= 21.41', -0.057578312942073995),
                ('mean area <= 419.25', -0.05598211138713413),
                ('worst concave points <= 0.06', -0.05063258480760927),
                ('mean texture <= 16.34', -0.042193966171229905),
                ('mean concavity <= 0.03', -0.028153608385264327),
                ('area error <= 18.17', -0.027911303586217028),
                ('worst compactness <= 0.15', -0.024483076857988333)],
            1: [('worst perimeter <= 83.79', 0.10275161028167702),
                ('worst area <= 509.25', 0.09479442043867897),
                ('worst radius <= 12.93', 0.06014814561428753),
                ('worst texture <= 21.41', 0.057578312942073995),
                ('mean area <= 419.25', 0.05598211138713414),
                ('worst concave points <= 0.06', 0.05063258480760927),
                ('mean texture <= 16.34', 0.0421939661712299),
                ('mean concavity <= 0.03', 0.028153608385264303),
                ('area error <= 18.17', 0.027911303586217028),
                ('worst compactness <= 0.15', 0.024483076857988346)]
        }
        return explanations[label]


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_explanation_to_json(self):
        """
        Test the parsing of explanations
        """
        dummy_explanation = DummyExplanation()
        labels = [0, 1]
        confidences = np.array([0.0, 1.0])

        expected = {0: {'prediction': 0.0,
                        'explanation': sorted([{'feature': 'worst perimeter <= 83.79',
                                         'score': -0.10275161028167702},
                                        {'feature': 'worst area <= 509.25',
                                         'score': -0.09479442043867894},
                                        {'feature': 'worst radius <= 12.93',
                                         'score': -0.060148145614287524},
                                        {'feature': 'worst texture <= 21.41',
                                         'score': -0.057578312942073995},
                                        {'feature': 'mean area <= 419.25',
                                         'score': -0.05598211138713413},
                                        {'feature': 'worst concave points <= 0.06',
                                         'score': -0.05063258480760927},
                                        {'feature': 'mean texture <= 16.34',
                                         'score': -0.042193966171229905},
                                        {'feature': 'mean concavity <= 0.03',
                                         'score': -0.028153608385264327},
                                        {'feature': 'area error <= 18.17',
                                         'score': -0.027911303586217028},
                                        {'feature': 'worst compactness <= 0.15',
                                         'score': -0.024483076857988333}],
                                              key=lambda x: x['score'], reverse=True)},
                    1: {'prediction': 1.0,
                        'explanation': sorted([{'feature': 'worst perimeter <= 83.79',
                                         'score': 0.10275161028167702},
                                        {'feature': 'worst area <= 509.25',
                                         'score': 0.09479442043867897},
                                        {'feature': 'worst radius <= 12.93',
                                         'score': 0.06014814561428753},
                                        {'feature': 'worst texture <= 21.41',
                                         'score': 0.057578312942073995},
                                        {'feature': 'mean area <= 419.25',
                                         'score': 0.05598211138713414},
                                        {'feature': 'worst concave points <= 0.06',
                                         'score': 0.05063258480760927},
                                        {'feature': 'mean texture <= 16.34',
                                         'score': 0.0421939661712299},
                                        {'feature': 'mean concavity <= 0.03',
                                         'score': 0.028153608385264303},
                                        {'feature': 'area error <= 18.17',
                                         'score': 0.027911303586217028},
                                        {'feature': 'worst compactness <= 0.15',
                                         'score': 0.024483076857988346}],
                                              key=lambda x: x['score'], reverse=True)}}

        actual = explanation_to_json(
            explanation=dummy_explanation,
            labels=labels,
            predictions=confidences,
            mode=MODE.CLASSIFICATION
        )

        self.assertEquals(expected, actual, msg='JSON explanations should be the same!')


if __name__ == '__main__':
    unittest.main()
