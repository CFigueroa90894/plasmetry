#! /usr/bin/bash

echo 'Setting up plasmetry...'

# Check directory exists otherwise create it
[[ -d ~/plasmetry ]] || mkdir ~/plasmetry

# Install dependencies and make venv
. ~/plasmetry/.setup_scripts/plasmetry.reqs.sh

# Add plasmetry app to desktop and start menu
. ~/plasmetry/.setup_scripts/plasmetry.mkdesk.sh
. ~/plasmetry/.setup_scripts/plasmetry.deskadd.sh

# Make init executable
chmod +x ~/plasmetry/plasmetry.init.sh
