import os
import argparse

VERB_BUILD = 'build'
VERB_CREATE = 'create'
VERB_LIST = 'list'
VERB_UPDATE = 'update'
VERB_UPLOAD = 'upload'
VERB_VERIFY = 'verify'


def noun_defaultcmf_print_output(args):
    print(args)


def noun_humevent_print_output(args):
    print(args)


def noun_gisdata_print_output(args):
    print(args)


def noun_maps_print_output(args):
    print(args)


all_nouns = {
    'defaultcmf': ('Print info about the Default Crash Move Folder', noun_defaultcmf_print_output),
    'humevent': ('Access and update info about a Humanitarian Event', noun_humevent_print_output),
    'gisdata': ('Access and update info about the GIS data collected for a Humanitarian Event', noun_gisdata_print_output),
    'maps': ('Access, build, update and upload maps for a Humanitarian Event', noun_maps_print_output)
}

all_verbs = {
    'defaultcmf': [
        (VERB_VERIFY, 'Verify the internal self consistancy of the Default Crash Move Folder, without reference'
                      ' to any country or situational GIS data')
    ],
    'humevent': [
        (VERB_CREATE, 'Create a new Humanitarian Event description file. Values are read from relevent'
                      ' environment variables'),
        (VERB_UPDATE, 'Update an existing Humanitarian Event description file. Values are read from relevent'
                      ' environment variables'),
        (VERB_VERIFY, 'Verify the internal self consistancy of the Humanitarian Event description, without'
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
        parser.error("The file %s does not exist!" % arg)
        return False
    else:
        return arg


def _add_verbs_to_parser(verb_desc, parser):
    verb_grp = parser.add_mutually_exclusive_group(required=False)

    for verb, help_desc in verb_desc:
        flag = '--{}'.format(verb)

        verb_grp.add_argument(
            flag,
            action='store_const',
            dest='my_action',
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
            "Please look at the sub commands for more details"
        )
    )
    prs_nouns = mainparser.add_subparsers(title='extra-subcommands',
                                          description='stuff you can do with valid subcommands',
                                          help='helo world additional help')

    # Noun: defaultcmf
    prs_defaultcmf = _create_noun_parser('defaultcmf', prs_nouns)
    prs_defaultcmf.add_argument(
        'cmf_desc_path',
        metavar='crash-move-folder-description-file',
        help='The path to Humanitarian Event description file.',
        type=lambda x: is_valid_file(prs_defaultcmf, x)
    )

    # Noun: humevent
    prs_humevent = _create_noun_parser('humevent', prs_nouns)
    prs_humevent.add_argument(
        'humevent_desc_path',
        metavar='humanitarian-event-description-file',
        help='The path to Humanitarian Event description file.',
        type=lambda x: is_valid_file(prs_humevent, x)
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
        '--map-name',
        metavar='"Map Name"',
        help=('The name of an individual map to produce. This must match a product name that'
              ' exists in the MapCookbook. If this option is not specified then'
              ' all maps in the MapCookbook will be created.')
    )

    maps_options_grp = prs_maps.add_mutually_exclusive_group(required=False)

    maps_options_grp.add_argument(
        '--force',
        action='store_true',
        help=('Generate a new verion of the specificed products, even if no change is detected'
              ' in any of the input files. (`--dry-run` and `--force` cannot'
              ' be specificed together.)')
    )

    maps_options_grp.add_argument(
        '--dry-run',
        action='store_true',
        help=('Do not generate a new verion of the specificed products. Run through each step'
              ' and attempt to identify any potential errors. (`--dry-run` and `--force` cannot'
              ' be specificed together.)')
    )

    return mainparser.parse_args()


def entry_point():
    args = get_args()
    args.func(args)


if __name__ == "__main__":
    entry_point()
