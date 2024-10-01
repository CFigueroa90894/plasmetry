#! /usr/bin/bash

# Adds Plasmetry app to start menu and Desktop
# Assumes plasmetry.desktop exists and is correctly configured
echo 'Adding plasmetry app and desktop shortcut...'
cp ~/plasmetry/.bash_scripts/plasmetry.desktop ~/.local/share/applications/plasmetry.desktop
cp ~/plasmetry/.bash_scripts/plasmetry.desktop ~/Desktop/Plasmetry