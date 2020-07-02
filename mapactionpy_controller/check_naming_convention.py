import glob
import logging
import os

import mapactionpy_controller.name_convention as name_convention
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.event import Event
from mapactionpy_controller.steps import Step


def get_defaultcmf_step_list(cmf_config_path, verbose):
    """
    Generates a list of Steps, each of which execucutes a suitable naming convention test
    for a static item within the crash move folder.
    """
    cmf = CrashMoveFolder(cmf_config_path)

    ncs_to_check = (
        (cmf.layer_rendering, cmf.layer_nc_definition, '.lyr', 'layer'),
        (cmf.layer_rendering, cmf.layer_nc_definition, '.qml', 'layer'),
        (cmf.layer_rendering, cmf.layer_nc_definition, '.qlr', 'layer'),
        (cmf.map_projects, cmf.map_projects_nc_definition, '.qgs', 'map project'),
        (cmf.map_projects, cmf.map_projects_nc_definition, '.mxd', 'map project'),
        (cmf.map_templates, cmf.map_template_nc_definition, '.qgs', 'map template'),
        (cmf.map_templates, cmf.map_template_nc_definition, '.pagx', 'map template'),
        (cmf.map_templates, cmf.map_template_nc_definition, '.mxd', 'map template')
    )

    name_convention_steps = []

    for dir_to_check, nc_desc_file, extn_to_check, convention_name in ncs_to_check:
        nc = name_convention.NamingConvention(nc_desc_file)
        name_convention_steps.extend(
            _step_builer(_get_all_files(dir_to_check, extn_to_check), nc, verbose, convention_name))

    return name_convention_steps


def _get_all_files(dir, extn):
    return glob.glob('{}/*{}'.format(dir, extn))


def get_active_data_step_list(humev_config_path, verbose):
    """
    Generates a list of Steps, each of which execucutes a suitable naming convention test
    for a GIS dataset with the `2_Active_data` folder within the crash move folder.
    """
    humev = Event(humev_config_path)
    cmf = CrashMoveFolder(humev.cmf_descriptor_path)
    nc = name_convention.NamingConvention(cmf.data_nc_definition)
    return _step_builer(_get_all_gisfiles(cmf), nc, verbose, 'data')


def _get_all_gisfiles(cmf):
    gisfiles_with_paths = []

    for extn in ['.shp', '.img', '.tif']:
        gisfiles_with_paths.extend(glob.glob('{}/*/*{}'.format(cmf.active_data, extn)))

    return gisfiles_with_paths


def get_single_file_checker(f_path, nc, verbose):
    def check_data_name(**kwargs):
        f_name = os.path.basename(f_path)
        ncr = nc.validate(f_name)
        if not ncr.is_valid:
            raise ValueError(ncr)

        return ncr

    return check_data_name


def _step_builer(file_list, nc, verbose, convention_name):
    step_list = []
    for f_path in file_list:
        # return_code += check_dir(dir_to_check, nc_desc_file, extn_to_check, args.inc_valid)
        base_name = os.path.basename(f_path)
        step_list.append(
            Step(
                get_single_file_checker(f_path, nc, verbose),
                logging.WARNING,
                "Checking the file '{}' against the {} naming convention".format(base_name, convention_name),
                "The file '{}' matches the {} naming convention".format(base_name, convention_name),
                "The file '{}' does not match the {} naming convention".format(base_name, convention_name)
            )
        )

    return step_list
