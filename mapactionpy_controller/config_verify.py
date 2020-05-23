from mapactionpy_controller.map_cookbook import MapCookbook
from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
# from jsonschema import ValidationError
import os
import argparse
from mapactionpy_controller.steps import Step


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


class ConfigVerifier():
    def __init__(self, cmf_desc, lyr_file_exn_list):
        self.cmf_desc_path = cmf_desc
        self.lyr_file_exn_list = lyr_file_exn_list

    def check_cmf_description(self):
        try:
            CrashMoveFolder(self.cmf_desc_path)
            # print('The Crash Move Folder description file open correctly:\n"{}"\n'.format(
            #     self.cmf_desc_path
            # ))
        except ValueError:
            raise

    def check_json_file_schemas(self):
        try:
            # JSON schema validation is implicit in the creation of these objects
            cmf = CrashMoveFolder(self.cmf_desc_path)
            lp = LayerProperties(cmf, '', verify_on_creation=False)
            MapCookbook(cmf, lp, verify_on_creation=False)
            # print('No json validation problems were detected in the parsing of these two'
            #       ' files:\n"{}"\n"{}"'.format(lp.cmf.layer_properties, cmf.map_definitions)
            #       )
        except ValueError:
            raise

    def check_lyr_props_vs_rendering_dir(self):
        for lyr_exn in self.lyr_file_exn_list:
            try:
                cmf = CrashMoveFolder(self.cmf_desc_path)
                LayerProperties(cmf, lyr_exn, verify_on_creation=True)
                # print('No inconsistancy detected between:\n'
                #     ' * the contents of the layer properties json file:\n\t{props}\n'
                #     ' * and layer rendering dir:\n\t{render}\n'.format(
                #         props=cmf.layer_properties,
                #         render=cmf.layer_rendering
                #     ))
            except ValueError:
                raise

    def check_lyr_props_vs_map_cookbook(self):
        try:
            cmf = CrashMoveFolder(self.cmf_desc_path)
            lyrs = LayerProperties(cmf, '', verify_on_creation=False)
            MapCookbook(cmf, lyrs, verify_on_creation=True)
            # print('No inconsistancy detected between:\n'
            #       ' * the contents of the layer properties json file:\n\t{props}\n'
            #       ' * and the contents of the MapCookbook json:\n\t{cbook}\n'.format(
            #           props=cmf.layer_properties,
            #           cbook=cmf.map_definitions
            #       ))
        except ValueError:
            raise

    def get_args(self):
        parser = argparse.ArgumentParser(
            description='This tool checks the internal self-consistency various components of the Crash Move Folder,'
                        ' including several of the contained configuration files. Use sub-commands to specify which'
                        ' checks should be completed, or the special sub-comand `all` for all checks.'
        )
        parser.add_argument("-c", "--cmf", dest="cmf_desc", required=True,
                            help="path to CMF description file", metavar="FILE",
                            type=lambda x: is_valid_file(parser, x))

        subparsers = parser.add_subparsers(title='subcommands',
                                           description='valid subcommands',
                                           help='additional help')

        # `all` to call all sub commands
        parser_all = subparsers.add_parser('all')
        parser_all.description = ('Call all of the avilable subcommands to check validity')
        parser_all.set_defaults(func=self.check_all)

        parser_cmf_only = subparsers.add_parser('cmf-only')
        parser_cmf_only.description = ('Just checks the validity of the cmf_description file. This includes checking'
                                       ' that each of the file and directory paths specified are valid')
        parser_cmf_only.set_defaults(func=self.check_cmf_description)

        parser_lp_vs_rendering = subparsers.add_parser('lp-vs-rendering')
        parser_lp_vs_rendering.description = (
            'This tool checks the internal self-consistency of the cookbook file, layerProperties file and the'
            ' layerfiles within the layerDirectory'
        )
        parser_lp_vs_rendering.add_argument(
            '-e',
            '--layer-file-extension',
            dest='layer_file_extension',
            required=True,
            help='file extension layer files which will be checked against the layer_properties.json file'
        )
        parser_lp_vs_rendering.set_defaults(func=self.check_lyr_props_vs_rendering_dir)

        parser_lp_vs_cb = subparsers.add_parser('lp-vs-cb')
        parser_lp_vs_cb.description = (
            'This tool checks the internal self-consistency of the cookbook file, layerProperties file and the'
            ' layerfiles within the layerDirectory'
        )
        parser_lp_vs_cb.set_defaults(func=self.check_lyr_props_vs_map_cookbook)

        parser_lp_vs_cb = subparsers.add_parser('check-schemas')
        parser_lp_vs_cb.description = (
            'This tool checks the compliance of the json schemas for the cookbook file and the layerProperties file'
        )
        parser_lp_vs_cb.set_defaults(func=self.check_json_file_schemas)

        return parser.parse_args()

    # TODO look up a better way to handle the `all` option. Is there a way to extract each of teh functions from
    # the subparsers.get_defaults() method?
    def check_all(self, args):
        # for cmd_name, argparser in self.subparsers.choices.iteritems():
        #    if not cmd_name == 'all':
        #        func = argparser.get_default('func')
        #        func(args)
        # self.check_cmf_description(args)
        # self.check_json_file_schemas(args)
        # self.check_lyr_props_vs_rendering_dir(args)
        # self.check_lyr_props_vs_map_cookbook(args)
        pass


def get_config_verify_steps(cmf_desc_path, lyr_file_exn_list):
    cv = ConfigVerifier(cmf_desc_path, lyr_file_exn_list)

    config_verify_steps = [
        Step(
            cv.check_cmf_description,
            'Checking that the Crash Move Folder description file opens correctly',
            'The Crash Move Folder description file opened correctly',
            'Failed to open the Crash Move Folder description file correctly',
        ),
        Step(
            cv.check_json_file_schemas,
            'Checking that each of the configuration files matches their relevant schemas',
            'Each of the configuration files adheres to their relevant schemas',
            'Failed to verify one or more of the configuration files against the relevant schema',
        ),
        Step(
            cv.check_lyr_props_vs_rendering_dir,
            'Comparing the contents of the layer properties json file and the layer rendering directory',
            'Compared the contents of the layer properties json file and the layer rendering directory',
            'Inconsistancy found in between the contents of the layer properties json file and the layer'
            ' rendering directory'
        ),
        Step(
            cv.check_lyr_props_vs_map_cookbook,
            'Comparing the contents of the layer properties json file and the MapCookbook',
            'Compared the contents of the layer properties json file and the MapCookbook',
            'Inconsistancy found in between the contents of the layer properties json file and the MapCookbook'
        )
    ]

    return config_verify_steps

# def run_checks(args=None):
#     cv = ConfigVerifier()
#     if not args:
#         args = cv.get_args()
#     args.func(args)


# TODO: asmith 2020/03/04
# This commandline interface and arg parser should be merged with other commandline interfaces
# such as the one in mapactionpy_controller.check_naming_convention.py
if __name__ == "__main__":
    # run_checks()
    pass
