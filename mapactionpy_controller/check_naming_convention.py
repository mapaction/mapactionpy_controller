import argparse
import os
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
import mapactionpy_controller.name_convention as name_convention
from mapactionpy_controller.steps import Step


# def is_valid_file(parser, arg):
#     if not os.path.exists(arg):
#         parser.error("The file %s does not exist!" % arg)
#         return False
#     else:
#         return arg


def get_naming_results_for_dir(dir, nc, file_ext=''):
    """
    Returns:
        - None if there are no naming convention violations
        - An object describing the violations if they exist.
    """
    def _is_relevant_file(f):
        f_path = os.path.join(dir, f)
        extension = os.path.splitext(f)[1]
        return (os.path.isfile(f_path)) and (extension == file_ext)

    filenames = os.listdir(dir)
    filenames = filter(_is_relevant_file, filenames)

    return [nc.validate(fi) for fi in filenames]


def extract_naming_results_messages(name_results, extract_failures_only=True):
    messages = set()

    if extract_failures_only:
        filtered_list = filter(lambda r: (not r.is_valid), name_results)
    else:
        filtered_list = name_results

    for ncr in filtered_list:
        messages.add(ncr.get_message)

    return messages


def get_dir_checker(dir_to_check, nc_desc_file, extn_to_check, inc_valid):
    def check_dir():
        nc = name_convention.NamingConvention(nc_desc_file)
        nrs = get_naming_results_for_dir(dir_to_check, nc, extn_to_check)
        msgs = extract_naming_results_messages(nrs, extract_failures_only=(not inc_valid))
        if len(msgs):
            raise ValueError('\n'.join(msgs))

        # count of all the invalid names
        return sum(int(not r.is_valid) for r in nrs)

    return check_dir


def get_step_list(cmf_config_path, inc_valid):
    cmf = CrashMoveFolder(cmf_config_path)

    # TODO: handle case where there is a need to drill down into subdirectories
    # eg `cmf.active_data`
    ncs_to_check = (
        (cmf.active_data, cmf.data_nc_definition, '.shp'),
        (cmf.layer_rendering, cmf.layer_nc_definition, '.lyr'),
        (cmf.layer_rendering, cmf.layer_nc_definition, '.qml'),
        (cmf.layer_rendering, cmf.layer_nc_definition, '.qlr'),
        (cmf.map_projects, cmf.map_projects_nc_definition, '.qgs'),
        (cmf.map_projects, cmf.map_projects_nc_definition, '.mxd'),
        (cmf.map_templates, cmf.map_template_nc_definition, '.qgs'),
        (cmf.map_templates, cmf.map_template_nc_definition, '.pagx'),
        (cmf.map_templates, cmf.map_template_nc_definition, '.mxd')
    )

    name_convention_steps = []

    for dir_to_check, nc_desc_file, extn_to_check in ncs_to_check:
        # return_code += check_dir(dir_to_check, nc_desc_file, extn_to_check, args.inc_valid)
        base_name = os.path.basename(dir_to_check)
        name_convention_steps.append(
            Step(
                get_dir_checker(dir_to_check, nc_desc_file, extn_to_check, inc_valid),
                "'Checking '{}' files in '{}' match relevant naming convention".format(extn_to_check, base_name),
                "All '{}' files in '{}' match the relevant naming convention".format(extn_to_check, base_name),
                "One of more '{}' files in '{}' did not match the relevant naming convention".format(
                    extn_to_check, base_name)
            )
        )

    return name_convention_steps


# def main():
#     args = get_args()
#     cmf = CrashMoveFolder(args.cmf_config_path)
#     return_code = 0

#     ncs_to_check = (
#         (cmf.active_data, cmf.data_nc_definition, '.shp'),
#         (cmf.layer_rendering, cmf.layer_nc_definition, '.lyr'),
#         (cmf.layer_rendering, cmf.layer_nc_definition, '.qml'),
#         (cmf.layer_rendering, cmf.layer_nc_definition, '.qlr'),
#         (cmf.map_projects, cmf.map_projects_nc_definition, '.qgs'),
#         (cmf.map_projects, cmf.map_projects_nc_definition, '.mxd'),
#         (cmf.map_templates, cmf.map_template_nc_definition, '.qgs'),
#         (cmf.map_templates, cmf.map_template_nc_definition, '.pagx'),
#         (cmf.map_templates, cmf.map_template_nc_definition, '.mxd')
#     )

#     name_convention_steps = []

#     for dir_to_check, nc_desc_file, extn_to_check in ncs_to_check:
#         # return_code += check_dir(dir_to_check, nc_desc_file, extn_to_check, args.inc_valid)
#         base_name = os.path.basename(dir_to_check)
#         name_convention_steps.append(
#             Step(
#                 get_dir_checker(dir_to_check, nc_desc_file, extn_to_check, args.inc_valid),
#                 'Checking shapefiles in {} match data naming convention'.format(base_name),
#                 'All shapefiles in {} match the data naming convention'.format(base_name),
#                 'One of more shapefiles in CMF did not match the data naming convention'.format(base_name)
#             )
#         )

#     # Quit with the exit code
#     return return_code


# def get_args():
#     parser = argparse.ArgumentParser(
#         description=('This tool checks the conformance with the naming-convention for selected'
#                      'files within the Crash Move Folder')
#     )
#     parser.add_argument("cmf_config_path", help="path to layer directory", metavar="FILE",
#                         type=lambda x: is_valid_file(parser, x))
#     parser.add_argument(
#         '--inc-valid', action='store_true',
#         help='Include valid: Print messages for valid names in addition to printing messages for failing names',
#     )

#     return parser.parse_args()


# if __name__ == "__main__":
#     result = main()
#     exit(result)
