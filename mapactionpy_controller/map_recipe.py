import json
from mapactionpy_controller.label_class import LabelClass
from mapactionpy_controller import _get_validator_for_config_schema
import mapactionpy_controller.data_schemas as data_schemas
from os import path

validate_against_atlas_schema = _get_validator_for_config_schema('atlas-v0.2.schema')
validate_against_layer_schema = _get_validator_for_config_schema('layer_properties-v0.2.schema')
validate_against_recipe_schema = _get_validator_for_config_schema('map-recipe-v0.2.schema')


def get_state_optional_fields(obj, optional_fields):
    # See https://docs.python.org/3/library/pickle.html#pickle-state
    # Copy the object's state from self.__dict__ which contains
    # all our instance attributes. Always use the dict.copy()
    # method to avoid modifying the original state.
    state = obj.__dict__.copy()
    # Remove the unpicklable entries.
    for option in optional_fields:
        if not state[option]:
            del state[option]
    return state


def set_state_optional_fields(obj, state, optional_fields):
    # Restore instance attributes (i.e., filename and lineno).
    for option in optional_fields:
        if option not in state:
            state[option] = None

    obj.__dict__.update(state)


class RecipeLayer:

    OPTIONAL_FIELDS = ('data_source_path', 'data_name')

    def __init__(self, layer_def):
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
        self.data_source_path = layer_def.get('data_source_path', None)
        self.data_name = layer_def.get('data_name', None)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

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
        self.layers = self._parse_layers(frame_def["layers"], lyr_props)

        # Optional fields
        self.scale_text_element = frame_def.get('scale_text_element', None)
        self.spatial_ref_text_element = frame_def.get('spatial_ref_text_element', None)

    def _parse_layers(self, lyr_defs, lyr_props):
        lyrs = []
        for lyr_def in lyr_defs:
            # if lyr_def only includes the name of the layer and no other properties
            # then import them from a LayerProperties object
            # Else, load them from the lyr_def
            l_name = lyr_def['name']
            if len(lyr_def) == 1:
                lyrs.append(lyr_props.properties.get(l_name, l_name))
            else:
                lyrs.append(RecipeLayer(lyr_def))

        return lyrs

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __getstate__(self):
        return get_state_optional_fields(self, RecipeFrame.OPTIONAL_FIELDS)

    def __setstate__(self, state):
        set_state_optional_fields(self, state, RecipeFrame.OPTIONAL_FIELDS)


class RecipeAtlas:
    def __init__(self, atlas_def, recipe, lyr_props):
        validate_against_atlas_schema(atlas_def)

        # Required fields
        self.map_frame = atlas_def["map_frame"]
        self.layer_name = atlas_def["layer_name"]
        self.column_name = atlas_def["column_name"]

        # Compare the atlas definition with the other parts of the recipe definition
        m_frame_lst = [mf for mf in recipe.map_frames if mf.name == self.map_frame]
        if len(m_frame_lst) == 1:
            m_frame = m_frame_lst[0]
        else:
            raise ValueError(
                'The Map Recipe definition is invalid. The "atlas" section refers to a map_frame '
                ' ({}) that does not exist in the "map_frames" section of the recipe.'.format(
                    self.map_frame)
            )

        lyr_lst = [l for l in m_frame.layers if l.name == self.layer_name]
        if len(lyr_lst) == 1:
            lyr = lyr_lst[0]
        else:
            raise ValueError(
                'The Map Recipe definition is invalid. The "atlas" section refers to a layer_name '
                ' ({}) that does not exist in the relevant "map_frame" ({}) section of the recipe.'
                ''.format(self.layer_name, self.map_frame)
            )

        schema_file = path.join(lyr_props.cmf.data_schemas, lyr.schema_definition)
        schema = data_schemas.parse_yaml(schema_file)
        if self.column_name not in schema['required']:
            raise ValueError(
                'The Map Recipe definition is invalid. The "atlas" section refers to a column_name '
                ' ({}) that does not exist in the schema of the relevant layer ({}).'
                ''.format(self.column_name, lyr.name)
            )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)


class MapRecipe:
    """
    MapRecipe
    """
    OPTIONAL_FIELDS = ('runners', 'atlas')

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
        self.map_frames = self._parse_map_frames(recipe_def["map_frames"], lyr_props)
        self.summary = recipe_def["summary"]
        self.template = recipe_def["template"]

        # Optional fields
        self.runners = recipe_def.get('runners', None)
        atlas_def = recipe_def.get('atlas', None)
        if atlas_def:
            self.atlas = RecipeAtlas(atlas_def, self, lyr_props)
        else:
            self.atlas = None

        # Self consistancy checks
        self._check_for_dup_text_elements()

    def get_lyrs_as_set(self):
        def get_lyr_name(lyr):
            try:
                return lyr.name
            except AttributeError:
                return lyr

        unique_lyrs = set()
        for mf in self.map_frames:

            lyrs = [get_lyr_name(l) for l in mf.layers]
            unique_lyrs.update(lyrs)

        return unique_lyrs

    def _parse_map_frames(self, map_frames_def, lyr_props):
        map_frames = []
        for frame_def in map_frames_def:
            mf = RecipeFrame(frame_def, lyr_props)
            map_frames.append(mf)

        return map_frames

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

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)

    def __getstate__(self):
        return get_state_optional_fields(self, MapRecipe.OPTIONAL_FIELDS)

    def __setstate__(self, state):
        set_state_optional_fields(self, state, MapRecipe.OPTIONAL_FIELDS)
