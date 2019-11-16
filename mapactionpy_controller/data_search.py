import argparse
import jsonpickle
import os
import re
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.event import Event
from mapactionpy_controller.product_bundle_definition import MapRecipe


class DataSearch():
    def __init__(self, event):
        self.event = event
        self.cmf = CrashMoveFolder(self.event.cmf_descriptor_path)

    def update_search_with_event_details(self, recipe):
        for lyr in recipe.layers:
            output_str = lyr.search_definition.format(e=self.event)
            lyr.search_definition = output_str

        return recipe

    def update_recipe_with_datasources(self, recipe):
        for lyr in recipe.layers:
            lyr.data_source_path, lyr.data_name = self._find_data(lyr)

        return recipe

    def _find_data(self, lyr):
        found_datasources = []
        found_datanames = []
        for root, dirs, files in os.walk(self.cmf.active_data):  # pylint: disable=unused-variable
            for f in files:
                if re.match(lyr.search_definition, f):
                    found_datasources.append(
                        os.path.normpath(os.path.join(root, f)))
                    found_datanames.append(
                        os.path.splitext(os.path.basename(f))[0])

        return ';'.join(found_datasources), ';'.join(found_datanames),


def _is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--recipe-file", dest="recipe_file", required=True,
                        help="path to recipe json file.", metavar="FILE", type=lambda x: _is_valid_file(parser, x))
    parser.add_argument("-e", "--event", dest="event_path", required=True,
                        help="path the Event descriptor file.", metavar="FILE",
                        type=lambda x: _is_valid_file(parser, x))
    parser.add_argument("-o", "--output-file", dest="output_file", required=False,
                        help="(optional) path to the ouptut file. If omited the output is printed to stdout.",
                        metavar="FILE")

    return parser.parse_args()


def main():
    args = get_args()

    org_recipe = MapRecipe(args.recipe_file)

    ds = DataSearch(Event(args.event_path))
    updated_recipe = ds.update_search_with_event_details(org_recipe)
    updated_recipe = ds.update_recipe_with_datasources(updated_recipe)

    json_recipe = jsonpickle.encode(updated_recipe, unpicklable=False)

    if args.output_file is not None:
        with open(args.output_file, 'w') as f:
            f.write(json_recipe)
    else:
        print(json_recipe)


if __name__ == '__main__':
    main()
