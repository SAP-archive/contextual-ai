#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import os
from nltk import data as nltk_data

# -- Set NLTK Data Path --
path = os.path.dirname(__file__)
nltk_data.path.append(path)

from xai.data import helper as DataUtil
