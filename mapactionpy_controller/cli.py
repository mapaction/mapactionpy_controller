import argparse
import os

import mapactionpy_controller.check_naming_convention as cnc
import mapactionpy_controller.config_verify as config_verify
import mapactionpy_controller.plugin_controller as plugin_controller
from mapactionpy_controller.main_stack import process_stack

VERB_BUILD = 'build'
VERB_CREATE = 'create'
VERB_LIST = 'list'
VERB_UPDATE = 'update'
VERB_UPLOAD = 'upload'
VERB_VERIFY = 'verify'


def noun_defaultcmf_print_output(args):
    if args.verb == VERB_VERIFY:
        cv_steps = config_verify.get_config_verify_steps(args.cmf_desc_path, ['.lyr'])
        # process_stack(cv_steps, None)
        cv_steps.extend(cnc.get_defaultcmf_step_list(args.cmf_desc_path))
        process_stack(cv_steps, None)
    else:
        raise NotImplementedError(args)


def noun_humevent_print_output(args):
    raise NotImplementedError(args)


def noun_gisdata_print_output(args):
    if args.verb == VERB_VERIFY:
        nc_steps = cnc.get_active_data_step_list(args.humevent_desc_path)
        process_stack(nc_steps, None)
        # print(nc_steps)
    else:
        raise NotImplementedError(args)


def noun_maps_print_output(args):
    if args.verb == VERB_BUILD:
        build_maps(args.humevent_desc_path, args.map_number, args.dry_run)
    else:
        raise NotImplementedError(args)


def build_maps(humevent_desc_path, map_number, dry_run):
    # build_steps = config_verify.get_config_verify_steps(args.cmf_desc_path, ['.lyr'])
    # build_steps.append(cnc.get_defaultcmf_step_list(args.cmf_desc_path, False))
    # build_steps.append(cnc.get_active_data_step_list(args.humevent_desc_path, True))
    # main_stack.process_stack(build_steps)
    my_runner = process_stack(plugin_controller.get_plugin_step(), humevent_desc_path)
    process_stack(plugin_controller.get_cookbook_steps(my_runner, map_number, dry_run), None)

    # map_nums = None
    # if map_number:
    #     map_nums = [map_number]

    # for recipe in plugin_controller.select_recipes(my_cookbook, map_nums):
    #     product_steps = plugin_controller.get_per_product_steps(my_runner, recipe.mapnumber, recipe.product)
    #     process_stack(product_steps, recipe)


all_nouns = {
    'defaultcmf': ('Print info about the Default Crash Move Folder', noun_defaultcmf_print_output),
    'humevent': ('Access and update info about a Humanitarian Event', noun_humevent_print_output),
    'gisdata': ('Access and update info about the GIS data collected for a Humanitarian Event',
                noun_gisdata_print_output),
    'maps': ('Access, build, update and upload maps for a Humanitarian Event', noun_maps_print_output)
}

all_verbs = {
    'defaultcmf': [
        (VERB_VERIFY, 'Verify the internal self consistency of the Default Crash Move Folder, without reference'
                      ' to any country or situational GIS data')
    ],
    'humevent': [
        (VERB_CREATE, 'Create a new Humanitarian Event description file. Values are read from relevant'
                      ' environment variables'),
        (VERB_UPDATE, 'Update an existing Humanitarian Event description file. Values are read from relevant'
                      ' environment variables'),
        (VERB_VERIFY, 'Verify the internal self consistency of the Humanitarian Event description, without'
                      ' reference to any country or situational GIS data')
    ],
    'gisdata': [
        (VERB_VERIFY, 'Verify that the "active" GIS data adheres to relevant GIS standards (eg Data Naming'
                      ' Convention and Schemas)')
    ],
    'maps': [
        (VERB_BUILD, 'Create the maps described in the MapCookbook. Existing maps are recreated if any'
                     ' of the inputs have changed.'),
        (VERB_UPLOAD, 'Upload maps to the publishing site')
    ]
}


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error('The file "%s" does not exist!' % arg)
    else:
        return arg


def _add_verbs_to_parser(verb_desc, parser):
    verb_grp = parser.add_mutually_exclusive_group(required=False)

    for verb, help_desc in verb_desc:
        flag = '--{}'.format(verb)

        verb_grp.add_argument(
            flag,
            action='store_const',
            dest='verb',
            help=help_desc,
            const=verb
        )


def _create_noun_parser(noun_str, subparser):
    noun_desc, noun_func = all_nouns[noun_str]

    parser = subparser.add_parser(noun_str)
    parser.description = (noun_desc)
    parser.set_defaults(func=noun_func)
    _add_verbs_to_parser(all_verbs[noun_str], parser)
    return parser


def get_args():
    mainparser = argparse.ArgumentParser(
        prog='mapchef',
        description=(
            "This tool does everything you'd ever what to make maps automatically."
            " Please look at the sub commands for more details"
        )
    )

    prs_nouns = mainparser.add_subparsers(title='available subcommands',
                                          description=(
                                              'To perform any useful tasks you will need to use one of'
                                              ' the subcommands listed below. For more detailed information'
                                              ' try `{} < subcommand > help`'.format(mainparser.prog)),
                                          help=None)

    # Noun: defaultcmf
    prs_defaultcmf = _create_noun_parser('defaultcmf', prs_nouns)
    prs_defaultcmf.add_argument(
        'cmf_desc_path',
        metavar='crash-move-folder-description-file',
        help='The path to Crash Move Foler (CMF) description file.',
        type=lambda x: is_valid_file(prs_defaultcmf, x)
    )

    # Noun: humevent
    prs_humevent = _create_noun_parser('humevent', prs_nouns)
    # It is acceptable that the `humevent_desc_path` does not exist for `humevent create`
    prs_humevent.add_argument(
        'humevent_desc_path',
        metavar='humanitarian-event-description-file',
        help='The path to Humanitarian Event description file.'
    )

    # Noun: gisdata
    prs_gisdata = _create_noun_parser('gisdata', prs_nouns)
    prs_gisdata.add_argument(
        'humevent_desc_path',
        metavar='humanitarian-event-description-file',
        help='The path to Humanitarian Event description file.',
        type=lambda x: is_valid_file(prs_humevent, x)
    )

    # Noun: maps
    prs_maps = _create_noun_parser('maps', prs_nouns)
    prs_maps.add_argument(
        'humevent_desc_path',
        metavar='humanitarian-event-description-file',
        help='The path to Humanitarian Event description file.',
        type=lambda x: is_valid_file(prs_humevent, x)
    )

    prs_maps.add_argument(
        '--map-number',
        metavar='"Map Number"',
        help=('The number of an individual map to produce (eg "MA0123"). This must match a map'
              ' number name that exists in the MapCookbook. If this option is not specified then'
              ' all maps in the MapCookbook will be created.')
    )

    maps_options_grp = prs_maps.add_mutually_exclusive_group(required=False)

    maps_options_grp.add_argument(
        '--force',
        action='store_true',
        help=('Generate a new version of the specified products, even if no change is detected'
              ' in any of the input files. (`--force` and `--dry-run`  cannot'
              ' be specified together.)')
    )

    maps_options_grp.add_argument(
        '--dry-run',
        action='store_true',
        help=('Do not generate a new version of the specified products. Run through each step'
              ' and attempt to identify any potential errors. (`--dry-run` and `--force` cannot'
              ' be specified together.)')
    )

    return mainparser.parse_args()


def entry_point():
    args = get_args()
    args.func(args)


if __name__ == "__main__":
    entry_point()
