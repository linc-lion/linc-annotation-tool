# LINC ANNOTATION TOOL

This project wraps the LINC lion recognition ML model and the Labelimg annotation
tool.

The ML model for this tool was developed in conjunction with Joaquín Alori
 of http://Tryolabs.com

The LabelImg annotation is a solid project from: https://github.com/tzutalin/labelImg


Tested on:
```
	OS Name    Microsoft Windows 10 Pro
	Version    10.0.18362
	Processor  Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz, 2901 Mhz, 2 Core(s), 4 Logical Processor(s)
	Python     version 3.6.4

	OS Name    Debian GNU/Linux 10 (buster)
	Processor  Intel(R) Core(TM) i7-3520M CPU @ 2.90GHz, 2901 Mhz, 2 Core(s), 4 Logical Processor(s)
	Python     version 3.6.4

	Model Performance ~6-12 seconds per image
```

## INSTALL LINC
### 1. --Install Python --
*You can install manually with the command line or try the install scripts, this is a beta project so be patient.*

This will create a new separate version of python from your systems python installation to keep the OS clean. LINC is tested under python 3.6.4.

**LINUX**
Option 1 - Run the `installPython_Linux.sh`file

Option 2 - Use pyenv to set up Python 3.6.4

Option 3 - Do the manual install below

MANUAL INSTALL:
1. Update system and add build tools if needed:

		sudo apt-get update && sudo apt-get install libssl-dev openssl

1. Test your systems python version it should be greater than

		python-3.6 and less than 3.7
		python --version

1. If it is not, get python 3.6.4 (below downloads python 3.6.4) **BE SURE TO INSTALL IN LOCAL USER "~/opt/" DIRECTORY, MAKE IT IF NEEDED!**

		mkdir ~/opt/
		cd ~/opt/
		wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz

1. Change into python directory and build it (WARNING YOU SHOULD NOT
HAVE TO USE ROOT PASSWORD, IT IS A LOCAL INSTALL) CHANGE **YOUR_USER_NAME_HERE** to your user name.

			tar -xzf Python-3.6.4.tgz
			cd Python-3.6.4/
			./configure --prefix=/home/**YOUR_USER_NAME_HERE**/opt/python-3.6.4
			make
			make install

1. Add to your PATH in the .bashrc file in your home '~/' directory.
			#Python 3.6.4
			PATH=$HOME/opt/Python-3.6.4:$PATH

1. Test installation.
		python --version

Should say "python 3.6.4"


**Windows**
		handy tutorial (https://realpython.com/installing-python/#windows)
1. Download the Python 3 Installer for 3.6.4 64 bit
			Open a browser window and navigate to the Download page for Windows at python.org.
			Underneath the heading at the top that says Python Releases for Windows, click on
			the link for Python 3.6.4

			Scroll to the bottom and select either Windows x86-64 executable installer for 64-bit
			or Windows x86 executable installer for 32-bit.

1. Run the Installer
			Once you have chosen and downloaded an installer,
			simply run it by double-clicking on the downloaded file.
			A dialog should appear:

			**Important:** You want to be sure to check the box that says Add Python 3.x to PATH
			to ensure that the interpreter will be placed in your execution path.

			Then just click Install Now. That should be it.
			A few minutes later you should have a working Python 3 installation
			on your system.

1. Add path to your environment - You then may need to add the new python path to your environment to get the commands working:
			Tutorial https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/
			1. Add the path of the python executable to your local path, replace **YOUR_USER_NAME** with your user name
				c:/users/**YOUR_USER_NAME**/appdata/local/programs/python/python36/Scripts



### Download LINC code
**LINUX and WINDOWS**

1. Download LINC

		1.Go to: https://github.com/linc-lion/linc-annotation-tool
		2.Clone with Git or download as a zip file
		3.Under releases on the top of the page download the body_parts_1.pth
		4.Unzip the linc-annotation-tool to a separate directory anywhere in your system, can be the Desktop
		5.Move the body_parts_1.pth to DeployModels directory

1. Download LabelImage code and install in LINC directory
		1.Go to:https://github.com/tzutalin/labelImg
		2.Clone with Git or download as a zip file
		3.Unzip into the linc-annotation-tool-master directory

### Install Python modules and set up virtual env
		Next we create the virtual enviornment and install all the python modules
		in it. Using a virtual env will make sure your main systems python
		libraries are not effected.

**LINUX**

Option 1 - Try to first run the installLINC_Linux.sh file

*! If this gives a error you can try the steps below in terminal:*

**WINDOWS**

Option 1 -Try to first run the installLINC_Windows.bat file
*! If this gives a error you can try the steps below in the windows cmd prompt:*

**LINUX and Windows** (**Change forward / to backslash \ for Windows**)

Option 2 - Manual install you should be able to use the same commands on linux/Windows

		a. Change into LINC directory
			cd /path/to/linc-annotation-master

		b. Update pip
			python -m pip install --upgrade pip

		c. Install virtualenv
			pip install pipenv

		d. Create virtual env
			virtualenv env

		e. Start virtual env
		    (Windows)
			./env/Scripts/activate

			(LINUX)
			source ./env/bin/activate

		f. Install python modules (this will take awhile)
			pip install -r requirement.txt

		g.Create resources.py file for Imagelabel, from linc-annotation-tool-master
			cd labelImg-master
			pyrcc5 -o libs/resources.py resources.qrc

### Run LINC
	Now every time you want to run LINC you should be able to double click on

		runLINC_windows.bat

		        OR

		runLINC_Linux.sh

	and the LINC annotator will start up
