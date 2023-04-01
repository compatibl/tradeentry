@echo off

:PROMPT
set PYPIUSER=""
set /p PYPIUSER=User for ***PROD*** PyPI?

:PROMPT
set PYPIPASS=""
set /p PYPIPASS=Password for ***PROD*** PyPI?

echo.
echo Build wheel
call ./build_wheel.cmd

pushd ..

echo.
echo Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo Publish to Test PyPI
twine upload -u %PYPIUSER% -p %PYPIPASS% dist/*

echo.
echo Exit without deactivating virtual environment

popd
