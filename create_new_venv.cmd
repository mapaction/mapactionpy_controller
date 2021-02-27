
if not exist env27\Scripts\python.exe (cmd /c C:/py27arcgis106/ArcGIS10.6/python.exe -m virtualenv --system-site-packages env27)
if not exist env37\Scripts\python.exe (cmd /c "C:\Program Files\Python37\python.exe" -m virtualenv env37)
if not exist env38\Scripts\python.exe (cmd /c "C:\Program Files\Python38\python.exe" -m virtualenv env38)


:: for %%g in (env27, env37, env38) do (
for %%g in (env27, env37) do (
 %%g\Scripts\python.exe -m pip install --no-cache-dir --no-color -e %~dp0
 %%g\Scripts\python.exe -m pip install -r requirements-jira.txt
 %%g\Scripts\python.exe -m pip install -r requirements-dev.txt
)
:: Install arcmap plugin
.\env27\Scripts\python.exe -m pip install --no-color -e ..\mapactionpy_arcmap

@REM :: py 3.7 on WSL
@REM if not exist env38wsl\bin\python3 (wsl sudo ./install-dependencies-ubuntu.sh)
@REM if not exist env38wsl\bin\python3 (wsl python3 -m virtualenv env38wsl)
@REM :: \\wsl$\Ubuntu-20.04\home\andy
@REM :: wsl ./env38wsl/bin/python3 -m pip install 'GDAL==$(gdal-config --version)'
@REM wsl ./env38wsl/bin/python3 -m pip install --no-cache-dir --no-color -e .
@REM wsl ./env38wsl/bin/python3 -m pip install -r ./requirements-jira.txt
@REM wsl ./env38wsl/bin/python3 -m pip install -r ./requirements-dev.txt

::env27\Scripts\python.exe -m pip install --no-color -e D:\code\github\mapactionpy_controller\
::env37\Scripts\python.exe -m pip install --no-color -e D:\code\github\mapactionpy_controller\
::env38\Scripts\python.exe -m pip install --no-color -e D:\code\github\mapactionpy_controller\
