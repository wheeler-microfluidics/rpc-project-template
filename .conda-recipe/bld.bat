@echo off
setlocal enableextensions
md "%PREFIX%"\Library\include\Arduino
md "%PREFIX%"\Library\bin\platformio\rpc-project-template\uno
endlocal

REM Generate Arduino/Python code
"%PYTHON%" -m paver generate_all_code
if errorlevel 1 exit 1
REM Build firmware
"%PYTHON%" -m paver build_firmware
if errorlevel 1 exit 1
REM Copy Arduino library to Conda include directory
xcopy /S /Y /I /Q "%SRC_DIR%"\lib\Dropbot "%PREFIX%"\Library\include\Arduino\Dropbot
REM Copy compiled firmware to Conda bin directory
copy "%SRC_DIR%"\platformio.ini "%PREFIX%"\Library\bin\platformio\rpc-project-template
copy "%SRC_DIR%"\.pioenvs\uno\firmware.hex "%PREFIX%"\Library\bin\platformio\rpc-project-template\uno\firmware.hex
if errorlevel 1 exit 1

REM Generate `setup.py` from `pavement.py` definition.
"%PYTHON%" -m paver generate_setup

REM **Workaround** `conda build` runs a copy of `setup.py` named
REM `conda-build-script.py` with the recipe directory as the only argument.
REM This causes paver to fail, since the recipe directory is not a valid paver
REM task name.
REM
REM We can work around this by wrapping the original contents of `setup.py` in
REM an `if` block to only execute during package installation.
"%PYTHON%" -c "from __future__ import print_function; input_ = open('setup.py', 'r'); data = input_.read(); input_.close(); output_ = open('setup.py', 'w'); output_.write('\n'.join(['import sys', 'import path_helpers as ph', '''if ph.path(sys.argv[0]).name == 'conda-build-script.py':''', '    sys.argv.pop()', 'else:', '\n'.join([('    ' + d) for d in data.splitlines()])])); output_.close(); print(open('setup.py', 'r').read())"

REM Install source directory as Python package.
"%PYTHON%" -m pip install --no-cache .
if errorlevel 1 exit 1
