#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================
# -- Utilities --

import json

import numpy as np


################################################################################
### Report Utilities
################################################################################

class JsonSerializable(json.JSONEncoder):
    """
    Json Serializable - numpy object type
    """

    def default(self, obj):
        if isinstance(obj, np.integer):
            if np.isnan(obj):
                return 0
            return int(obj)
        elif isinstance(obj, np.floating):
            if np.isnan(obj):
                return 0.0
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(JsonSerializable, self).default(obj)


def get_table_layout(table_header):
    """
    Count table layout

    Args:
        table_header: table header array-list

    Returns:
        size of the layout
    """
    column = len(table_header) - 1
    width = (180 - 30) / column
    layout = [30]
    layout.extend([width] * column)
    return layout
