# TODO: asmith 2020/03/04
# This whole file should be moved to the mapactionpy_controller module.
from MapCookbook import MapCookbook
from LayerProperties import LayerProperties
import os
import argparse
# import collections


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
        return False
    else:
        return arg


def is_valid_directory(parser, arg):
    if os.path.isdir(arg):
        return arg
    else:
        parser.error("The directory %s does not exist!" % arg)
        return False


# def check_undefined_lyrs_in_cookbook(cb, lyrs):
# def check_unused_lyrs_in_lyr_properties(cb, lyrs):
# def check_lyrs_in_config_missing_lyrfile(lyr_props, lyr_dir):
# def check_lyrfiles_in_dir_not_in_lyr_props(lyr_props, lyr_dir):


def get_unique_lyr_names(cookbook, lyr_props, lyr_dir):
    cb_unique_lyrs = set()
    lp_unique_lyrs = set()
    files_unique = set()

    for recipe in cookbook.get_products():
        for l in recipe.layers:
            cb_unique_lyrs.add(l.name)

    for l in lyr_props.properties:
        lp_unique_lyrs.add(l.layerName)

    for root, dirs, files in os.walk(lyr_dir):
        for f in files:
            if '.lyr' in f:
                files_unique.add(os.path.splitext(f)[0])

    return (cb_unique_lyrs, lp_unique_lyrs, files_unique)


def main(args):
    cb = MapCookbook(args.cookbookFile)
    cb.parse()
    lyrs = LayerProperties(args.layerConfig)
    lyrs.parse()

    cb_unique_lyrs, lp_unique_lyrs, files_unique = get_unique_lyr_names(
        cb, lyrs, args.layerDirectory)
    all = cb_unique_lyrs.union(lp_unique_lyrs).union(files_unique)

    print('in_cookbook?,\t in_layerpros?,\t in_lyr_dir?,\t layername')

    for l in all:
        in_cookbook = l in cb_unique_lyrs
        in_lyr_props = l in lp_unique_lyrs
        in_lyr_dir = l in files_unique

        if in_cookbook:
            print("\t".join(map(str, (in_cookbook, in_lyr_props, in_lyr_dir, l))))


# TODO: asmith 2020/03/04
# This commandline interface and arg parser should be merged with other commandline interfaces
# such as the one in mapactionpy_controller.check_naming_convention.py
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This tool checks the internal self-consistency of the cookbook file, layerProperties file and the'  # noqa
                    ' layerfiles within the layerDirectory'
    )
    parser.add_argument("-b", "--cookbook", dest="cookbookFile", required=True,
                        help="path to cookbook json file", metavar="FILE", type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-l", "--layerConfig", dest="layerConfig", required=True,
                        help="path to layer config json file", metavar="FILE", type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-ld", "--layerDirectory", dest="layerDirectory", required=True,
                        help="path to layer directory", metavar="FILE", type=lambda x: is_valid_directory(parser, x))

    args = parser.parse_args()
    main(args)

# this_dir = os.path.abspath(os.path.dirname(__file__))
# example_cookbook_path = os.path.join(this_dir, 'Config', 'mapCookbook.json')
# example_lyr_props__path = os.path.join(
#    this_dir, 'Config', 'layerProperties.json')
