@echo off

pushd ..

set target=cl
set level=""

echo.
echo Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo Format using isort
isort %target% --sp=%level%.isort.cfg

echo.
echo Format using black
black -q %target% --config=%level%pyproject.toml

echo.
echo Validate using flake8
flake8 %target% --config=%level%.flake8

echo.
echo Exit without deactivating virtual environment

popd
