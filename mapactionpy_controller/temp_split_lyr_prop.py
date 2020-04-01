from layer_properties import LayerProperties
from map_layer import MapLayer
import config_verify
import crash_move_folder
import map_cookbook
import os
import json
import jsonpickle

CMF_PATH = r"D:\code\github\default-crash-move-folder\20YYiso3nn\cmf_description.json"
cmf = crash_move_folder.CrashMoveFolder(CMF_PATH)

output_lyr_props_to_keep = os.path.join(os.path.dirname(cmf.layer_properties), 'layer_props_keep.json')
print('output_lyr_props_to_keep=' + output_lyr_props_to_keep)

output_lyr_props_to_stash = os.path.join(os.path.dirname(cmf.layer_properties), 'layer_props_stash.json')
print('output_lyr_props_to_stash=' + output_lyr_props_to_stash)

lyr_prop = LayerProperties(cmf, '.lyr', verify_on_creation=True)

lp_only, files_only = lyr_prop.get_difference_with_layer_rendering_dir()
print('lp_only=', lp_only)
print('files_only=', files_only)

cb = map_cookbook.MapCookbook(cmf.map_definitions)
cb_unique_lyrs, lp_unique_lyrs = config_verify.get_unique_lyr_names(cb, lyr_prop)

cb_only = cb_unique_lyrs.difference(lp_unique_lyrs)
lp_only = lp_unique_lyrs.difference(cb_unique_lyrs)

keep = set()
stash = set()

with open(cmf.layer_properties) as json_file:
    jsonContents = json.load(json_file)
    for layer in jsonContents['layerProperties']:
        mapLayer = MapLayer(layer)
        if mapLayer.layerName in cb_unique_lyrs:
            keep.add(mapLayer)
        else:
            stash.add(mapLayer)

json_keep = jsonpickle.encode(keep, unpicklable=False)
json_stash = jsonpickle.encode(stash, unpicklable=False)

with open(output_lyr_props_to_keep, 'w') as keep_file:
    keep_file.write(json_keep)

with open(output_lyr_props_to_stash, 'w') as stash_file:
    stash_file.write(json_stash)

