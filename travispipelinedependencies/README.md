Installing
==========

During a Travis CI build, these dependencies will be installed as part of the setup process and declared in the .travis.yml file. 
We store them locally to avoid issues related to fetching them from online sources.

These wheel files ensure that the correct dependencies are installed manually via pip. 
GDAL is notoriously difficult to install via pip without using wheel files from https://www.lfd.uci.edu/~gohlke/pythonlibs/.

The order in which these dependencies are installed is important.

Future Notes
==========

It would be beneficial to update these wheels as they are quite old. 
The reason for using them is to ensure they match the mapy-dependencies39 PyPI package and are the same as the ones we have been installing with our toolbar.

Toolbar in 2023
==========

The current method of toolbar installation clones the default ArcPro environment, obtaining an up-to-date version of the GDAL library. 
The installation method where mapy-dependencies39 (where 39 represents Python version 3.9) might become obsolete. This is to be tested.


