#!/usr/bin/env bash

INSTALL_DIR=$HOME/opt/
PYTHON_VERSION=Python-3.6.4
##EDIT ABOVE HERE#####################

PYTHON_PATH=$INSTALL_DIR$PYTHON_VERSION
export PATH=$PYTHON_PATH:$PATH
export PATH=$PYTHON_PATH/bin:$PATH
PYTHON=$PYTHON_PATH/python

echo --Script to install LINC on Linux--
echo Using python version: $(which python)

if  [ ! $PYTHON -ef $(which python) ]; then
	echo "$PYTHON_VERSION does not seem to be installed, please run the
	installPython_Linux.sh script, manually install or change the
	INSTALL_DIR path in this script to run python-3.6.4"
	exit 1
fi

#upgrade pip install virtualenv
echo $(python -m pip install --upgrade pip);
echo $(python -m pip install virtualenv);

#If successful activate virtual env and install reqs
COMMAND="virtualenv --version";
if $COMMAND; then
	echo "virtualenv command is present at version: $($COMMAND)"
	echo $(which virtualenv)
else
	echo "virtualenv did not get installed correctly please try the manual 
	install instructions"
	exit 1
fi

START_VIR_ENV="source $PWD/env/bin/activate" 
INSTALL_MOD="pip3 install -r $PWD/requirements.txt"
ACTIVATE_PYQT5="pyrcc5 -o libs/resources.py resources.qrc"
if [[ -d $PWD/env ]]; then
	echo "Virtual environment has already been created...
	to do a clean install delete the env/ directory 
	and run script again."
	echo "Installing modules, it could take awhile."
	$START_VIR_ENV \
	&& echo $(which pip)\
	&& pip list \
	&& $INSTALL_MOD \
	&& cd $PWD/labelImg-master/ \
	&& $ACTIVATE_PYQT5 \
	&& pip list
else
	#create virtual env
	echo "Creating new virtual environment...."
	echo $(virtualenv env) 
	echo "Installing modules, it could take awhile."
	$START_VIR_ENV \
	&& pip list \
	&& $INSTALL_MOD \
	&& cd $PWD/labelImg-master/ \
	&& $ACTIVATE_PYQT5 \
	&& pip list
fi

exit 0
