#! /usr/bin/bash

echo 'Creating plasmetry virtual python environment...'
cd ~/plasmetry

python -m venv g3_env --system-site-packages

source g3_env/bin/activate

echo 'Installing dependecies...'
pip install -r .setup_scripts/plasmetry.requirements

echo 'Dependencies satisfied.'
deactivate
