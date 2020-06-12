from mapactionpy_controller import _get_validator_for_config_schema

validate_against_atlas_schema = _get_validator_for_config_schema('atlas-v0.2.schema')


class RecipeAtlas:
    def __init__(self, atlas_def, recipe, lyr_props):
        validate_against_atlas_schema(atlas_def)

        # Required fields
        self.map_frame = atlas_def["map_frame"]
        self.layer_name = atlas_def["layer_name"]
        self.column_name = atlas_def["column_name"]

        # Compare the atlas definition with the other parts of the recipe definition
        if recipe.contains_frame(self.map_frame):
            m_frame = recipe.get_frame(self.map_frame)
        else:
            raise ValueError(
                'The Map Recipe definition is invalid. The "atlas" section refers to a map_frame '
                ' ({}) that does not exist in the "map_frames" section of the recipe.'.format(
                    self.map_frame)
            )

        if m_frame.contains_layer(self.layer_name):
            lyr = m_frame.get_layer(self.layer_name)
        else:
            raise ValueError(
                'The Map Recipe definition is invalid. The "atlas" section refers to a layer_name '
                ' ({}) that does not exist in the relevant "map_frame" ({}) section of the recipe.'
                ''.format(self.layer_name, self.map_frame)
            )

        if self.column_name not in lyr.data_schema['required']:
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
