:: Windows, Python 2.7
.\env27\Scripts\python.exe -m autopep8 --in-place --max-line-length=120 --recursive . --exclude ./env*
.\env27\Scripts\python.exe -m flake8 --exclude ./env*
.\env27\Scripts\python.exe -m coverage run -m unittest discover .\mapactionpy_controller/tests
:: .\env27\Scripts\python.exe -m coverage run -m unittest discover -p test_xml_export.py

:: Windows, Python 3.7
:: .\env37\Scripts\python.exe -m flake8 --extend-exclude ./env*
:: .\env37\Scripts\python.exe -m unittest discover .\mapactionpy_controller/tests 

:: Windows, Python 3.8
:: .\env38\Scripts\python.exe -m flake8 --extend-exclude ./env*
:: .\env38\Scripts\python.exe -m unittest discover .\mapactionpy_controller/tests 

:: WSL, Python 3.8
:: wsl ./env38wsl/bin/python3 -m unittest discover ./mapactionpy_controller/tests

:: Build coverage report
.\env27\Scripts\python.exe -m coverage html --include="./*" --omit="env*"