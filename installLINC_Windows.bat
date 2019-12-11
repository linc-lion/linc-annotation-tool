@echo off
Echo --Script to install LINC on Windows 10--
Rem upgrade pip install virtualenv
python -m pip install --upgrade pip && pip install pipenv
Rem if successful activate virtual env and install reqs
WHERE virtualenv
IF %ERRORLEVEL% NEQ 0 (
  ECHO --Virtualenv did not install correctly-- & exit /b 1
)
ECHO --Creating virtual env:--
IF EXIST %~dp0\env\ (
  ECHO --Virtual env exists to do a clean install, delete the env directory and run this script again--
  cmd /C "%~dp0\env\Scripts\activate && cd /d %~dp0 && pip install -r %~dp0\requirements.txt"
  pause
) else (
  ECHO --Creating new virtual env--
  virtualenv %~dp0\env\
  cmd /C "%~dp0\env\Scripts\activate && cd /d %~dp0 && pip install -r %~dp0\requirements.txt"
  pause
)
ECHO --Package Check:
cmd /C "%~dp0\env\Scripts\activate && pip list"
pause
ECHO Set up PyQt5
pause
ECHO --Creating PyQt5 resourcesfile.py--
cmd "/C %~dp0\env\Scripts\activate && cd /d %~dp0\labelImg-master\ && pyrcc5 -o libs/resources.py resources.qrc"
ECHO there should be a new file resources.py in labelimg-master/lib/resources.py
pause
