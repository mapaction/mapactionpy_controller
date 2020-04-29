import yaml
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
import json
from jsonschema import validate
from os import path


def get_validator_for_data_schema(schema_file, cmf):

    schema_path = path.join(cmf.data_schemas, schema_file)

    with open(schema_path) as sf:
        schema = json.load(sf)

    def validate_against_schema(data):
        validate(data, schema)

    return validate_against_schema


def parse_yaml(filename):
    with open(filename, 'r') as stream:
        config = yaml.safe_load(stream)
    return config
