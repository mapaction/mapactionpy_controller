About
=====

Master branch [![Build Status](https://travis-ci.org/mapaction/mapactionpy_controller.svg?branch=master)](https://travis-ci.org/mapaction/mapactionpy_controller)

Installing
==========
To install for development purposes:
Clone the github repo then from the root of your local clone:
```
python -m pip install --user -e .
```

To install for use non-development purposes:
Clone the github repo then from the root of your local clone:
```
python -m pip install .
```

todo:
[] enable installation via pypi.


Usage
=====
Using the MapRecipe, CrashMoveFolder and Event classes
----
There are three classes which are designed for reuse in other modules. For each of these there is a corresponding json representation. There should not be any need for any other code to touch these json files:

* **MapRecipe** : An object that represents a recipe (as read from a json file).  
This object may be manipulated by 
(eg the data_search tool, updates the datasources fields )
* **CrashMoveFolder** : An object that describes the CrashMoveFolder and its contents. There should be no need to hardcode any path (absolute or relevate) to anywhere in a crash move folder
* **Event** : This decribes the real-world humanitarian event to which the Crash Move Folder cooresponds.

(**Note1:**) The name `Event` matches the naming of the equivilent concept on the Map & Data Respository (see https://github.com/mapaction/ckanext-mapactionevent). However it is rather too generic in this context. A more decriptive name for this class would be helpful.

(**Note2**: in the MapExportTool the information within the CrashMoveFolder and Event used to be encapsulated in the operational_config.xml file. This mixed _state_ about the event/emergency and _configuration_ about the local paths to and within the crash move folder.  )


Using the Data Serach tool from the commandline
----
```
> python.exe data_search.py
usage: data_search.py [-h] -r FILE -c FILE [-o FILE]
data_search.py: error: the following arguments are required: -r/--recipe-file, -c/--cmf
> python data_search.py -r example/product_bundle_example.json -c example/cmf_description.json
```
This command will output an updated recipe file with the 
If the ouput file parameter (-o) is specificed than the updated recipe will be output to that file. Otherwise the updated recipe is sent to stdout.

Tests
=====
The test coverage appears OK (~86%). However this risks overstating the effectiveness of these tests with only a few error conditions included at present.


Further development
===================
In no particular order:

 [] Improve the constructors for the main state classes. It should be possible to round-robin between the instance and the json representation. eg there should be tests which look something like this:
```
    assert my_recipe == MapRecipe.fromJOSN(my_recipe>toJSON())
```   
The `jsonpickle` module is particularly well suited for this.

 [] Implenment json schema validation for the various json files.

 [] CrashMoveFolder class should check for the existance of all of the subdirectories in the constructor.

 [] Replace debug print statements with output to a logging libaray - to ensure that standard output is not corrupted with error/debug messages.

 [] Better name for the `Event` class
