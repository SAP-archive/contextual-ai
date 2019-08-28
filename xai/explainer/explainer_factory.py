"""
This module houses the main Explainer class that users interact with, and can be imported with
from xai.explainer import Explainer
"""

from typing import Dict

from .abstract_explainer import AbstractExplainer
from .config import DICT_DOMAIN_TO_CLASS, DICT_DOMAIN_TO_DEFAULT_ALG
from .explainer_exceptions import DomainNotSupported, AlgorithmNotFoundInDomain


class Explainer(object):

    def __init__(self, domain: str, algorithm: str = None):
        """
        Constructor of the Explainer class

        Args:
            domain (str): Domain of the data, which should be one that is currently supported
            algorithm (str): Unique name of the algorithm for the particular domain
        """
        self.domain = domain
        self.algorithm = algorithm
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

        # We know that the domain is available, now see whether the user supplied an algorithm
        # or not
        if algorithm:
            self.algorithm = algorithm
        else:
            self.algorithm = DICT_DOMAIN_TO_DEFAULT_ALG[domain]
            algorithm = self.algorithm

        if algorithm not in dict_domain[domain]:
            raise AlgorithmNotFoundInDomain(domain, algorithm)

        alg_class = dict_domain[domain][algorithm]
        self.explainer = alg_class()

        # Set the base functions to those of the explainer class
        self.build_explainer = self.explainer.build_explainer
        self.explain_instance = self.explainer.explain_instance
        self.save_explainer = self.explainer.save_explainer
        self.load_explainer = self.explainer.load_explainer
