#! /usr/bin/bash

echo 'Locating user home folder...'
home="$HOME"
rel_path="/plasmetry/.bash_scripts/plasmetry.init.sh"
abs_path=$home$rel_path
exec="Exec="$abs_path
echo $exec > tmp

echo 'Creating desktop file...'
cat ~/plasmetry/.bash_scripts/plasmetry.blankdesk tmp > ~/plasmetry/.bash_scripts/plasmetry.desktop
rm tmp