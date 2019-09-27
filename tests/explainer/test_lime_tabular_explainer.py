#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import os
import unittest

import numpy as np
from lime.lime_tabular import LimeTabularExplainer as OriginalLimeTabularExplainer

import xai
from xai.explainer.explainer_exceptions import UnsupportedModeError, ExplainerUninitializedError
from xai.explainer.tabular.lime_tabular_explainer import LimeTabularExplainer


class TestLimeTabularExplainer(unittest.TestCase):

    def setUp(self) -> None:
        self.save_path = 'lime_tabular_explainer.pkl'

    def test_build_explainer_unsupported_mode(self):
        """
        Test exception check when unsupported mode is provided
        """
        with self.assertRaises(UnsupportedModeError, msg='Algorithm should raise unsupported mode'
                                                         'error'):
            explainer = LimeTabularExplainer()
            explainer.build_explainer(np.arange(9).reshape((3, 3)), mode='unsupported_mode',
                                      predict_fn=None)

    def test_build_explainer_uninitialized_explainer(self):
        """
        Test exception check when explain_instance is called for un-built explainer
        """
        with self.assertRaises(ExplainerUninitializedError, msg='Algorithm should raise '
                                                                'uninitialized error if exlpainers'
                                                                'build method is not called'):
            explainer = LimeTabularExplainer()
            explainer.explain_instance(None, None)

    def test_build_explainer(self):
        """
        Test building the explainer
        """
        explainer = LimeTabularExplainer()
        explainer.build_explainer(np.arange(9).reshape((3, 3)),
                                  mode=xai.MODE.CLASSIFICATION, predict_fn=None, verbose=True)
        self.assertIsInstance(explainer.explainer_object, OriginalLimeTabularExplainer)

    def test_save_explainer(self):
        """
        Test the saving of the explainer
        """
        explainer = LimeTabularExplainer()
        explainer.build_explainer(np.arange(9).reshape((3, 3)), mode=xai.MODE.CLASSIFICATION,
                                  predict_fn=None)
        explainer.save_explainer(self.save_path)
        self.assertTrue(os.path.exists(self.save_path))

    def test_load_explainer(self):
        """
        Test loading the explainer
        """
        explainer = LimeTabularExplainer()
        explainer.build_explainer(np.arange(9).reshape((3, 3)), mode=xai.MODE.CLASSIFICATION,
                                  predict_fn=None)
        explainer.save_explainer(self.save_path)

        new_explainer = LimeTabularExplainer()
        new_explainer.load_explainer(self.save_path)
        self.assertIsNotNone(new_explainer.explainer_object)

    def tearDown(self) -> None:
        if os.path.exists(self.save_path):
            os.remove(self.save_path)


if __name__ == '__main__':
    unittest.main()
