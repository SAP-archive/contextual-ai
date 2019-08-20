"""
This module houses the main Explainer class that users interact with, and can be imported with
from xai.explainer import Explainer
"""

from typing import Dict

from xai.explainer.abstract_explainer import AbstractExplainer
from xai.explainer.config import DICT_DOMAIN_TO_CLASS, DICT_DOMAIN_TO_DEFAULT_ALG
from xai.explainer.explainer_exceptions import DomainNotSupported, AlgorithmNotFoundInDomain


class Explainer(object):

    def __init__(self, domain: str, algorithm: str = None):
        """
        Constructor of the Explainer class

        Args:
            domain (str): Domain of the data, which should be one that is currently supported
            algorithm (str): Unique name of the algorithm for the particular domain
        """
        self.domain = domain

        if algorithm:
            self.algorithm = algorithm
        else:
            self.algorithm = DICT_DOMAIN_TO_DEFAULT_ALG[self.domain]

        self.create_explainer(DICT_DOMAIN_TO_CLASS, self.domain, self.algorithm)

    def create_explainer(self, dict_domain: Dict[str, Dict[str, AbstractExplainer]],
                         domain: str, algorithm: str):
        """
        Checks whether the given domain and algorithm leads to an existing explainer implementation

        Args:
            dict_domain (dict): Mapping from domain to explainer algorithms
            domain (str): User-provided domain
            algorithm (str): User-provided unique identifier of the algorithm

        Returns:
            None

        Raises:
            DomainNotSupported: If the domain is not in dict_domain
            AlgorithmNotFound: If the algorithm is not in the particular domain

        """
        if domain not in dict_domain:
            raise DomainNotSupported(domain)

        if algorithm not in dict_domain[domain]:
            raise AlgorithmNotFoundInDomain(domain, algorithm)

        self.explainer = dict_domain[domain][algorithm].__init__()
        # Set the base functions to those of the explainer class
        self.build_explainer = self.explainer.build_explainer
        self.explain_instance = self.explainer.explain_instance

    def save_explainer(self, path: str):
        """
        Saves the explainer to disk.

        Args:
            path (str): Path to which the explainer is stored

        Returns:
            (bool) Whether saving the explainer was successful or not
        """
        self.explainer.save_explainer(path)

    def load_explainer(self, path: str):
        """
        Loads the explainer from disk.

        Args:
            path (str): Path to the explainer

        Returns:
            (bool) Whether the explainer was successfully loaded or not

        Notes:
            load_explainer should not return the explainer, but it should instead load the
            AbstractExplainer instance with the explainer (e.g. set the self.explainer to the loaded
            object)
        """
        self.explainer.load_explainer(path)
