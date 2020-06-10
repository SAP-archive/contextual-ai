#!/usr/bin/env bash
rm -rf build
rm -rf dist
rm -rf contextual-ai.egg-info
python setup.py bdist_wheel --universal
