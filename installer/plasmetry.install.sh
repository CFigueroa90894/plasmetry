#! /usr/bin/bash

echo 'Downloading Plasmetry - RPIplate CM4 DAQC2plate...'
cd ~/
git clone -b rpiplasmaplate git@github.com:CFigueroa90894/plasmetry.git

echo 'Running setup...'
. ~/plasmetry/.setup_scripts/plasmetry.setup.sh
cd ~
