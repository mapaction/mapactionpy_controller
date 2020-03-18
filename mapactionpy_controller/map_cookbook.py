from map_recipe import MapRecipe
import json


class MapCookbook:
    """
    MapCookbook - Contains recipes for Map Products
    """

    def __init__(self, cookbookJsonFile):
        """
        Sets path for Map Cookbook json file.
        Creates empty list of of products.

        Arguments:
           cookbookJsonFile {str} -- path to Map Cookbook json file "mapCookbook.json"
        """
        # @TODO Add validation +
        # pass in LayerProperties object, and validate
        self.cookbookJsonFile = cookbookJsonFile
        self.products = {}
        self._parse()

    def _parse(self):
        """
        Reads product "recipes" from Map Cookbook json file
        """
        with open(self.cookbookJsonFile) as json_file:
            jsonContents = json.load(json_file)
            for recipe in jsonContents['recipes']:
                rec = MapRecipe(recipe)
                self.products[recipe['product']] = rec
