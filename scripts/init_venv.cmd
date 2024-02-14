@echo off

pushd ..

:PROMPT
set AREYOUSURE=N
set /p AREYOUSURE=This will delete the existing venv and recreate it. Whould you like to procced (Y\[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

echo.
echo Create an empty venv
IF EXIST "venv" rd /s /q venv
python -m venv venv

echo.
echo Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo Upgrade pip
python -m pip install --upgrade pip

echo.
echo Install requirements (excludes linter and build requirements)
pip install -r requirements.txt

echo.
echo Exit without deactivating virtual environment

popd
:END
