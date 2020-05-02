import argparse
import json
import jsonpickle
import os
import re
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.event import Event
from mapactionpy_controller.map_recipe import MapRecipe
from mapactionpy_controller.layer_properties import LayerProperties


class DataSearch():
    def __init__(self, event):
        self.event = event
        self.cmf = CrashMoveFolder(self.event.cmf_descriptor_path)

    def update_search_with_event_details(self, recipe):
        def update_regex(lyr):
            try:
                lyr.reg_exp = lyr.reg_exp.format(e=self.event)
            except IndexError:
                pass

            return lyr

        for mf in recipe.map_frames:
            mf.layers = [update_regex(lyr) for lyr in mf.layers]

        return recipe

    def update_recipe_with_datasources(self, recipe):
        for mf in recipe.map_frames:
            for lyr in mf.layers:
                lyr.data_source_path, lyr.data_name = self._find_data(lyr)

        return recipe

    def _find_data(self, lyr):
        found_datasources = []
        found_datanames = []
        for root, dirs, files in os.walk(self.cmf.active_data):  # pylint: disable=unused-variable
            for f in files:
                if re.match(lyr.reg_exp, f):
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

    ev = Event(args.event_path)
    cmf = CrashMoveFolder(ev.cmf_descriptor_path, verify_on_creation=False)
    lyr_props = LayerProperties(cmf, '.lyr', verify_on_creation=False)

    with open(args.recipe_file) as rf:
        recipe_def = json.load(rf)['recipes'].pop()

    org_recipe = MapRecipe(recipe_def, lyr_props)

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
