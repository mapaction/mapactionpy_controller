from mapactionpy_controller.label_class import LabelClass
from mapactionpy_controller import _get_validator_for_config_schema
import mapactionpy_controller.data_schemas as data_schemas
from os import path

validate_against_atlas_schema = _get_validator_for_config_schema('atlas-v0.2.schema')
validate_against_layer_schema = _get_validator_for_config_schema('layer_properties-v0.2.schema')
validate_against_recipe_schema = _get_validator_for_config_schema('map-recipe-v0.2.schema')


class RecipeLayer:
    def __init__(self, layer_def):
        """Constructor.  Creates an instance of layer properties

        Arguments:
            row {dict} -- From the layerProperties.json file
        """
        validate_against_layer_schema(layer_def)

        self.layerName = layer_def["LayerName"]
        self.regExp = layer_def["RegExp"]
        self.definitionQuery = layer_def["DefinitionQuery"]
        self.schema_definition = layer_def["schema_definition"]
        self.display = layer_def["Display"]
        self.addToLegend = layer_def["AddToLegend"]
        self.labelClasses = list()
        for labelClass in layer_def["LabelClasses"]:
            self.labelClasses.append(LabelClass(labelClass))


class RecipeFrame:
    def __init__(self, frame_def, lyr_props):
        # Required fields
        self.name = frame_def["name"]
        self.layers = self._parse_layers(frame_def["layers"], lyr_props)

        # Optional fields
        self.scale_text_element = frame_def.get('scale_text_element', None)
        self.spatial_ref_text_element = frame_def.get('spatial_ref_text_element', None)

    def _parse_layers(self, lyrs_def, lyr_props):
        lyrs = {}
        for lyr_def in lyrs_def:
            # if lyr_def only includes the name of the layer and no other properties
            # then import them from a LayerProperties object
            # Else, load them from the lyr_def
            l_name = lyr_def['name']
            if len(lyr_def) == 1:
                lyrs[l_name] = lyr_props.properties.get(l_name, l_name)
            else:
                lyrs[l_name] = RecipeLayer(lyrs_def)

        return lyrs


class RecipeAtlas:
    def __init__(self, atlas_def, recipe, lyr_props):
        validate_against_atlas_schema(atlas_def)

        # Required fields
        self.map_frame = atlas_def["map_frame"]
        self.layer_name = atlas_def["layer_name"]
        self.column_name = atlas_def["column_name"]

        # Compare the atlas definition with the other parts of the recipe definition
        try:
            m_frame = recipe.map_frames[self.map_frame]
        except KeyError as ke:
            raise ValueError(
                'The Map Recipe definition is invalid. The "atlas" section refers to a map_frame '
                ' ({}) that does not exist in the "map_frames" section of the recipe.'.format(ke)
            )

        try:
            lyr = m_frame.layers[self.layer_name]
        except KeyError as ke:
            raise ValueError(
                'The Map Recipe definition is invalid. The "atlas" section refers to a layer_name '
                ' ({}) that does not exist in the relevant "map_frame" ({}) section of the recipe.'
                ''.format(ke, self.map_frame)
            )

        schema_file = path.join(lyr_props.cmf.data_schemas, lyr.schema_definition)
        schema = data_schemas.parse_yaml(schema_file)
        if self.column_name not in schema['required']:
            raise ValueError(
                'The Map Recipe definition is invalid. The "atlas" section refers to a column_name '
                ' ({}) that does not exist in the schema of the relevant layer ({}).'
                ''.format(self.column_name, lyr.layerName)
            )


class MapRecipe:
    """
    MapRecipe - Ordered list of layers for each Map Product
    """

    def __init__(self, recipe_def, lyr_props):
        validate_against_recipe_schema(recipe_def)

        # Required fields
        self.mapnumber = recipe_def["mapnumber"]
        self.category = recipe_def["category"]
        self.export = recipe_def["export"]
        self.product = recipe_def["product"]
        self.map_frames = self._parse_map_frames(recipe_def["map_frames"], lyr_props)
        self.summary = recipe_def["summary"]

        # Optional fields
        self.runners = recipe_def.get('runners', None)
        atlas_def = recipe_def.get('atlas', None)
        if atlas_def:
            self.atlas = RecipeAtlas(atlas_def, self, lyr_props)
        else:
            self.atlas = None

        self._check_for_dup_text_elements()

    def get_lyrs_as_set(self):
        def get_lyr_name(lyr):
            try:
                return lyr['name']
            except TypeError:
                return lyr

        unique_lyrs = set()
        for mf in self.map_frames.values():

            lyrs = [get_lyr_name(l) for l in mf.layers]
            unique_lyrs.update(lyrs)

        return unique_lyrs

    def _parse_map_frames(self, map_frames_def, lyr_props):
        map_frames = {}
        for frame_def in map_frames_def:
            mf = RecipeFrame(frame_def, lyr_props)
            map_frames[mf.name] = mf

        return map_frames

    def _check_for_dup_text_elements(self):
        # check that any named `scale_text_element`s and `spatial_ref_text_element`s
        # are each only referred to by a single map_frame
        scale_text_elements_set = set()
        spatial_ref_text_elements_set = set()

        for mf in self.map_frames.values():
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
