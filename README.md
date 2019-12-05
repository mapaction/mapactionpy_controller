About
=====

Master branch [![Build Status](https://travis-ci.org/mapaction/mapactionpy_controller.svg?branch=master)](https://travis-ci.org/mapaction/mapactionpy_controller) [![Coverage Status](https://coveralls.io/repos/github/mapaction/mapactionpy_controller/badge.svg?branch=master)](https://coveralls.io/github/mapaction/mapactionpy_controller?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/2cd96643c21a0cedaa57/maintainability)](https://codeclimate.com/github/mapaction/mapactionpy_controller/maintainability)

Installing
==========
To install the latest stable release via PyPi:
```
python -m pip install mapactionpy_controller
```

To install a specific version for testing see the relevant commandline from here:
https://pypi.org/project/mapactionpy-controller/#history


Commandline Usage
==========
Check the compliance with the Data Naming Convention, MXD Naming Convention, MXD Template Naming Convention and Layer Naming Convetion.
```
> python.exe -m mapactionpy_controller.check_naming_convention /path/to/current/cmf/2019gbr01/cmf_description.json
```


Using the Data Serach tool from the commandline
----
```
> python.exe -m mapactionpy_controller.data_search
usage: data_search [-h] -r FILE -c FILE [-o FILE]
data_search.py: error: the following arguments are required: -r/--recipe-file, -c/--cmf

> python -m mapactionpy_controller.data_search -r example/product_bundle_example.json -c example/cmf_description.json
```
This command will output an updated recipe file with the 
If the ouput file parameter (-o) is specified than the updated recipe will be output to that file. Otherwise the updated recipe is sent to stdout.


Programmatic Usage
=====
Using the MapRecipe, CrashMoveFolder and Event classes
----
There are three classes which are designed for reuse in other modules. For each of these there is a corresponding json representation. There should not be any need for any other code to touch these json files:

* **MapRecipe** : An object that represents a recipe (as read from a json file).  
This object may be manipulated by 
(e.g. the data_search tool, updates the datasources fields )
* **CrashMoveFolder** : An object that describes the CrashMoveFolder and its contents. There should be no need to hardcode any path (absolute or relative) to anywhere in a crash move folder
* **Event** : This decribes the real-world humanitarian event to which the Crash Move Folder corresponds.

(**Note1:**) The name `Event` matches the naming of the equivalent concept on the Map & Data Respository (see https://github.com/mapaction/ckanext-mapactionevent). However it is rather too generic in this context. A more descriptive name for this class would be helpful.

(**Note2**: in the MapExportTool the information within the CrashMoveFolder and Event used to be encapsulated in the `operational_config.xml` file. This mixed _state_ about the event/emergency and _configuration_ about the local paths to and within the crash move folder.  )


Using the DataNameConvention and related classes
----
The `naming_convention` sub-module provides a framework for specifying a naming convention (such as for file or table). A naming convention is specified in a json configuration file and consists of:
1) A regular expression, with named groups
2) For each named group in the regex, details of a class which can provide futher validation of that value in that named group.

Exmples of the naming convention config files are in the `examples` directory, including MapAction's DataNamingConvention, MXDNamingConvention and LayerfileNamingConvention.

**DataNameConvention** represents the _convention_ itself. At its core is a regular expression. Each named group (clause) within the Regex as additionally validation, which is implemented by a DataNameClause. DataNameConvention has a dictionary of DataNameClause objects. A individual name is tested by using the `.validate(data_name_str)` method. If the data name does not match the regex the value None is returned. If the regex matches a DataNameInstance object will be returned, whether or not all of the clauses pass.

**DataNameClause** is an abstract class. Callers are unlikely to need to directly access this class or any concrete examples. Concrete examples are DataNameFreeTextClause and DataNameLookupClause. When the `.validate(data_name_str)` method is called on a DataNameConvention object, it will call `.validate(clause_str)` in each individual DataNameClause obj. 

**DataNameResult** represents the _result_ of a specific data name test and is returned by `DataNameConvention.validate()`. The `.is_valid` property indicates whether or not all of the clauses validate. DataNameResult is a [namedtuple](https://docs.python.org/2.7/library/collections.html#collections.namedtuple).
The values for individual clauses can be directly accessed using dotted property notation (eg  via members such as  `dnr.datatheme.Description` or `dnr.source.Organisation`. If whether or not the clause validated is returned by the `.is_valid` property (eg . `dnr.datatheme.is_valid`).

Example code:
```
dnc = DataNameConvention(path_to_dnc_json_definition)

# regex does not match
dnr = dnc.validate('abcde')
self.assertIsNone(dnr)

# regex does matches, but some clauses fail lookup in csv file
dnr = dnc.validate(r'aaa_admn_ad3_py_s0_wfp_pp')

if dnr.is_valid:
	print('the dataname is valid')
else:
	print('the dataname is not valid')
	
# use the `_asdict()` method to loop through all clauses
for clause in dnr._asdict().values():
	clause_details = dni.clause(clause)
	if clause_details:
		print('The extra information associated with clause name {} are {}'.format(clause, clause_details)
	else:
		print('The erroneous value for clause {} was {} '.format(clause, clause_details)

# Use the dnr object in template strings
print('The {dnr.datatheme.Description} data was generously supplied by {dnr.source.Organisation}, downloaded '
	'from {dnr.source.url}'.format(dnr=dnr))
```
Output:
```
The erroneous value for clause `geoext` was `aaa`
Extra information associated with clause `scale`:
    Description = Global mapping
    Scale_range = ? 5 000 000
Extra information associated with clause `freetext`:
    text = None
Extra information associated with clause `perm`:
    Description = Data public - Products public
Extra information associated with clause `source`:
    url =
    Organisation = World Food Program
    admn1PCode =
    admn2Name =
    admn2PCode =
    admn1Name =
Extra information associated with clause `datacat`:
    Description = Admin
Extra information associated with clause `geom`:
    Description = Polygon / area
Extra information associated with clause `datatheme`:
    Category = admn
    Description = Administrative boundary (level 3)


The Administrative boundary (level 3) data was generously supplied by World Food Program, downloaded from https://www.wfp.org/
```
