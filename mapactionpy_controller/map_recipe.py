import json
import logging
from os import path

import jsonpickle
import jsonschema

import mapactionpy_controller.state_serialization as state_serialization
from mapactionpy_controller import _get_validator_for_config_schema
from mapactionpy_controller.recipe_atlas import RecipeAtlas
from mapactionpy_controller.recipe_layer import RecipeLayer

logger = logging.getLogger(__name__)
validate_against_recipe_schema_v0_3 = _get_validator_for_config_schema('map-recipe-v0.3.schema')
validate_against_recipe_schema_v0_2 = _get_validator_for_config_schema('map-recipe-v0.2.schema')


class RecipeFrame:
    """
    RecipeFrame - Includes an ordered list of layers for each Map Frame
    """
    OPTIONAL_FIELDS = ('scale_text_element', 'spatial_ref_text_element')

    def __init__(self, frame_def, lyr_props):
        # Required fields
        self.name = frame_def["name"]
        # This is a list, but see note in `_parse_layers` method
        self.layers = self._parse_layers(frame_def["layers"], lyr_props)

        # Optional fields
        self.scale_text_element = frame_def.get('scale_text_element', None)
        self.spatial_ref_text_element = frame_def.get('spatial_ref_text_element', None)

    def _parse_layers(self, lyr_defs, lyr_props):
        # We create a seperate list nad set here so that we can enforce unique layernames. However only
        # the list is returned. Client code is generally more readable and elegant if `self.layers` is a
        # list. This enforces that layer names must be unique in the json representation, however
        # theoretically allows client code to create multiple layers with identical names. The behaviour
        # in this circumstance is not known or tested and is entirely the client's responsiblity.
        recipe_lyrs_list = []
        lyrs_names_set = set()
        for lyr_def in lyr_defs:
            l_name = lyr_def['name']
            if l_name in lyrs_names_set:
                raise ValueError(
                    'Duplicate layer name {} in mapframe {}. Each layername within a'
                    ' mapframe must unique'.format(l_name, self.name))

            lyrs_names_set.add(l_name)
            recipe_lyrs_list.append(self._parse_single_layer(l_name, lyr_def, lyr_props))

        return recipe_lyrs_list

    def _parse_single_layer(self, l_name, lyr_def, lyr_props):
        # if lyr_def only includes the name of the layer and no other properties
        # then import them from a LayerProperties object
        # Else, load them from the lyr_def
        if len(lyr_def) == 1:
            return lyr_props.properties.get(l_name, l_name)
        else:
            return RecipeLayer(lyr_def, lyr_props)

    def contains_layer(self, requested_layer_name):
        """
        Gets a layer by name.
        Returns a boolean
        """
        return requested_layer_name in [lyr.name for lyr in self.layers]

    def get_layer(self, requested_layer_name):
        """
        Gets a layer by name.
        Returns the RecipeLayer object
        Raises ValueError if the requested_layer_name does not exist
        """
        # We trust that the layer names are unique
        for lyr in self.layers:
            if lyr.name == requested_layer_name:
                return lyr

        raise ValueError(
            'The requested layer {} does not exist in the map frame {}'.format(
                requested_layer_name, self.name))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __getstate__(self):
        return state_serialization.get_state_optional_fields(self, RecipeFrame.OPTIONAL_FIELDS)

    def __setstate__(self, state):
        state_serialization.set_state_optional_fields(self, state, RecipeFrame.OPTIONAL_FIELDS)


class MapRecipe:
    """
    MapRecipe
    """
    OPTIONAL_FIELDS = ('runners', 'atlas', 'map_project_path', 'template_path', 'version_num')

    def __init__(self, recipe_definition, lyr_props):
        if isinstance(recipe_definition, dict):
            recipe_def = recipe_definition
        else:
            recipe_def = json.loads(recipe_definition)

        backwards_compat = self._check_schemas_with_backward_compat(recipe_def)

        # Required fields
        self.mapnumber = recipe_def["mapnumber"]
        self.category = recipe_def["category"]
        self.export = recipe_def["export"]
        self.product = recipe_def["product"]
        # This is a list, but see note in `_parse_map_frames` method
        self.map_frames = self._parse_map_frames(recipe_def["map_frames"], lyr_props)
        self.summary = recipe_def["summary"]
        self.template = recipe_def["template"]
        self.principal_map_frame = self._parse_principal_map_frame(recipe_def, backwards_compat)

        # Optional fields
        self.map_project_path = recipe_def.get('map_project_path', None)
        if self.map_project_path:
            self.map_project_path = path.abspath(self.map_project_path)
        self.template_path = recipe_def.get('template_path', None)
        self.version_num = recipe_def.get('version_num', None)
        self.runners = recipe_def.get('runners', None)
        atlas_def = recipe_def.get('atlas', None)
        if atlas_def:
            self.atlas = RecipeAtlas(atlas_def, self, lyr_props)
        else:
            self.atlas = None

        # Self consistency checks
        self._check_for_dup_text_elements()

    def _check_schemas_with_backward_compat(self, recipe_def):
        try:
            validate_against_recipe_schema_v0_3(recipe_def)
            return False
        except jsonschema.ValidationError as ve_v0_3:
            try:
                validate_against_recipe_schema_v0_2(recipe_def)
                # Do something useful here
                # Hack some values? Or raise a JIRA ticket?
                logger.warn('Attempting to load backwards compatable v0.2 MapRecipe')
                # raise ValueError('old maprecipe format')
                return True
            except jsonschema.ValidationError:
                raise ve_v0_3

    def get_lyrs_as_set(self):
        # this is required for the case that the lyr is a str of the layername
        # This can only happen if the layername was not found in the Layerproperties file
        def get_lyr_name(lyr):
            try:
                return lyr.name
            except AttributeError:
                return lyr

        unique_lyrs = set()
        for mf in self.map_frames:

            lyrs = [get_lyr_name(lyr) for lyr in mf.layers]
            unique_lyrs.update(lyrs)

        return unique_lyrs

    def _parse_map_frames(self, map_frames_def, lyr_props):
        # We create a seperate list nad set here so that we can enforce unique map_frames names. However only
        # the list is returned. Client code is generally more readable and elegant if `self.map_frames` is a
        # list. This enforces that map_frames names must be unique in the json representation, however
        # theoretically allows client code to create multiple map frames with identical names. The behaviour
        # in this circumstance is not known or tested and is entirely the client's responsiblity.
        recipe_map_frames_list = []
        map_frames_set = set()
        for frame_def in map_frames_def:
            mf = RecipeFrame(frame_def, lyr_props)
            if mf.name in map_frames_set:
                raise ValueError(
                    'Duplicate mapframe name {} in recipe {}. Each mapframe name within a'
                    ' recipe must unique'.format(mf.name, self.product))

            map_frames_set.add(mf.name)
            recipe_map_frames_list.append(mf)

        return recipe_map_frames_list

    def _parse_principal_map_frame(self, recipe_def, backwards_compat):
        """
        This assumes that `_parse_map_frames` as already been called.
        """
        p_map_frame = recipe_def.get('principal_map_frame', "Main map")

        if p_map_frame not in [mf.name for mf in self.map_frames]:
            err_msg = (
                'Unable to find a MapFrame "{}" in the recipe. The `principal_map_frame` value must have the'
                ' name of one of the MapFram objects in the recipe.')

            if backwards_compat:
                err_msg = ('Unable to find a MapFrame "Main map" in the recipe. Please update the recipe to'
                           ' v0.3 format.')

            raise ValueError(err_msg)

        return p_map_frame

    def _check_for_dup_text_elements(self):
        # check that any named `scale_text_element`s and `spatial_ref_text_element`s
        # are each only referred to by a single map_frame
        scale_text_elements_set = set()
        spatial_ref_text_elements_set = set()

        for mf in self.map_frames:
            self._find_dups(mf.scale_text_element, scale_text_elements_set,
                            'The Map Recipe definition is invalid. More than one "map_frame" is linked to the'
                            ' Scale text element "{}"'
                            )
            self._find_dups(mf.spatial_ref_text_element, spatial_ref_text_elements_set,
                            'The Map Recipe definition is invalid. More than one "map_frame" is linked to the'
                            ' Spatial reference text element "{}"'
                            )

    def _find_dups(self, elem, aggregate_set, msg):
        if elem:
            if elem in aggregate_set:
                raise ValueError(msg.format(elem))
            else:
                aggregate_set.add(elem)

    def contains_frame(self, requested_frame_name):
        """
        Check whether or not an atlas with the given name exists in the MapRecipe.
        Returns a boolean
        """
        return requested_frame_name in [mf.name for mf in self.map_frames]

    def get_frame(self, requested_frame_name):
        """
        Gets an atlas by name.
        @returns the RecipeAtlas object
        @raises ValueError if the requested_atlas_name does not exist
        """
        # We trust that the map frame names are unique
        try:
            return [mf for mf in self.map_frames if mf.name == requested_frame_name][0]
        except IndexError:
            raise ValueError(
                'The requested map frame {} does not exist in the recipe {}'.format(
                    requested_frame_name, self.product))

    def all_layers(self):
        """
        A convenience method which all layers within the MapRecipe, irrespective of the MapFrame. Saves the
        caller needing to iterate through the MapFrames.

        @returns A list of every layer reference in the Map from all MapFrames.
        """
        # Doubtless there is a neater, comprehension based way of doing this.
        result = []
        for mf in self.map_frames:
            result.extend(mf.layers)

        # print('MapRecipe.all_layers() = {}'.format(result))
        return result
        # return list(itertools.chain([mf.layers for mf in self.map_frames]))

    def __str__(self):
        return json.dumps(json.loads(jsonpickle.encode(self, unpicklable=False)), indent=4)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __getstate__(self):
        return state_serialization.get_state_optional_fields(self, MapRecipe.OPTIONAL_FIELDS)

    def __setstate__(self, state):
        state_serialization.set_state_optional_fields(self, state, MapRecipe.OPTIONAL_FIELDS)
