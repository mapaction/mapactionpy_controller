import logging
from os import path

import jsonschema

import mapactionpy_controller.data_schemas as data_schemas
import mapactionpy_controller.state_serialization as state_serialization
from mapactionpy_controller import _get_validator_for_config_schema


logger = logging.getLogger(__name__)
validate_against_layer_schema = _get_validator_for_config_schema('layer_properties-v0.2.schema')


class LabelClass:
    """
    Enables selection of properties to support labels in a Layer
    """

    def __init__(self, row):
        self.class_name = row["class_name"]
        self.expression = row["expression"]
        self.sql_query = row["sql_query"]
        self.show_class_labels = row["show_class_labels"]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)


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
            self.layer_file_path = path.abspath(layer_def['layer_file_path'])
            if verify_on_creation:
                self.verify_layer_file_path()
        else:
            self.layer_file_path = path.abspath(path.join(
                lyr_props.cmf.layer_rendering,
                (self.name + lyr_props.extension)
            ))

        self.data_source_path = layer_def.get('data_source_path', None)
        if self.data_source_path:
            self.data_source_path = path.abspath(self.data_source_path)

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
        return state_serialization.get_state_optional_fields(self, RecipeLayer.OPTIONAL_FIELDS)

    def __setstate__(self, state):
        state_serialization.set_state_optional_fields(self, state, RecipeLayer.OPTIONAL_FIELDS)
