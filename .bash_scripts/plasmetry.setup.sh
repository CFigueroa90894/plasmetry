#! /usr/bin/bash

echo 'Setting up plasmetry...'

# Check directory exists otherwise create it
[[ -d ~/plasmetry ]] || mkdir ~/plasmetry

# Install dependencies and make venv
. ~/plasmetry/.bash_scripts/plasmetry.reqs.sh

# Add plasmetry app to desktop and start menu
. ~/plasmetry/.bash_scripts/plasmetry.mkdesk.sh
. ~/plasmetry/.bash_scripts/plasmetry.deskadd.sh