import json
from jsonschema import validate
from os import path


def _get_schema():
    root_dir = path.abspath(path.dirname(__file__))
    schema_file = path.join(root_dir, 'schemas', 'map-recipe-v0.1.schema')
    with open(schema_file) as sf:
        return json.load(sf)


def validate_json(recipe_def):
    SCHEMA = _get_schema()
    validate(recipe_def, SCHEMA)


class MapRecipe:
    """
    MapRecipe - Ordered list of layers for each Map Product
    """

    def __init__(self, recipe_def):
        validate_json(recipe_def)

        self.mapnumber = recipe_def["mapnumber"]
        self.category = recipe_def["category"]
        self.export = recipe_def["export"]
        self.product = recipe_def["product"]
        self.layers = recipe_def["layers"]
        self.summary = recipe_def["summary"]
        self.hasQueryColumnName = self.containsQueryColumn()

    def containsQueryColumn(self):
        hasQueryColumnName = False
        for layer in self.layers:
            # TODO asmith 2020/03/06
            # Is this a terser way of achieving the same thing?
            # ```
            #    if 'columnName' in layer:
            # ```
            if (layer.get('columnName', None) is not None):
                hasQueryColumnName = True
                break
        return hasQueryColumnName
