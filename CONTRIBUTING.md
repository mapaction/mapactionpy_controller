Contributing
============
To install for development purposes:
Clone the github repo then from the root of your local clone:
```
python -m pip install --user -e .
```

Tests
=====
Please accompany any contribution with relevant unittests or integration tests. Two scripts exist to help with local testing

`create_new_venv.cmd`
--------
This creates a number of virtual envs covering key target environments. 

The following environments already exist on the development computer:
* Python 2.7, 32bit (with arcpy) installed `C:/py27arcgis106/ArcGIS10.6/python.exe`
* Python 3.7, 64bit installed `"C:\Program Files\Python37\python.exe"`
* Python 3.7, 64bit installed `"C:\Program Files\Python38\python.exe"`
* Ubuntu 18.04 LTS on Windows Subsystem for Linux with python 3.8 (Ubuntu 20.4 is not supported)

Additionally
* The package `virtualenv` must be installed in each of the python environments above
* The source for `mapactionpy_arcmap` must be cloned in the same parent directory as `mapactionpy_controller`. (ie so that is it possible to reach using `../mapactionpy_arcmap`).

This script is only run occasionally to (re)create the test environments.

`all-tests.cmd`
--------
This script runs linting and unittests for each of the environments established by `create_new_venv.cmd`. It also creates a local coverage report in './htmlcov/index.html'.

This script is indented to be run regularly during development.


Further development
===================
In no particular order:

 [] Improve the constructors for the Event and CrashMoveFolder classes. It should be possible to round-robin between the instance and the json representation. eg there should be tests which look something like this:
```
    assert my_event == Event.fromJSON(my_event.toJSON())
    assert my_cmf == CrashMoveFolder.fromJOSN(my_cmf.toJSON())
```
The `jsonpickle` module is particularly well suited for this.

 [] Implement json schema validation for the various json files.

 [] Replace debug print statements with output to a logging library - to ensure that standard output is not corrupted with error/debug messages.

 [] Better name for the `Event` class

 [] Use explict class names for validator in the Naming Convention config files.

 [] Document the process of creating the Naming Convention classes for validating specific clause types.
