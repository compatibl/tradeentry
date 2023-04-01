@echo off

pushd ..

echo.
echo Activate virtual environment
call venv\Scripts\activate.bat

echo.
echo Delete dist, build and egg-info directories
if exist cl_runtime.egg-info rmdir/q/s cl_runtime.egg-info
if exist dist rmdir/q/s dist
if exist build rmdir/q/s build

echo.
echo Build wheel
python setup.py bdist_wheel

echo.
echo Exit without deactivating virtual environment

popd
