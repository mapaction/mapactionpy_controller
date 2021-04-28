:: Windows, Python 2.7
.\env27\Scripts\python.exe -m autopep8 --in-place --max-line-length=120 --recursive . --exclude ./env*
.\env27\Scripts\python.exe -m flake8 --extend-exclude ./env*
.\env27\Scripts\python.exe -m coverage run -m unittest discover .\mapactionpy_controller/tests
:: .\env27\Scripts\python.exe -m coverage run -m unittest discover -p test_plugin_base.py

@REM :: Windows, Python 3.7
@REM .\env37\Scripts\python.exe -m flake8 --extend-exclude ./env*
@REM .\env37\Scripts\python.exe -m unittest discover .\mapactionpy_controller/tests 

@REM :: Windows, Python 3.8
@REM .\env38\Scripts\python.exe -m flake8 --extend-exclude ./env*
@REM .\env38\Scripts\python.exe -m unittest discover .\mapactionpy_controller/tests 

@REM :: WSL, Python 3.8
@REM wsl ./env38wsl/bin/python3 -m unittest discover ./mapactionpy_controller/tests

:: Build coverage report
.\env27\Scripts\python.exe -m coverage html --include="./*" --omit="env*"