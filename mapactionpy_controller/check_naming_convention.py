import os
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.event import Event
import mapactionpy_controller.name_convention as name_convention
from mapactionpy_controller.steps import Step
import glob


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


def extract_naming_results_messages(name_results, extract_failures_only):
    messages = set()

    if extract_failures_only:
        # filtered_list = filter(lambda r: (not r.is_valid), name_results)
        filtered_list = [r for r in name_results if not r.is_valid]
    else:
        filtered_list = name_results

    for ncr in filtered_list:
        messages.add(ncr.get_message)

    return messages


def get_dir_checker(dir_to_check, nc_desc_file, extn_to_check, inc_valid):
    def check_dir(**kwargs):
        nc = name_convention.NamingConvention(nc_desc_file)
        nrs = get_naming_results_for_dir(dir_to_check, nc, extn_to_check)
        msgs = extract_naming_results_messages(nrs, (not inc_valid))
        num_of_failure = sum([int(not r.is_valid) for r in nrs])
        if num_of_failure:
            raise ValueError('\n'.join(msgs))

        # count of all the invalid names
        return msgs

    return check_dir


def get_defaultcmf_step_list(cmf_config_path, verbose):
    cmf = CrashMoveFolder(cmf_config_path)

    ncs_to_check = (
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
                get_dir_checker(dir_to_check, nc_desc_file, extn_to_check, verbose),
                "'Checking '{}' files in '{}' match relevant naming convention".format(extn_to_check, base_name),
                "All '{}' files in '{}' match the relevant naming convention".format(extn_to_check, base_name),
                "One of more '{}' files in '{}' did not match the relevant naming convention".format(
                    extn_to_check, base_name)
            )
        )

    return name_convention_steps


def _get_active_data_sub_dirs(cmf):
    list_subfolders_with_paths = []
    for root, dirs, files in os.walk(cmf.active_data):
        if os.path.normpath(root) == os.path.normpath(cmf.active_data):
            list_subfolders_with_paths = [(os.path.join(root, dir), dir) for dir in dirs]

    return list_subfolders_with_paths


def _get_all_gisfiles(cmf):
    shapefiles_with_paths = []

    for extn in ['.shp', '.img', '.tif']:
        for f_path in glob.glob('{}/*/*{}'.format(cmf.active_data, extn)):
            shapefiles_with_paths.append(os.path.basename(f_path))

    return shapefiles_with_paths


def get_single_file_checker(d_name, nc, verbose):
    # hello world
    def check_gis_data_name(**kwargs):
        ncr = nc.validate(d_name)
        if not ncr.is_valid:
            raise ValueError(ncr.get_message)

        if verbose:
            return ncr.get_message

    return check_gis_data_name


def get_active_data_step_list(humev_config_path, verbose):
    humev = Event(humev_config_path)
    cmf = CrashMoveFolder(humev.cmf_descriptor_path)

    nc = name_convention.NamingConvention(cmf.data_nc_definition)

    dnc_per_dir_steps = []
    for base_name in _get_all_gisfiles(cmf):
        # return_code += check_dir(dir_to_check, nc_desc_file, extn_to_check, args.inc_valid)
        # base_name = os.path.basename(dir_to_check)
        dnc_per_dir_steps.append(
            Step(
                get_single_file_checker(base_name, nc, verbose),
                "Checking the file '{}' against the data naming convention".format(base_name),
                "The file '{}' matches the data naming convention".format(base_name),
                "The file '{}' does not match the data naming convention".format(base_name)
            )
        )

    return dnc_per_dir_steps
