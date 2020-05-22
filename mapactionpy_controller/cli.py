import os
import argparse

VERB_BUILD = 'build'
VERB_CREATE = 'create'
VERB_LIST = 'list'
VERB_UPDATE = 'update'
VERB_UPLOAD = 'upload'
VERB_VERIFY = 'verify'


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
        return False
    else:
        return arg


def noun_defaultcmf_print_output(args):
    print(args)


def noun_humevent_print_output(args):
    print(args)


def noun_gisdata_print_output(args):
    print(args)


def noun_maps_print_output(args):
    print(args)


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
    prs_defaultcmf = prs_nouns.add_parser('defaultcmf')
    prs_defaultcmf.description = ('Print info about the Default Crash Move Folder')
    prs_defaultcmf.set_defaults(func=noun_defaultcmf_print_output)

    relevant_verbs = [
        (VERB_VERIFY, 'Verify the internal self consistancy of the Default Crash Move Folder, without reference'
                      ' to any country or situational GIS data')
    ]
    _add_verbs_to_parser(relevant_verbs, prs_defaultcmf)

    prs_defaultcmf.add_argument(
        'cmf_desc_path',
        metavar='crash-move-folder-description-file'
    )

    # Noun: humevent
    prs_humevent = prs_nouns.add_parser('humevent')
    prs_humevent.description = ('Access and update info about a Humanitarian Event')
    prs_humevent.set_defaults(func=noun_humevent_print_output)

    relevant_verbs = [
        (VERB_CREATE, 'Create a new Humanitarian Event description file. Values are read from relevent'
                      ' environment variables'),
        (VERB_UPDATE, 'Update an existing Humanitarian Event description file. Values are read from relevent'
                      ' environment variables'),
        (VERB_VERIFY, 'Verify the internal self consistancy of the Humanitarian Event description, without'
                      ' reference to any country or situational GIS data')
    ]

    _add_verbs_to_parser(relevant_verbs, prs_humevent)

    prs_humevent.add_argument(
        'humevent_desc_path',
        metavar='humanitarian-event-description-file'
    )

    # Noun: gisdata
    prs_gisdata = prs_nouns.add_parser('gisdata')
    prs_gisdata.description = ('Access and update info about the GIS data collected for a Humanitarian Event')
    prs_gisdata.set_defaults(func=noun_gisdata_print_output)

    relevant_verbs = [
        (VERB_VERIFY, 'Verify that the "active" GIS data adheres to relevant GIS standards (eg Data Naming'
                      ' Convention and Schemas')
    ]

    _add_verbs_to_parser(relevant_verbs, prs_gisdata)

    prs_humevent.add_argument(
        'humevent_desc_path',
        metavar='humanitarian-event-description-file'
    )

    # Noun: maps
    prs_maps = prs_nouns.add_parser('maps')
    prs_maps.description = ('Access, build, update and upload maps for a Humanitarian Event')
    prs_maps.set_defaults(func=noun_maps_print_output)

    relevant_verbs = [
        (VERB_BUILD, 'Create the maps described in the MapCookbook. Existing maps are recreated if any'
                     ' of the inputs have changed.'),
        (VERB_UPLOAD, 'Verify that the "active" GIS data adheres to relevant GIS standards (eg Data Naming'
                      ' Convention and Schemas')
    ]

    _add_verbs_to_parser(relevant_verbs, prs_maps)

    prs_maps.add_argument(
        'humevent_desc_path',
        metavar='humanitarian-event-description-file'
    )

    prs_maps.add_argument(
        '--map-name'
    )

    maps_options_grp = prs_maps.add_mutually_exclusive_group(required=False)

    maps_options_grp.add_argument(
        '--force',
        action='store_true'
    )

    maps_options_grp.add_argument(
        '--dry-run',
        action='store_true'
    )

    return mainparser.parse_args()


def entry_point():
    args = get_args()
    args.func(args)


if __name__ == "__main__":
    entry_point()
