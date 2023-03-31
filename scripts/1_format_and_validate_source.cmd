@echo off

pushd ..

set target=cl
set level=""

call venv\Scripts\activate.bat
echo.
echo Formatting using isort
echo ----------------------------------------
isort %target% --sp=%level%.isort.cfg
echo ----------------------------------------
echo.
echo Formatting using black
echo ----------------------------------------
black %target% --config=%level%pyproject.toml
echo ----------------------------------------
echo.
echo Validating using flake8
echo ----------------------------------------
flake8 %target% --config=%level%.flake8
echo ----------------------------------------

call venv\Scripts\deactivate.bat

popd
