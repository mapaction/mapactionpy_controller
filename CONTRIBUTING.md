Contributing
============
To install for development purposes:
Clone the github repo then from the root of your local clone:
```
python -m pip install --user -e .
```

Tests
=====
Please accompany any contribution with relevant unittests or integration tests.


Further development
===================
In no particular order:

 [] Improve the constructors for the Event and CrashMoveFolder classes. It should be possible to round-robin between the instance and the json representation. eg there should be tests which look something like this:
```
    assert my_event == Event.fromJOSN(my_event.toJSON())
    assert my_cmf == CrashMoveFolder.fromJOSN(my_cmf.toJSON())
```   
The `jsonpickle` module is particularly well suited for this.

 [] Implement json schema validation for the various json files.

 [] Replace debug print statements with output to a logging library - to ensure that standard output is not corrupted with error/debug messages.

 [] Better name for the `Event` class

 [] Use explict class names for validator in the Naming Convention config files. 

 [] Document the process of creating the Naming Convention classes for validating specific clause types. 


