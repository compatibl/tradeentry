@echo off

pushd ..

echo.
echo Delete egg-info, build and dist directories before building
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Build wheel
python -m build --wheel

echo.
echo Delete egg-info and build directories after building, wheel is in dist
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"
if exist build rmdir /s /q build

popd
