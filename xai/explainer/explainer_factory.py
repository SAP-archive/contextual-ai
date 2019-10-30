"""
This module houses the main ExplainerFactory class that users interact with, and can be imported with
from xai.explainer import ExplainerFactory
"""
#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from typing import Optional

from xai.explainer.abstract_explainer import AbstractExplainer
from xai.explainer.config import DICT_DOMAIN_TO_CLASS, DICT_DOMAIN_TO_DEFAULT_ALG
from xai.explainer.explainer_exceptions import DomainNotSupported, AlgorithmNotFoundInDomain


class ExplainerFactory:

    @staticmethod
    def get_explainer(domain: str, algorithm: Optional[str] = None) -> AbstractExplainer:
        """
        Returns a AbstractExplainer that is supported by the XAI library

        Args:
            domain (str): User-provided domain
            algorithm (str): User-provided unique identifier of the algorithm

        Returns:
            AbstractExplainer

        Raises:
            DomainNotSupported: If the domain is not in dict_domain
            AlgorithmNotFound: If the algorithm is not in the particular domain

        """
        if domain not in DICT_DOMAIN_TO_CLASS:
            raise DomainNotSupported(domain)

        # We know that the domain is available, now see whether the user supplied an algorithm
        # or not
        if algorithm is None:
            algorithm = DICT_DOMAIN_TO_DEFAULT_ALG[domain]

        if algorithm not in DICT_DOMAIN_TO_CLASS[domain]:
            raise AlgorithmNotFoundInDomain(domain, algorithm)

        alg_class = DICT_DOMAIN_TO_CLASS[domain][algorithm]
        return alg_class()
