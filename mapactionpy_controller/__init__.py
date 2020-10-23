import json
import logging
from os import path

from jsonschema import validate

CONFIG_SCHEMAS_DIR = path.join(path.abspath(path.dirname(__file__)), 'schemas')
TASK_TEMPLATES_DIR = path.join(path.abspath(path.dirname(__file__)), 'task-templates')


def _get_validator_for_config_schema(schema_file):

    schema_path = path.join(CONFIG_SCHEMAS_DIR, schema_file)
    with open(schema_path) as sf:
        schema = json.load(sf)

    def validate_against_schema(data):
        validate(data, schema)

    return validate_against_schema


# logging.basicConfig(
#     level=logging.DEBUG,
#     format=(
#         '%(asctime)s %(module)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s'
#         ' [%(process)d] %(message)s',
#     )
# )

logger = logging.getLogger(__name__)
# logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s (%(module)s +ln%(lineno)s) ;- %(message)s')
# formatter = logging.Formatter('%(asctime)s %(module)s %(name)s.%(funcName)s
# +%(lineno)s: %(levelname)-8s [%(process)d] %(message)s')

ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)
