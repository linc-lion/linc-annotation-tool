This project wraps the LINC lion recognition ML model and the labelimg annotation
tool. 

The tool uses the labelImg annotation tool for verification after the models run, 
it is a great project from:
	https://github.com/tzutalin/labelImg

The labelimg git directory has been disabled though to provide easier deployment for
the conservationists avoiding submodules.

Installation:
1. Update your system python version to latest version > 3.7
2. Clone or download the code base to desired directory
3. Change into 

4. Use pipenv to install and run:
```
	Something goes wrong: pipenv --rm

	Debian:
 	 	pip install -U pipenv

	Install python 3.7
		pipenv install --python 3.7
	Enter into env
		pipenv shell
	Install dependancies
		pipenv install --ignore-pipfile
```

