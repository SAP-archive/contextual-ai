#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import os
import unittest

from lime.lime_text import LimeTextExplainer as OriginalLimeTextExplainer

from xai.explainer.explainer_exceptions import ExplainerUninitializedError
from xai.explainer.text.lime_text_explainer import LimeTextExplainer


class TestLimeTextExplainer(unittest.TestCase):

    def setUp(self) -> None:
        self.save_path = 'lime_text_explainer.pkl'

    def test_build_explainer_uninitialized_explainer(self):
        """
        Test exception check when explain_instance is called for un-built explainer
        """
        with self.assertRaises(ExplainerUninitializedError, msg='Algorithm should raise '
                                                                'uninitialized error if exlpainers'
                                                                'build method is not called'):
            explainer = LimeTextExplainer()
            explainer.explain_instance(None, None)

    def test_build_explainer(self):
        """
        Test building the explainer
        """
        explainer = LimeTextExplainer()
        explainer.build_explainer(predict_fn=None)
        self.assertIsInstance(explainer.explainer_object, OriginalLimeTextExplainer)

    def test_save_explainer(self):
        """
        Test the saving of the explainer
        """
        explainer = LimeTextExplainer()
        explainer.build_explainer(predict_fn=None)
        explainer.save_explainer(self.save_path)
        self.assertTrue(os.path.exists(self.save_path))

    def test_load_explainer(self):
        """
        Test loading the explainer
        """
        explainer = LimeTextExplainer()
        explainer.build_explainer(predict_fn=None)
        explainer.save_explainer(self.save_path)

        new_explainer = LimeTextExplainer()
        new_explainer.load_explainer(self.save_path)
        self.assertIsNotNone(new_explainer.explainer_object)

    def tearDown(self) -> None:
        if os.path.exists(self.save_path):
            os.remove(self.save_path)


if __name__ == '__main__':
    unittest.main()
