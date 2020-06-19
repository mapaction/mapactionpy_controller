import json
from mapactionpy_controller.label_class import LabelClass
from mapactionpy_controller.recipe_atlas import RecipeAtlas
from mapactionpy_controller import _get_validator_for_config_schema
import mapactionpy_controller.data_schemas as data_schemas
from os import path
import jsonschema

validate_against_layer_schema = _get_validator_for_config_schema('layer_properties-v0.2.schema')
validate_against_recipe_schema = _get_validator_for_config_schema('map-recipe-v0.2.schema')


def get_state_optional_fields(obj, optional_fields):
    # See https://docs.python.org/3/library/pickle.html#pickle-state
    # Copy the object's state from self.__dict__ which contains
    # all our instance attributes. Always use the dict.copy()
    # method to avoid modifying the original state.
    state = obj.__dict__.copy()
    # Remove any optional members which have a value of None.
    for option in optional_fields:
        if not state[option]:
            del state[option]
    return state


def set_state_optional_fields(obj, state, optional_fields):
    # Restore optional elements to None.
    for option in optional_fields:
        if option not in state:
            state[option] = None

    obj.__dict__.update(state)


class RecipeLayer:

    OPTIONAL_FIELDS = ('data_source_path', 'data_name', 'data_schema')

    def __init__(self, layer_def, lyr_props, verify_on_creation=True):
        """Constructor.  Creates an instance of layer properties

        Arguments:
            row {dict} -- From the layerProperties.json file
        """
        validate_against_layer_schema(layer_def)

        # Required fields
        self.name = layer_def["name"]
        self.reg_exp = layer_def["reg_exp"]
        self.definition_query = layer_def["definition_query"]
        self.schema_definition = layer_def["schema_definition"]

        self.display = layer_def["display"]
        self.add_to_legend = layer_def["add_to_legend"]
        self.label_classes = list()
        for lbl_class_def in layer_def["label_classes"]:
            self.label_classes.append(LabelClass(lbl_class_def))

        # Optional fields
        self._get_layer_file_path(layer_def, lyr_props, verify_on_creation)
        self._get_data_schema(layer_def, lyr_props)

    def _get_layer_file_path(self, layer_def, lyr_props, verify_on_creation):
        if 'layer_file_path' in layer_def:
            self.layer_file_path = layer_def['layer_file_path']
            if verify_on_creation:
                self.verify_layer_file_path()
        else:
            self.layer_file_path = path.join(
                lyr_props.cmf.layer_rendering,
                (self.name + lyr_props.extension)
            )

        self.data_source_path = layer_def.get('data_source_path', None)
        self.data_name = layer_def.get('data_name', None)

    def _get_data_schema(self, layer_def, lyr_props):
        if 'data_schema' in layer_def:
            self.data_schema = layer_def['data_schema']
        else:
            schema_file = path.abspath(path.join(lyr_props.cmf.data_schemas, self.schema_definition))
            self.data_schema = data_schemas.parse_yaml(schema_file)

        # check that the schema itself is valid.
        jsonschema.Draft7Validator.check_schema(self.data_schema)

    def verify_layer_file_path(self):
        if not path.exists(self.layer_file_path):
            raise ValueError("The expected layer file {} could not be found."
                             "".format(self.layer_file_path))

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except AttributeError:
            return False

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __getstate__(self):
        return get_state_optional_fields(self, RecipeLayer.OPTIONAL_FIELDS)

    def __setstate__(self, state):
        set_state_optional_fields(self, state, RecipeLayer.OPTIONAL_FIELDS)


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
        return get_state_optional_fields(self, RecipeFrame.OPTIONAL_FIELDS)

    def __setstate__(self, state):
        set_state_optional_fields(self, state, RecipeFrame.OPTIONAL_FIELDS)


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

        validate_against_recipe_schema(recipe_def)

        # Required fields
        self.mapnumber = recipe_def["mapnumber"]
        self.category = recipe_def["category"]
        self.export = recipe_def["export"]
        self.product = recipe_def["product"]
        # This is a list, but see note in `_parse_map_frames` method
        self.map_frames = self._parse_map_frames(recipe_def["map_frames"], lyr_props)
        self.summary = recipe_def["summary"]
        self.template = recipe_def["template"]

        # Optional fields
        self.map_project_path = recipe_def.get('map_project_path', None)
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
        Returns the RecipeAtlas object
        Raises ValueError if the requested_atlas_name does not exist
        """
        # We trust that the map frame names are unique
        try:
            return [mf for mf in self.map_frames if mf.name == requested_frame_name][0]
        except IndexError:
            raise ValueError(
                'The requested map frame {} does not exist in the recipe {}'.format(
                    requested_frame_name, self.product))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __getstate__(self):
        return get_state_optional_fields(self, MapRecipe.OPTIONAL_FIELDS)

    def __setstate__(self, state):
        set_state_optional_fields(self, state, MapRecipe.OPTIONAL_FIELDS)
