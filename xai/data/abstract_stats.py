#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

from abc import abstractmethod, ABC

from typing import Dict

from xai.data.exceptions import InvalidTypeError


class AbstractStats(ABC):
    """
    Abstract class for data statistics for all types data analyzer
    """

    def __init__(self):
        self.total_count = 0

    @property
    def total_count(self):
        return self._total_count

    @total_count.setter
    def total_count(self, value: int):
        if not isinstance(value, int):
            raise InvalidTypeError('total_count', type(value), '<int>')
        self._total_count = value

    @abstractmethod
    def to_json(self) -> Dict:
        """
        Map the stats to json object

        Returns:
            A dictionary contains key statistical attribute
        """
        raise NotImplementedError('The derived helper needs to implement it.')
