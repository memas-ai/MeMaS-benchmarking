#!/bin/bash

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt
# TODO: remove this after beam/datasets package upgrade 
pip install --no-deps -r requirements-no-deps.txt

# pip install -r test-requirements.txt

# export PYTHONPATH=$PYTHONPATH:memas:memas_client:memas_sdk
