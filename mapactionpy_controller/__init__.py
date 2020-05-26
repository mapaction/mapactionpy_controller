import json
from jsonschema import validate
from os import path

CONFIG_SCHEMAS_DIR = path.join(path.abspath(path.dirname(__file__)), 'schemas')


def _get_validator_for_config_schema(schema_file):

    schema_path = path.join(CONFIG_SCHEMAS_DIR, schema_file)
    with open(schema_path) as sf:
        schema = json.load(sf)

    def validate_against_schema(data):
        validate(data, schema)

    return validate_against_schema
