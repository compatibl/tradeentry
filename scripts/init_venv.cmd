@echo off

pushd ..

:PROMPT
set CONFIRM=n
set /p CONFIRM="ATTENTION - overwrite existing venv? (y/n)? "
IF /I "%CONFIRM%" NEQ "y" GOTO END

echo.
echo Create an empty venv
IF EXIST "venv" rd /s /q venv
python -m venv venv

echo.
echo Activate venv
call venv\Scripts\activate.bat

echo.
echo Upgrade pip
python -m pip install --upgrade pip

echo.
echo Install requirements (excludes linter and build requirements)
pip install -r requirements.txt

echo.
echo Exit without deactivating venv

popd
:END
