from mapactionpy_controller.label_class import LabelClass
from mapactionpy_controller import _get_validator_for_schema

validate_against_schema = _get_validator_for_schema('layer_properties-v0.1.schema')


class MapLayer:
    def __init__(self, layer_def):
        """Constructor.  Creates an instance of layer properties

        Arguments:
            row {dict} -- From the layerProperties.json file
        """
        validate_against_schema(layer_def)

        self.mapFrame = layer_def["MapFrame"]
        self.layerName = layer_def["LayerName"]
        self.regExp = layer_def["RegExp"]
        self.definitionQuery = layer_def["DefinitionQuery"]
        self.display = layer_def["Display"]
        self.addToLegend = layer_def["AddToLegend"]
        self.labelClasses = list()
        for labelClass in layer_def["LabelClasses"]:
            self.labelClasses.append(LabelClass(labelClass))
