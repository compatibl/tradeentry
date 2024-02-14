@echo off

:PROMPT
set REPOSITORY=""
set /p REPOSITORY="Package repository (pypi or testpypi)? "

echo.
echo Build wheel
call ./build.cmd

pushd ..

echo.
set CONFIRM=n
IF /I "%REPOSITORY%"=="pypi" (
    set /p CONFIRM="ATTENTION - about to publish to pypi (y/n)? "
) ELSE (
    set CONFIRM=y
    echo Publishing to: %REPOSITORY%
)

echo.
IF /I "%CONFIRM%" EQU "y" (
    twine upload -r %REPOSITORY% --verbose -u "__token__" dist/*
) ELSE (
    echo Exiting - publication not approved
)

popd
