import argparse
import os
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
import mapactionpy_controller.data_name_convention as data_name_convention


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
        return False
    else:
        return arg


def test_contents_of_dir(dir, name_conv_definition, file_ext):
    nc = data_name_convention.DataNameConvention(name_conv_definition)
    nc.regex.groupindex

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
                elif result.is_valid:
                    pass
                    # print("valid filename: {}".format(f))
                else:
                    print("one or more clauses not found in lookup tables : {}".format(f))
                    rdict = result._asdict()

                    for clausename in nc.regex.groupindex:
                        cdict = rdict[clausename]._asdict()
                        if (clausename in cdict) and not rdict[clausename].is_valid:
                            print("{} clause value {} is_valid = {}".format(
                                clausename,
                                cdict[clausename],
                                rdict[clausename].is_valid))


def main():
    args = get_args()

    cmf = CrashMoveFolder(args.cmf_config_path)

    # test data names
    test_contents_of_dir(cmf.active_data, cmf.dnc_definition, '.shp')

    # test layer names
    test_contents_of_dir(cmf.layer_rendering, cmf.layer_nc_definition, '.lyr')

    # test mxd names
    test_contents_of_dir(cmf.mxd_products, cmf.mxd_nc_definition, '.mxd')


def get_args():
    parser = argparse.ArgumentParser(
        description=('This tool checks the conformance with the naming-convention for selected'
                     'files within the Crash Move Folder')
    )
    parser.add_argument("cmf_config_path", help="path to layer directory", metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))

    return parser.parse_args()


if __name__ == "__main__":
    main()
