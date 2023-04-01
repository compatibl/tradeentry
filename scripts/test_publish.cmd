@echo off

:PROMPT
set PYPIUSER=""
set /p PYPIUSER=User for Test PyPI?

:PROMPT
set PYPIPASS=""
set /p PYPIPASS=Password for Test PyPI?

echo.
echo Build wheel
call ./build_wheel.cmd

pushd ..

echo.
echo Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo Publish to Test PyPI
twine upload -r testpypi --verbose -u %PYPIUSER% -p %PYPIPASS% dist/*

echo.
echo Exit without deactivating virtual environment

popd
