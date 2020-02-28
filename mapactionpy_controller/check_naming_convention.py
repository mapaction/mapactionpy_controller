import argparse
import os
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
import mapactionpy_controller.name_convention as data_name_convention


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
        return False
    else:
        return arg


def test_contents_of_dir(dir, name_conv_definition, file_ext):
    nc = data_name_convention.NamingConvention(name_conv_definition)
    nc.regex.groupindex
    return_code = 0

    print("*****************")
    print("CHECKING DIR {}".format(dir))
    print("*****************")

    for root, dirs, files in os.walk(dir):  # pylint: disable=unused-variable
        for f in files:
            basename, extension = os.path.splitext(f)
            if extension in file_ext:
                result = nc.validate(basename)
                if not result:
                    print("error filename does not match regex: {}".format(f))
                    return_code += 1
                elif result.is_valid:
                    pass
                    # print("valid filename: {}".format(f))
                else:
                    print("one or more clauses not found in lookup tables : {}".format(f))
                    rdict = result._asdict()
                    return_code += 1

                    for clausename in nc.regex.groupindex:
                        clause_details = rdict[clausename]
                        # print(clausename, cdict)
                        if not clause_details.is_valid:
                            print("\t{} is not a recognised value for the clause {}".format(
                                clause_details.Value,
                                clausename))

                    print

    return return_code


def main():
    args = get_args()
    cmf = CrashMoveFolder(args.cmf_config_path)
    return_code = 0

    # test data names
    return_code += test_contents_of_dir(cmf.active_data, cmf.data_nc_definition, '.shp')

    # test layer names
    return_code += test_contents_of_dir(cmf.layer_rendering, cmf.layer_nc_definition, '.lyr')

    # test mxd names
    return_code += test_contents_of_dir(cmf.mxd_products, cmf.mxd_nc_definition, '.mxd')

    # Quit with the exist code
    return return_code


def get_args():
    parser = argparse.ArgumentParser(
        description=('This tool checks the conformance with the naming-convention for selected'
                     'files within the Crash Move Folder')
    )
    parser.add_argument("cmf_config_path", help="path to layer directory", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))

    return parser.parse_args()


if __name__ == "__main__":
    result = main()
    exit(result)
