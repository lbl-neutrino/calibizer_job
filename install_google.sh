#!/usr/bin/env bash

python -m venv google_venv
source google_venv/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
