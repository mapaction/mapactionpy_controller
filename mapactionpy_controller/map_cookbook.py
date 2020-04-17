from mapactionpy_controller.map_recipe import MapRecipe
import json


class MapCookbook:
    """
    MapCookbook - Contains recipes for Map Products   
    """

    def __init__(self, cmf, layer_props, verify_on_creation=True):
        """
        Sets path for Map Cookbook json file.
        Creates empty list of of products.

        Positional Arguments:
            * cmf {CrashMoveFolder} - a CrashMoveFolder object
            * layer_props {LayerProperties} - a LayerProperties object
        
        Optional Named Arguments:
            verify_on_creation {bool} - If True (default) then contents of the `cmf.map_definitions`
            json file are compared to the `layer_props`. If the `cmf.map_definitions` contains references to
            layers which are not described by the `layer_props` object then a ValueError will be raised.
        """
        # @TODO Add validation +
        # pass in LayerProperties object, and validate
        self.cookbook_json_file = cmf.map_definitions
        self.products = {}
        self._parse()

    def _parse(self):
        """
        Reads product "recipes" from Map Cookbook json file
        """
        with open(self.cookbook_json_file) as json_file:
            jsonContents = json.load(json_file)
            for recipe in jsonContents['recipes']:
                rec = MapRecipe(recipe)
                self.products[recipe['product']] = rec
