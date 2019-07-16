import argparse
import jsonpickle
import os
import re
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.event import Event
from mapactionpy_controller.product_bundle_definition import MapRecipe

class DataSearch():
    def __init__(self, cmf):
        self.cmf = cmf
        self.event = Event(self.cmf)

    def update_search_with_event_details(self, recipe):
        for lyr in recipe.layers:
            output_str = lyr.search_definition.format(e=self.event)
            lyr.search_definition = output_str

        return recipe

    def update_recipe_with_datasources(self, recipe):
        for lyr in recipe.layers:
            lyr.data_source_path = self._find_datasource(lyr)

        return recipe

    def _find_datasource(self, lyr):
        found = []
        for root, dirs, files in os.walk(self.cmf.active_data):
            for f in files:
                if re.match(lyr.search_definition, f):
                    found.append(os.path.normpath(os.path.join(root, f)))

        return ';'.join(found)


def _is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
        return False
    else:
        return arg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--recipe-file", dest="recipe_file", required=True,
                        help="path to recipe json file.", metavar="FILE", type=lambda x: _is_valid_file(parser, x))
    parser.add_argument("-c", "--cmf", dest="crash_move_folder", required=True,
                        help="path the Crash Move Folder descriptor file.", metavar="FILE", type=lambda x: _is_valid_file(parser, x))
    parser.add_argument("-o", "--output-file", dest="output_file", required=False,
                        help="(optional) path to the ouptut file. If omited the output is printed to stdout.", metavar="FILE")

    args = parser.parse_args()
    org_recipe = MapRecipe(args.recipe_file)

    ds = DataSearch(CrashMoveFolder(args.crash_move_folder))
    updated_recipe = ds.update_search_with_event_details(org_recipe)
    updated_recipe = ds.update_recipe_with_datasources(updated_recipe)

    json_recipe = jsonpickle.encode(updated_recipe, unpicklable=False)

    if not args.output_file is None:
        with open(args.output_file, 'w') as f:
            f.write(json_recipe)
    else:
        print (json_recipe)


if __name__ == '__main__':
    main()