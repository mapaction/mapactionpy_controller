from jsonschema import validate
import glob
import json

# https://trello.com/c/tY2l5pu7/165-creating-schema-file-for-humanitarian-event-json-files
#
# Creating schema file for Humanitarian Event json files

# 1) Create a cmf_description.schema file
# 2) Publish the schema file
# 3) Enforce/validate Event object against the schema with it's constructor

# https://python-jsonschema.readthedocs.io/en/stable/

schema_path = "C:/Users/steve/Source/Repos/mapactionpy_controller/mapactionpy_controller/schemas"

cmf_config_file = "C:/Users/steve/Source/Repos/mapactionpy_controller/mapactionpy_controller/example/cmf_description.json"

schema_files = []
for file in glob.glob(schema_path+"/cmf-v*2.schema"):
    schema_files.append(file)
    print(file)

cmf_config_contents = None
with open(cmf_config_file, 'r') as f:
    cmf_config_contents = f.read()

for schema_file in schema_files:
    with open(schema_file, 'r') as f:
        schema = f.read()
        schema_obj = json.loads(schema)
        cmf_config_obj = json.loads(cmf_config_contents)
        validate(instance=cmf_config_obj, schema=schema_obj)
