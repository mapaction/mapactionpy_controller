About
=====

Master branch [![Build Status](https://travis-ci.com/mapaction/mapactionpy_controller.svg?branch=master)](https://travis-ci.com/mapaction/mapactionpy_controller) [![Coverage Status](https://coveralls.io/repos/github/mapaction/mapactionpy_controller/badge.svg?branch=master)](https://coveralls.io/github/mapaction/mapactionpy_controller?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/2cd96643c21a0cedaa57/maintainability)](https://codeclimate.com/github/mapaction/mapactionpy_controller/maintainability)

Installing
==========
To install the latest stable release via PyPi:
```
python -m pip install mapactionpy_controller
```

To install a specific version for testing see the relevant command line from here:
https://pypi.org/project/mapactionpy-controller/#history


Command-line Usage
==========
There are two key files `cmf_description.json` and `event_description.json` that are in the root of the crash move folder. Most command line options require one or the other of these.

General help:
```
> mapchef --help
```

Verify the content of the default crash move folder (eg MXD Naming Convention, MXD Template Naming Convention, Layer Naming Convention and self consistency of various configuration files.):
```
> mapchef defaultcmf --verify c:/path/to/default/crash/move/folder/cmf_description.json
```

Check the compliance with the Data Naming Convention.
```
mapchef gisdata --verify /path/to/current/cmf/2019gbr01/event_description.json
```

Create all maps in the cookbook file:
```
mapchef maps --build /path/to/current/cmf/2019gbr01/event_description.json
```

Create the map "MA001" from the cookbook file:
```
mapchef maps --build --map-number "MA001" /path/to/current/cmf/2019gbr01/event_description.json
```

Programmatic Usage
=====
Using the MapRecipe, CrashMoveFolder and Event classes
----
There are three classes which are designed for reuse in other modules. For each of these there is a corresponding json representation. There should not be any need for any other code to touch these json files:

* **MapRecipe** : An object that represents a recipe (as read from a json file).  
This object may be manipulated by 
(e.g. the data_search tool, updates the `datasources` fields )
* **CrashMoveFolder** : An object that describes the CrashMoveFolder and its contents. There should be no need to hardcode any path (absolute or relative) to anywhere in a crash move folder
* **Event** : This describes the real-world humanitarian event to which the Crash Move Folder corresponds.

(**Note1:**) The name `Event` matches the naming of the equivalent concept on the Map & Data Repository (see https://github.com/mapaction/ckanext-mapactionevent). However it is rather too generic in this context. A more descriptive name for this class would be helpful.

(**Note2**: in the MapExportTool the information within the CrashMoveFolder and Event used to be encapsulated in the `operational_config.xml` file. This mixed _state_ about the event/emergency and _configuration_ about the local paths to and within the crash move folder.  )


Using the DataNameConvention and related classes
----
The `naming_convention` sub-module provides a framework for specifying a naming convention (such as for file or table). A naming convention is specified in a json configuration file and consists of:
1) A regular expression, with named groups
2) For each named group in the regex, details of a class which can provide further validation of that value in that named group.

Examples of the naming convention config files are in the `examples` directory, including MapAction's DataNamingConvention, MXDNamingConvention and LayerfileNamingConvention.

**DataNameConvention** represents the _convention_ itself. At its core is a regular expression. Each named group (clause) within the Regex as additionally validation, which is implemented by a DataNameClause. DataNameConvention has a dictionary of DataNameClause objects. A individual name is tested by using the `.validate(data_name_str)` method. If the data name does not match the regex the value None is returned. If the regex matches a DataNameInstance object will be returned, whether or not all of the clauses pass.

**DataNameClause** is an abstract class. Callers are unlikely to need to directly access this class or any concrete examples. Concrete examples are DataNameFreeTextClause and DataNameLookupClause. When the `.validate(data_name_str)` method is called on a DataNameConvention object, it will call `.validate(clause_str)` in each individual DataNameClause obj. 

**DataNameResult** represents the _result_ of a specific data name test and is returned by `DataNameConvention.validate()`. The `.is_parsable` property indicates whether or not the name could be parsed by the DataNameConvention's regex. The `.is_valid` property indicates whether or not _all_ of the clauses validate. (`.is_valid` will always be `False` if `.is_parsable` is `False`). DataNameResult is a [namedtuple](https://docs.python.org/2.7/library/collections.html#collections.namedtuple).
The values for individual clauses can be directly accessed using dotted property notation (eg  via members such as  `dnr.datatheme.Description` or `dnr.source.Organisation`. Each individual clause will have its own `.is_valid` property (eg . `dnr.datatheme.is_valid`).

Example code:
```
dnc = DataNameConvention(path_to_dnc_json_definition)

# regex does not match
dnr = dnc.validate('abcde')
self.assertFalse(dnr.is_parsable)

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

Licence
=====


A number of third party packages are bundled with the distribution of `mapactionpy_controller`. These are stored in the
folder `dependency_wheels` and are included purely to simplify the experience of those installing `mapactionpy_controller` 
via `pip`. We are grateful for the excellent of these projects and do not claim either copyright or credit for their work. 
Nor do we claim any endorsement from their authors for `mapactionpy_controller`.

The wheel files used are sourced from Christoph Gohlke's "Unofficial Windows Binaries for Python Extension Packages"
https://www.lfd.uci.edu/~gohlke/pythonlibs/ They come with the following disclaimer:
"The files are provided "as is" without warranty or support of any kind. The entire risk as to the quality and performance is with you."

pyproj 
----
https://github.com/pyproj4/pyproj

Author's copyright notice:
> Copyright (c) 2006-2018, Jeffrey Whitaker.
> Copyright (c) 2019-2020, Open source contributors.
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy of
> this software and associated documentation files (the "Software"), to deal in
> the Software without restriction, including without limitation the rights to use,
> copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
> Software, and to permit persons to whom the Software is furnished to do so,
> subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in all
> copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
> INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
> PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
> HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
> OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
> SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Shapely
----
https://github.com/Toblerity/Shapely

Author's copyright notice:
> Copyright (c) 2007, Sean C. Gillies
> All rights reserved.
> 
> Redistribution and use in source and binary forms, with or without
> modification, are permitted provided that the following conditions are met:
> 
> * Redistributions of source code must retain the above copyright
>   notice, this list of conditions and the following disclaimer.
> * Redistributions in binary form must reproduce the above copyright
>   notice, this list of conditions and the following disclaimer in the
>   documentation and/or other materials provided with the distribution.
> * Neither the name of Sean C. Gillies nor the names of
>   its contributors may be used to endorse or promote products derived from
>   this software without specific prior written permission.
> 
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
> AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
> IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
> ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
> LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
> CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
> SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
> INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
> CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
> ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
> POSSIBILITY OF SUCH DAMAGE.

