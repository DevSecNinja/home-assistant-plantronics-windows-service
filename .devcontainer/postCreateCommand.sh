#!/bin/bash

# Prepare Python venv
python -m venv ./.env
./.env/bin/python -m pip install --upgrade pip setuptools wheel
./.env/bin/python -m pip install -r ./requirements.txt
