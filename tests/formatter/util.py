#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import os

def prepare_input_path(data_path: str):
    """ Prepare input path """
    path = os.path.dirname(__file__)
    input_path = os.path.join(path, data_path)
    return input_path

def prepare_output_path(working_path: str):
    """ Prepare output path"""
    path = os.path.dirname(__file__)
    output_path = os.path.join(path, working_path)
    return output_path
