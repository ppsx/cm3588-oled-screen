#!/bin/bash

source "$(dirname "$0")"/venv/bin/activate
python3 "$(dirname "$0")"/oled-screen.py "$@"
deactivate
