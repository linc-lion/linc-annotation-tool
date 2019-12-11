#!/usr/bin/env bash

if [[ ! -f $PWD/env/bin/activate ]]; then
	echo "Virtual env does not seem to be installed, please install"
	exit 1
fi
source $PWD/env/bin/activate
cd $PWD
python ui_main.py
