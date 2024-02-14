@echo off

pushd ..

echo.
echo Format using isort
isort cl --sp=.isort.cfg
isort stubs --sp=.isort.cfg
isort tests --sp=.isort.cfg

echo.
echo Format using black
black -q cl --config=pyproject.toml
black -q stubs --config=pyproject.toml
black -q tests --config=pyproject.toml

popd
