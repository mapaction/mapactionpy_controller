from mapactionpy_controller.label_class import LabelClass
import json
from jsonschema import validate
from os import path


def _get_schema():
    root_dir = path.abspath(path.dirname(__file__))
    schema_file = path.join(root_dir, 'schemas', 'layer_properties-v0.1.schema')
    with open(schema_file) as sf:
        return json.load(sf)


SCHEMA = _get_schema()


def validate_json(recipe_def):
    validate(recipe_def, SCHEMA)


class MapLayer:
    def __init__(self, layer_def):
        """Constructor.  Creates an instance of layer properties

        Arguments:
            row {dict} -- From the layerProperties.json file
        """
        validate_json(layer_def)

        self.mapFrame = layer_def["MapFrame"]
        self.layerName = layer_def["LayerName"]
        self.regExp = layer_def["RegExp"]
        self.definitionQuery = layer_def["DefinitionQuery"]
        self.display = layer_def["Display"]
        self.addToLegend = layer_def["AddToLegend"]
        self.labelClasses = list()
        for labelClass in layer_def["LabelClasses"]:
            self.labelClasses.append(LabelClass(labelClass))
