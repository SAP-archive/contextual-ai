#!/usr/bin/env bash
rm -rf build
rm -rf dist
rm -rf sap_explainable_ai.egg-info
python setup.py bdist_wheel --universal
