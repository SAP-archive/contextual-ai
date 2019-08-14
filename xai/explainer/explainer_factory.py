"""
This module houses the main Explainer class that users interact with, and can be imported with
from xai.explainer import Explainer
"""

from typing import Dict

from xai.explainer.abstract_explainer import AbstractExplainer
from xai.explainer.config import DEFAULT_ALGORITHM, DICT_DOMAIN_TO_CLASS
from xai.explainer.explainer_exceptions import DomainNotSupported, AlgorithmNotFoundInDomain


class Explainer(object):

    def __init__(self, domain: str, algorithm: str = DEFAULT_ALGORITHM):
        """
        Constructor of the Explainer class

        Args:
            domain (str): Domain of the data, which should be one that is currently supported
            algorithm (str): Unique name of the algorithm for the particular domain
        """
        self.domain = domain
        self.algorithm = algorithm
        self.explainer = self._get_explainer(DICT_DOMAIN_TO_CLASS, self.domain, self.algorithm)

    def _get_explainer(self, dict_domain: Dict[str, Dict[str, AbstractExplainer]],
                       domain: str, algorithm: str) -> AbstractExplainer:
        """
        Checks whether the given domain and algorithm leads to an existing explainer implementation

        Args:
            dict_domain (dict): Mapping from domain to explainer algorithms
            domain (str): User-provided domain
            algorithm (str): User-provided unique identifier of the algorithm

        Returns:
            An child instance of AbstractExplainer

        Raises:
            DomainNotSupported: If the domain is not in dict_domain
            AlgorithmNotFound: If the algorithm is not in the particular domain

        """
        if domain not in dict_domain:
            raise DomainNotSupported(domain)

        if algorithm not in dict_domain[domain]:
            raise AlgorithmNotFoundInDomain(domain, algorithm)

        return dict_domain[domain][algorithm]
