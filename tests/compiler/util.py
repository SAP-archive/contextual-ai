#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import os
import shutil

def prepare_template(filename: str):
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

def remove_temp():
    path = os.path.dirname(__file__)
    working_path = os.path.join(path, '_temp')
    if os.path.exists(working_path):
        shutil.rmtree(working_path)


def prepare_output_path(working_path: str):
    path = os.path.dirname(__file__)
    output_path = os.path.join(path, working_path)
    return output_path
