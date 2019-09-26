#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import unittest

from xai.explainer.abstract_explainer import AbstractExplainer


class UnimplementedAbstractExplainer(AbstractExplainer):

    def __init__(self):
        super(AbstractExplainer, self).__init__()


class TestAbstractExplainer(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_unimplemented_abstract_explainer(self):
        """
        Make sure that an unimplemented abstract explainer subclass does not get instantiated
        """
        with self.assertRaises(TypeError):
            try:
                _ = AbstractExplainer()
            except TypeError as e:
                msg = e.args[0]
                self.assertEqual(msg,
                                 'Can\'t instantiate abstract class AbstractExplainer '
                                 'with abstract methods build_explainer, explain_instance, '
                                 'load_explainer, save_explainer',
                                 'Exception messages do not match')
                raise TypeError(msg)


if __name__ == '__main__':
    unittest.main()
