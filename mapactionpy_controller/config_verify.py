from mapactionpy_controller.map_cookbook import MapCookbook
from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
import os
import argparse


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


def get_unique_lyr_names(cookbook, lyr_props):
    cb_unique_lyrs = set()
    lp_unique_lyrs = set()

    for recipe in cookbook.products.values():
        for l in recipe.layers:
            # print(l['name'], l)
            cb_unique_lyrs.add(l['name'])

    for l in lyr_props.properties:
        # print l
        lp_unique_lyrs.add(l)

    return (cb_unique_lyrs, lp_unique_lyrs)


def main(cmf_desc, layer_file_extension):
    cmf = CrashMoveFolder(cmf_desc)

    print('-------------------------------------\n')
    try:
        lyrs = LayerProperties(cmf, layer_file_extension, verify_on_creation=True)
        print('No inconsistancy detected between:\n'
              ' * the contents of the layer properties json file:\n\t{props}\n'
              ' * and layer rendering dir:\n\t{render}\n'.format(
                  props=cmf.layer_properties,
                  render=cmf.layer_rendering
              ))
    except ValueError as ve:
        print(ve.message)
        exit(1)

    print('-------------------------------------\n')
    cb = MapCookbook(cmf.map_definitions)
    cb_unique_lyrs, lp_unique_lyrs = get_unique_lyr_names(cb, lyrs)

    cb_only = cb_unique_lyrs.difference(lp_unique_lyrs)
    lp_only = lp_unique_lyrs.difference(cb_unique_lyrs)

    if len(cb_only) or len(lp_only):
        msg = ('There is a mismatch between the layer_properties.json file:\n\t"{}"\n'
               'and the MapCookbook.json file:\n\t"{}"\n'
               'One or more layer names occur in only one of these files.\n'.format(
                   cmf.layer_properties,
                   cmf.map_definitions
               ))
        if len(cb_only):
            msg = msg + 'These layers are only mentioned in the MapCookbook json file and not in Layer'
            msg = msg + ' Properties json file:\n\t'
            msg = msg + '\n\t'.join(cb_only)
        if len(lp_only):
            msg = msg + '\nThese layers are only mentioned in the Layer Properties json file and not in the'
            msg = msg + ' MapCookbook json file: \n\t'
            msg = msg + '\n\t'.join(lp_only)

        print(msg)
        print('-------------------------------------\n')
        exit(2)
    else:
        print('No inconsistancy detected between:\n'
              ' * the contents of the layer properties json file:\n\t{props}\n'
              ' * and the contents of the MapCookbook json:\n\t{cbook}\n'.format(
                  props=cmf.layer_properties,
                  cbook=cmf.map_definitions
              ))
        print('-------------------------------------\n')
        exit(0)


# TODO: asmith 2020/03/04
# This commandline interface and arg parser should be merged with other commandline interfaces
# such as the one in mapactionpy_controller.check_naming_convention.py
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This tool checks the internal self-consistency of the cookbook file, layerProperties file and the'  # noqa
                    ' layerfiles within the layerDirectory'
    )
    parser.add_argument("-c", "--cmf", dest="cmf_desc", required=True,
                        help="path to CMF description file", metavar="FILE", type=lambda x: is_valid_file(parser, x))
    parser.add_argument("-e", "--layer-file-extension", dest="layer_file_extension", required=True,
                        help="file extension layer files which will be checked against the layer_properties.json file")

    args = parser.parse_args()
    main(args.cmf_desc, args.layer_file_extension)
