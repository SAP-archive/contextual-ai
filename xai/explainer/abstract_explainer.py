#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from abc import ABC, abstractmethod

from typing import Dict


class AbstractExplainer(ABC):

    def __init__(self):
        self.explainer_object = None

    @abstractmethod
    def build_explainer(self, **kwargs):
        """
        The build method for the explainer. Any explainer implementing a custom AbstractExplainer
        should provide clear documentation on the parameters required to initialize it.

        Args:
            **kwargs (dict): keyword arguments for initializing the explainer

        Returns:
            None
        """
        raise NotImplementedError("Derived class should implement this")

    @abstractmethod
    def explain_instance(self, **kwargs) -> Dict:
        """
        Explain an instance using the AbstractExplainer

        Args:
            **kwargs (dict): keyword arguments for calling the explanation method

        Returns:
            A dictionary that maps a class index to explanations
        """
        raise NotImplementedError("Derived class should implement this")

    @abstractmethod
    def save_explainer(self, path: str):
        """
        Saves the explainer to disk.

        Args:
            path (str): Path to which the explainer is stored

        Returns:
            None
        """
        raise NotImplementedError("Derived class should implement this")

    @abstractmethod
    def load_explainer(self, path: str):
        """
        Loads the explainer from disk.

        Args:
            path (str): Path to the explainer

        Returns:
            None

        Notes:
            load_explainer should not return the explainer, but it should instead load the
            AbstractExplainer instance with the explainer
            (e.g. set the self.explainer to the loaded object)
        """
        raise NotImplementedError("Derived class should implement this")
