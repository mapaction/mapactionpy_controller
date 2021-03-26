Contributing
============
To install for development purposes:
Clone the github repo then from the root of your local clone:
```
python -m pip install --user -e .
```

Python versions
============
In order to support the `mapactionpy_arcmap` and `mapactionpy_qgis` plugins, both Python 2 and 3 need to be support by the controller. Currently all code (including tests) is tested on these versions of Python:

* Python 2.7 Windows 32 bit
* Python 3.6 Windows 64 bit
* Python 3.6 Linux 64 bit
* Python 3.7 Windows 64 bit
* Python 3.7 Linux 64 bit

Individal plugins do not need to support all of these.

The `six` module has been helpful for handling cases where the syntax or the dependencies differ. See [examples](https://github.com/mapaction/mapactionpy_controller/search?q=six).

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


Self-review of the current code base 
===================

The remainer of this doc includes a general introduction to the code base. It is devided by the conceptual areas of functionality. For each it highlights the relevant files, a description of the functionality and the known weaknesses and future ideas.

## Main Stack

_**Relevant files**_
`steps.py` and `main_stack.py`

_**Functionality**_
* Step class, which is a wrapper for:
    * A function to run (which must accept `kwargs**`).
    * Defines a “running” “success” and “failure” message.
    * How sever failure of the function would be.
* The key function in `main_stack.py` is `process_stack()`:
    * This is the “main loop”, which works through a list of “Step” objects.
    * Each step may return:
        * One or more new Step objects (which are inserted into the slack). Closures are very useful here.
        * An updated state object (which will passed to the next step).
* Note: main_stack.py also includes humanfriendly.terminal which is really part of the CLI

_**Known weaknesses and future ideas**_
> Either 
> * Improve the clarity about the expectations of the kwargs** that are passed to step.func and the values it can return.
> 
> Or:
> * Completely replace with a DAG from Dagster or similar framework.

## Commandline Interface
_**Relevant files**_
`cli.py`' and `main_stack.py` (the later only for minor details)

_**Functionality**_
* Mostly a wrapper for argparse
* Uses “noun” and “verb” combinations
  * Current nouns are “defaultcmf”, “humevent”, “gisdata” and “maps”
  * Current verbs are 'build', 'create', 'list', 'update', 'upload', and 'verify'
* Generally each combination will call a function that generates an initial list of “Step” objects using the commandline args (typically wrapped in closures). And then starts the main_stack.
* Some combinations will raise `NotImplementedError`

_**Known weaknesses and future ideas**_
> Complete the combinations which current which raise NotImplementedError
> Enable plugins to extend the CLI by added additional noun, verb combinations.


## Crash Move Folder and Event management

_**Relevant files**_
`crash_move_folder.py`, `data_search.py` and `event.py`

_**Functionality**_
* The "Crash Move Folder" (CMF) is a directory stucture used by MapAction in its operations. It is generally "atomic", meaning that all of the data, maps, products, etc relating to a particular humanitarian response in included in the CMF. The is human and machine readable. 
* “Event” is a poor choice of class name as it can mean soooo many things, (particularly in OO or Event driven programing). I wish I had used HumEvent instead, but I haven’t gone back and changed it.
* The CMF and Event json files are called “cmf_description.json” and “event_description.json” by convention only. The should not be anywhere (except tests) where this is hardcoded.
* The “cmf_description.json” contains key value pairs indicating the _relative_ path to each of the subdirectories of the CMF. The CrashMoveFolder class should resolve all of these to absolute path and (by default) should ensure that each of the subdirectories and files references exist.
* There are “cmf-v0.2.schema” and “event-v0.2.schema” files, which is distributed with the package and are enforced using `jsonschema`. This is used to ensure that any future changes to the schema of the objects can be mapped to the relevant config files and will enable support for backward compatibility. It is legitimate (and encouraged) to hardcode references to these schema files.
* data_search.py is here for want of somewhere better.


_**Known weaknesses and future ideas**_
> “Event” is a poor choice of class name as it can mean soooo many things, (particularly in OO or Event driven programing). "HumEvent" (short for HumanitarianEvent) might have been a better choice instead, but it is unclear if it is worth going back and changing it.
>
> At present it is only possible to create an “event_description.json” on disk and use it to instanciate an Event object. It would be useful to be able to create an Event object in code and write out the config file.


## Recipes and Layer Properties

_**Relevant files**_
`config_verify.py`, `data_schemas.py`, `label_class.py`, `layer_properties.py`, `map_cookbook.py`, `map_recipe.py`, and `recipe_atlas.py`

_**Functionality**_
* Reading in json files is reinforced by config json.schema files.
* The hierarchy of objects:
```
MapCookbook
 \-MapRecipe (1, many)
    |-RecipeAtlas(0, 1)
    \-RecipeFrame (1, many)
       \-RecipeLayer (1, many)
          |-LabelClass (0, many)
          \-Data schema (0, 1)

The numbers in () are min and max permitted numbers of each object
```
* Recipes and Layer Properties can be regarded as two tables in 3NF. Joined at point of reading files. (“layername” is primary key in LyrProps and foreign key in Recipe).
* Round-robin serialisation and optional fields - mean that these classes can (and should) be used as a state object.
* `config_verify.py` merely checks for self-consistency

_**Known weaknesses and future ideas**_
> Would like to separate MapCookbook into multiple files.


## File Naming Conventions

_**Relevant files**_
`check_naming_convention.py`, `name_clause_validators.py` and `name_convention.py`

_**Functionality**_
* The code only encapculates generic naming convention classes. The MapAction “Data Naming Convention”, (along with “mxd naming convention”, “layerfile naming convention”, “pdf naming convention” etc) exist only as configuration files.
* A convention must have a regex which devides the name into multiple cluases and then a means to test each individual clause.
* Current it can enforce CSV lookup based clauses and freetext clauses.
* The code makes heavy use of “named tuples” - not sure I would do that again.


_**Known weaknesses and future ideas**_
> Create a Clause Validator to test geometry clauses for shapefiles/feature clauses.
> 
> Create a Clause Validator to test the version number clauses for MXDs.


--------------------------------------

## Generic Exporter

_**Relevant files**_
`data_source.py`
`map_data.py`
`map_doc.py`
`map_report.py`
`map_result.py` and 
`xml_exporter.py`

_**Functionality**_
* Handles export of metadata related to maps, for onward distribution. 
* A lot of this was migrated (with minimal changes) from the earlier versions of ArcMap automation plugin.

_**Known weaknesses and future ideas**_
> Refactor and improve unit testing coverage
> There is some stale code in this section that should be removed.
> Align names with the rest of the mapactionpy_contoller


## Plugin Interface

_**Relevant files**_
`plugin_base.py` and
`plugin_controller.py`

_**Functionality**_
* Plugins are dynamically loaded, but the names of potential plugins are currently hardcoded into mapactionpy_controller. 
* `BaseRunnerPlugin` is an abstract implementation (but without using the abs module). It contains a number of methods, some of these are implemented, and some of which raise `NotImplementedError` (See https://stackoverflow.com/a/25300153). A plugin should subclass BaseRunnerPlugin and override the methods which raise NotImplementedError.
* Separation of "what lives within mapactionpy_controller" vs "what lives in mapactionpy_arcmap" modules has largely been driven by isolating any classes/methods that have direct dependencies on arcpy into mapactionpy_arcmap and everything else into the controller. There has not been a more purposeful API design process for this.

_**Known weaknesses and future ideas**_
> Improved registration of plugins
> 
> Better design of the separation of duties between the controller and the plugin


## Tasks and JIRA

_**Relevant files**_
`jira_tasks.py` and
`task_renderer.py`

_**Functionality**_
* There is a hook in the main stack that allows an interaction with JIRA for each Step object processed. The action can be to create a new task or to comment on, move or close an existing task.
* Rich text templating for JIRA markup is done using mustache.io. Custom delimiters are used because `{{` and `}}`  have different reserved meanings in mustache.io and JIRA markup.
* Relevant python packages (jira) are not included in requirement.txt or setup.py. Also if the jira module is absent, then jira integration is passed over gracefully. This is to accommodate home users who do not want/need to setup JIRA integration.
* (as of v1.1) `TaskReferralBase` is an abstract class. Each subclass represents a category of problems (eg FixDataNameTask, FixSchemaErrorTask). Instances of these classes represent individual problems (eg file `foo` is misnamed. File `bar` has the wrong schema).


_**Known weaknesses and future ideas**_
> Make it easier to propagate the contextual information about the error condition that occured to the task_renderer. 
>
> Examine whether or not the one-to-one relationship between a Step and the opportunity to interact with a task is appropriate. If not what should replace it? Would it be better to make `TaskReferralBase` a custom Exception type instead?
>
> Plugins could extend the list of scenarios that result in a JIRA task
>
> Ideally isolate JIRA specific dependencies from general task handling.


-- END --