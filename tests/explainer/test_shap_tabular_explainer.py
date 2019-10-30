#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import os
import unittest

import numpy as np
from shap import KernelExplainer

from xai.explainer.explainer_exceptions import ExplainerUninitializedError
from xai.explainer.tabular.shap_tabular_explainer import SHAPTabularExplainer
from sklearn.dummy import DummyClassifier


class TestSHAPTabularExplainer(unittest.TestCase):

    def dummy_predict_fn(self, x):
        return self.model.predict_proba(x)

    def setUp(self) -> None:
        self.save_path = 'shap_tabular_explainer.pkl'
        self.model = DummyClassifier()
        self.model.fit(np.arange(9).reshape((3, 3)), [1, 2, 3])

    def test_build_explainer_uninitialized_explainer(self):
        """
        Test exception check when explain_instance is called for un-built explainer
        """
        with self.assertRaises(ExplainerUninitializedError, msg='Algorithm should raise '
                                                                'uninitialized error if exlpainers'
                                                                'build method is not called'):
            explainer = SHAPTabularExplainer()
            explainer.explain_instance(np.array([0]))

    def test_build_explainer(self):
        """
        Test building the explainer
        """
        explainer = SHAPTabularExplainer()
        data = np.arange(9).reshape((3, 3))
        explainer.build_explainer(predict_fn=self.dummy_predict_fn,
                                  training_data=data)
        self.assertIsInstance(explainer.explainer_object, KernelExplainer)

    def test_save_explainer(self):
        """
        Test the saving of the explainer
        """
        explainer = SHAPTabularExplainer()
        explainer.save_explainer(self.save_path)
        self.assertTrue(os.path.exists(self.save_path))

    def tearDown(self) -> None:
        if os.path.exists(self.save_path):
            os.remove(self.save_path)


if __name__ == '__main__':
    unittest.main()
