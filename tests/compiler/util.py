#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import os
import json
import yaml
import shutil

def prepare_template(filename: str):
    """ Prepare the path to template """
    path = os.path.dirname(__file__)
    json_file = os.path.join(path, 'sample_template', filename)
    with open(json_file) as f:
        file_data = f.read()
    in_path = os.path.join(path, 'sample_input')
    file_data = file_data.replace('{in_path}', in_path)
    out_path = os.path.join(path, 'sample_output')
    file_data = file_data.replace('{out_path}', out_path)
    working_path = os.path.join(path, '_temp')
    if not os.path.exists(working_path):
        os.makedirs(working_path)
    out_file = os.path.join(working_path, filename)
    with open(out_file, 'w') as f:
        f.write(file_data)
    return out_file

def read_json_source(filepath: str):
    """ Read Json Configuration Template """
    with open(filepath) as file:
        data = json.load(file)
    return data

def read_yaml_source(filepath: str):
    """ Read Yaml Configuration Template """
    with open(filepath) as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)
    return data

def prepare_input_path(working_path: str):
    """ Prepare input path """
    path = os.path.dirname(__file__)
    input_path = os.path.join(path, working_path)
    return input_path

def prepare_output_path(working_path: str):
    """ Prepare output path """
    path = os.path.dirname(__file__)
    output_path = os.path.join(path, working_path)
    return output_path

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

def remove_temp():
    """ Remove working dir """
    path = os.path.dirname(__file__)
    working_path = os.path.join(path, '_temp')
    if os.path.exists(working_path):
        shutil.rmtree(working_path)
