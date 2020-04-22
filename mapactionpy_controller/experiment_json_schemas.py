from jsonschema import validate
import json
import os
from map_recipe import MapRecipe

root_dir = os.path.abspath(os.path.dirname(__file__))
schema_file = os.path.join(root_dir, 'schemas', 'map_cook_book-v0.1.schema')

cookbookfile = os.path.join(root_dir, 'example','dummy_mapCookbook.json')
cookbookfile = r"D:\code\github\default-crash-move-folder\20YYiso3nn\GIS\3_Mapping\31_Resources\316_Automation\mapCookbook.json"
cookbookfile = r"D:\code\github\default-crash-move-folder\20YYiso3nn\GIS\3_Mapping\31_Resources\316_Automation\future_map_cook_book.json"

with open(schema_file) as sf:
    SCHEMA = json.load(sf)

with open(cookbookfile) as cbf:
    data = json.load(cbf)

    for recipe in data['recipes']:
        print(validate(recipe, SCHEMA))
        rec = MapRecipe(recipe)
        # self.products[recipe['product']] = rec

# print(validate(data, SCHEMA))
