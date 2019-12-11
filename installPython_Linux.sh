#!/usr/bin/env bash
#This script installs python 3.6.4 into ~/opt on LINUX

INSTALL_DIR=$HOME/opt/
PYTHON_VERSION=Python-3.6.4
PY_URL=https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz

#If ~/opt/ does not exist
if [[ ! -d $INSTALL_DIR ]]; then
		echo "Making directory $INSTALL_DIR"
		mkdir $INSTALL_DIR
fi
#If dir enter into it and install
if [[ -d $INSTALL_DIR ]]; then
	#Change into dir
	echo "Entering dir"
	cd $INSTALL_DIR
else
	echo "Error:Directory not made aborting"
	exit 1
fi
#Unzip if tgz is present
if [[ -f $PYTHON_VERSION.tgz ]]; then
		echo "tgz file already exists installing"
#Else get python from mirror
elif wget $PY_URL; then 
	echo "Decompressing file...."
	tar -xzf $PYTHON_VERSION.tgz 	#Decompress
else
	echo "Download failed, is there internet?"
	exit 1
fi
#Build python
if [[ -d $PYTHON_VERSION ]]; then
	echo "Building Python"
	cd $INSTALL_DIR$PYTHON_VERSION
	configure --prefix=$HOME/opt/$PYTHON_VERSION 
	if make; then
		make install
	else
		echo "It seems make is not installed try installing:
		sudo apt-get update && sudo apt-get install build-essential libssl-dev openssl"
	fi
fi

