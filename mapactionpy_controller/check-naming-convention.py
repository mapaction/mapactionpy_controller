import argparse
import os
from crash_move_folder import CrashMoveFolder
import data_name_convention 

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
        return False
    else:
        return arg
"""

def is_valid_directory(parser, arg):
    if os.path.isdir(arg):
        return arg
    else:
        parser.error("The directory %s does not exist!" % arg)
        return False
"""

def test_contents_of_dir(dir, name_conv_definition, file_ext):
    dnc = data_name_convention.DataNameConvention(name_conv_definition)
    dnc.regex.groupindex

    for root, dirs, files in os.walk(dir):  # pylint: disable=unused-variable
        for f in files:
            basename, extension = os.path.splitext(f)
            if extension in file_ext:
                result = dnc.validate(basename)
                #print("filename: to test {}".format(f))

                if not result:
                    print("error filename does not match regex: {}".format(f))
                elif result.is_valid:
                    pass
                    #print("valid filename: {}".format(f))
                else:
                    print("one or more clauses not found in lookup tables : {}".format(f))
                    rdict = result._asdict()

                    for clausename in dnc.regex.groupindex:
                        cdict = rdict[clausename]._asdict()
                        if (clausename in cdict) and not rdict[clausename].is_valid:
                            print("{} clause value {} is_valid = {}".format(
                                clausename,
                                cdict[clausename],
                                rdict[clausename].is_valid))
                        



def main(args):
    cmf = CrashMoveFolder(args.cmf_config_path)
    
    #test data names
    test_contents_of_dir(cmf.active_data, cmf.dnc_definition, '.shp')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='This tool checks the conformance with the naming-convention for selected files within the Crash Move Folder'
    )
    parser.add_argument("cmf_config_path", help="path to layer directory", metavar="FILE", 
                        type=lambda x: is_valid_file(parser, x))

    args = parser.parse_args()
    main(args)
