#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import unittest

from xai.explainer.config import DICT_DOMAIN_TO_DEFAULT_ALG, DICT_DOMAIN_TO_CLASS
from xai.explainer.explainer_exceptions import DomainNotSupported, AlgorithmNotFoundInDomain
from xai.explainer.explainer_factory import ExplainerFactory


class TestExplainer(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_get_explainer_domain_unsupported(self):
        """
        Test unsupported domain exception handling
        """
        with self.assertRaises(DomainNotSupported, msg='Domain should not be supported'):
            _ = ExplainerFactory.get_explainer(domain='unsupported_domain')

    def test_get_explainer_alg_unsupported(self):
        """
        Test unsupported algorithm exception handling
        """
        with self.assertRaises(AlgorithmNotFoundInDomain, msg='Algorithm should not be supported'):
            _ = ExplainerFactory.get_explainer(domain='text', algorithm='unsupported_algorithm')

    def test_get_explainer(self):
        """
        Test the creation of the explainer via the factory
        """
        domain = 'text'
        alg = DICT_DOMAIN_TO_DEFAULT_ALG[domain]
        expected_explainer_class = DICT_DOMAIN_TO_CLASS[domain][alg]
        expected_explainer = expected_explainer_class()
        actual_explainer = ExplainerFactory.get_explainer(domain, alg)

        # Is the correct class returned?
        self.assertIsInstance(actual_explainer, expected_explainer_class)

        # Are the functions properly mapped?
        self.assertEqual(actual_explainer.build_explainer.__qualname__,
                         expected_explainer.build_explainer.__qualname__)
        self.assertEqual(actual_explainer.explain_instance.__qualname__,
                         expected_explainer.explain_instance.__qualname__)
        self.assertEqual(actual_explainer.save_explainer.__qualname__,
                         expected_explainer.save_explainer.__qualname__)
        self.assertEqual(actual_explainer.load_explainer.__qualname__,
                         expected_explainer.load_explainer.__qualname__)


if __name__ == '__main__':
    unittest.main()
