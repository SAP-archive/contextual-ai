import unittest
import os
import numpy as np

from xai.explainer.config import DICT_DOMAIN_TO_DEFAULT_ALG, DICT_DOMAIN_TO_CLASS
from xai.explainer.explainer_exceptions import DomainNotSupported, AlgorithmNotFoundInDomain, \
    UnsupportedModeError, ExplainerUninitializedError
from xai.explainer.tabular.lime_tabular_explainer import LimeTabularExplainer
from lime.lime_tabular import LimeTabularExplainer as OriginalLimeTabularExplainer


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


class TestLimeTabularExplainer(unittest.TestCase):

    def setUp(self) -> None:
        self.save_path = 'lime_tabular_explainer.pkl'

    def test_build_explainer_unsupported_mode(self):
        """
        Test exception handling when unsupported mode is raised
        """
        with self.assertRaises(UnsupportedModeError, msg='Algorithm should raise unsupported mode'
                                                         'error'):
            explainer = LimeTabularExplainer()
            explainer.build_explainer(np.arange(9).reshape((3, 3)), mode='unsupported_mode')

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
        explainer.build_explainer(np.arange(9).reshape((3, 3)), mode='classification', verbose=True)
        self.assertIsInstance(explainer.explainer_object, OriginalLimeTabularExplainer)

    def test_save_explainer(self):
        """
        Test the saving of the explainer
        """
        explainer = LimeTabularExplainer()
        explainer.build_explainer(np.arange(9).reshape((3, 3)), mode='classification')
        explainer.save_explainer(self.save_path)
        self.assertTrue(os.path.exists(self.save_path))

    def test_load_explainer(self):
        """
        Test loading the explainer
        """
        explainer = LimeTabularExplainer()
        explainer.build_explainer(np.arange(9).reshape((3, 3)), mode='classification')
        explainer.save_explainer(self.save_path)

        new_explainer = LimeTabularExplainer()
        new_explainer.load_explainer(self.save_path)
        self.assertIsNotNone(new_explainer.explainer_object)

    def test_explanation_to_json(self):
        dummy_explanation = DummyExplanation()
        labels = [0, 1]
        confidences = np.array([0.0, 1.0])

        expected = {0: {'confidence': 0.0,
                        'explanation': [{'feature': 'worst perimeter <= 83.79',
                                         'importance': -0.10275161028167702},
                                        {'feature': 'worst area <= 509.25',
                                         'importance': -0.09479442043867894},
                                        {'feature': 'worst radius <= 12.93',
                                         'importance': -0.060148145614287524},
                                        {'feature': 'worst texture <= 21.41',
                                         'importance': -0.057578312942073995},
                                        {'feature': 'mean area <= 419.25',
                                         'importance': -0.05598211138713413},
                                        {'feature': 'worst concave points <= 0.06',
                                         'importance': -0.05063258480760927},
                                        {'feature': 'mean texture <= 16.34',
                                         'importance': -0.042193966171229905},
                                        {'feature': 'mean concavity <= 0.03',
                                         'importance': -0.028153608385264327},
                                        {'feature': 'area error <= 18.17',
                                         'importance': -0.027911303586217028},
                                        {'feature': 'worst compactness <= 0.15',
                                         'importance': -0.024483076857988333}]},
                    1: {'confidence': 1.0,
                        'explanation': [{'feature': 'worst perimeter <= 83.79',
                                         'importance': 0.10275161028167702},
                                        {'feature': 'worst area <= 509.25',
                                         'importance': 0.09479442043867897},
                                        {'feature': 'worst radius <= 12.93',
                                         'importance': 0.06014814561428753},
                                        {'feature': 'worst texture <= 21.41',
                                         'importance': 0.057578312942073995},
                                        {'feature': 'mean area <= 419.25',
                                         'importance': 0.05598211138713414},
                                        {'feature': 'worst concave points <= 0.06',
                                         'importance': 0.05063258480760927},
                                        {'feature': 'mean texture <= 16.34',
                                         'importance': 0.0421939661712299},
                                        {'feature': 'mean concavity <= 0.03',
                                         'importance': 0.028153608385264303},
                                        {'feature': 'area error <= 18.17',
                                         'importance': 0.027911303586217028},
                                        {'feature': 'worst compactness <= 0.15',
                                         'importance': 0.024483076857988346}]}}

        explainer = LimeTabularExplainer()
        actual = explainer._explanation_to_json(
            explanation=dummy_explanation,
            labels=labels,
            confidences=confidences
        )

        self.assertEquals(expected, actual, msg='JSON explanations should be the same!')

    def tearDown(self) -> None:
        if os.path.exists(self.save_path):
            os.remove(self.save_path)


if __name__ == '__main__':
    unittest.main()
