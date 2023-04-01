@echo off

pushd ..

:PROMPT
set AREYOUSURE=N
set /p AREYOUSURE=This will delete current venv and recreate it. Whould you like to procced (Y\[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

echo.
echo Create empty venv
IF EXIST "venv" rd /s /q venv
python -m venv venv

echo.
echo Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo Upgrade pip, install the latest setuptools and wheel
python -m pip install --upgrade pip
pip install setuptools
pip install wheel

echo.
echo Install requirements
pip install -r requirements.txt

echo.
echo Exit without deactivating virtual environment

popd
:END
