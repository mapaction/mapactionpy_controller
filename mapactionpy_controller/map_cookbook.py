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
        self.layer_props = layer_props
        self._parse_json_file()

        if verify_on_creation:
            msg = self.layer_props.get_difference_with_other_layer_set(
                self.get_all_included_lyrs_as_set(),
                self._get_mismatch_wtih_lyr_props_message
            )
            if msg:
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
                rec = MapRecipe(recipe, self.layer_props)
                self.products[recipe['product']] = rec

    def get_all_included_lyrs_as_set(self):
        cb_unique_lyrs = set()

        for recipe in self.products.values():
            cb_unique_lyrs.update(recipe.get_lyrs_as_set())

        return cb_unique_lyrs

    def _get_mismatch_wtih_lyr_props_message(self, lp_only, cb_only):
        msg = ('There is a mismatch between the layer_properties.json file:\n\t"{}"\n'
               'and the MapCookbook.json file:\n\t"{}"\n'
               'One or more layer names occur in only one of these files.\n'.format(
                   self.layer_props.cmf.layer_properties,
                   self.cookbook_json_file
               ))

        pair = ((cb_only, 'These layers are only mentioned in the MapCookbook json file and not in Layer'
                          ' Properties json file:'),
                (lp_only, 'These layers are only mentioned in the Layer Properties json file and not in the'
                          ' MapCookbook json file:'))

        return self.layer_props._msg_builder(pair, msg)
