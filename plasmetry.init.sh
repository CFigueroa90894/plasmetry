#! /usr/bin/bash

echo 'LNCH: launching plasmetry...'
cd ~/plasmetry

echo 'LNCH: sourcing venv...'
source g3_env/bin/activate

echo 'starting plasmetry...'
cd ~/plasmetry/src/user_interface/gui_manager
python gui_manager.py

echo 'LNCH: terminating plasmetry...'
deactivate
cd ~/plasmetry
echo 'LNCH: plasmetry exited.'
