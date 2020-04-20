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
        self._check_cmf_param(cmf, layer_props, verify_on_creation)
        self.products = {}
        self._parse_json_file()
        self.layer_props = layer_props

        if verify_on_creation:
            cb_only, lp_only = self.get_difference_with_layer_properties()
            if len(cb_only) or len(lp_only):
                msg = self._get_verify_failure_message(lp_only, cb_only)
                raise ValueError(msg)

    def _check_cmf_param(self, cmf, layer_props, verify_on_creation):
        if cmf.verify_paths():
            self.cookbook_json_file = cmf.map_definitions
        else:
            raise ValueError('The `cmf` parameter for MapCookbook.__init__() can only accept'
                             ' values where the paths verify. eg `cmf.verify_paths() == True`.'
                             ' The value passed in this case failed this test')

        if verify_on_creation and not (layer_props.cmf.layer_properties == cmf.layer_properties):
            raise ValueError('Attempting to create a MapCookBook using a a CMF object and LayerProperties'
                             ' object which point to different layer_properties.json files. This is probably'
                             ' not what you want and may produce strange results. If you are sure this is want'
                             ' you require, then use `verify_on_creation=False` in the MapCookBook constructor.\n'
                             ' Values passed to the MapCookBook constructor\n'
                             '   cmf.layer_properties={}\n'
                             '   layer_props={}\n'.format(
                                 cmf.layer_properties,
                                 layer_props.cmf.layer_properties
                             ))

    def _parse_json_file(self):
        """
        Reads product "recipes" from Map Cookbook json file
        """
        with open(self.cookbook_json_file) as json_file:
            jsonContents = json.load(json_file)
            for recipe in jsonContents['recipes']:
                rec = MapRecipe(recipe)
                self.products[recipe['product']] = rec

    def get_difference_with_layer_properties(self):
        cb_unique_lyrs = set()

        for recipe in self.products.values():
            for l in recipe.layers:
                cb_unique_lyrs.add(l['name'])

        lp_unique_lyrs = set(self.layer_props.properties)

        cb_only = cb_unique_lyrs.difference(lp_unique_lyrs)
        lp_only = lp_unique_lyrs.difference(cb_unique_lyrs)

        return cb_only, lp_only

    def _get_verify_failure_message(self, lp_only, cb_only):
        msg = ('There is a mismatch between the layer_properties.json file:\n\t"{}"\n'
               'and the MapCookbook.json file:\n\t"{}"\n'
               'One or more layer names occur in only one of these files.\n'.format(
                   self.layer_props.cmf.layer_properties,
                   self.cookbook_json_file
               ))
        if len(cb_only):
            msg = msg + 'These layers are only mentioned in the MapCookbook json file and not in Layer'
            msg = msg + ' Properties json file:\n\t'
            msg = msg + '\n\t'.join(cb_only)
        if len(lp_only):
            msg = msg + '\nThese layers are only mentioned in the Layer Properties json file and not in the'
            msg = msg + ' MapCookbook json file: \n\t'
            msg = msg + '\n\t'.join(lp_only)

        return msg
