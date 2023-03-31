@echo off

pushd ..

:PROMPT
set AREYOUSURE=N
set /p AREYOUSURE=This will delete current venv and recreate it. Whould you like to procced (Y\[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

echo Create empty venv
IF EXIST "venv" rd /s /q venv
python -m venv venv

rem Activate virtual environment:
call venv\Scripts\activate.bat

echo Installing requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

call venv\Scripts\deactivate.bat

popd
:END
