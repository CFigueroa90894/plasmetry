#! /usr/bin/bash

echo 'Locating user home folder...'
home="$HOME"
dsk_path="/plasmetry/plasmetry.init.sh"
ico_path="/plasmetry/.setup_scripts/g3_lowres.png"
exec="Exec="$home$dsk_path
icon="Icon="$home$ico_path


echo 'Creating desktop file...'
echo $icon > ico
echo $exec > exe
cat ico exe > tmp

cat ~/plasmetry/.setup_scripts/plasmetry.blankdesk tmp > ~/plasmetry/.setup_scripts/plasmetry.desktop

rm ico
rm exe
rm tmp
