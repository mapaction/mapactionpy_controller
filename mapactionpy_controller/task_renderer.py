import os

import chevron

from mapactionpy_controller import TASK_TEMPLATES_DIR

# key = step.func
# value = filename for mustache template
mustache_template_lookup = {
    'check_gis_data_name': 'misnamed-gis-file',
    'check_file_in_wrong_directory': 'file-in-wrong-directory',
    'update_recipe_with_datasources': 'gis-data-missing',
    'schema_error': 'schema-error',
    'file_in_wrong_directory': 'file-in-wrong-directory',
    'multiple_matching_files': 'multiple-matching-files',
    '_runner.build_project_files': 'project-build-error',
    'check_dir': 'check-names-of-files-other-than-gis-files'
}

fallback_template = 'major-configuration-error'


def check_all_templates_exist():
    pass


def _get_task_template_path(func_name):
    m_name = mustache_template_lookup.get(func_name, fallback_template)
    return os.path.join(TASK_TEMPLATES_DIR, '{}.mustache'.format(m_name))


def get_task_template(func_name):
    m_path = _get_task_template_path(func_name)
    with open(m_path, 'r') as m_file:
        template = m_file.read()

    # print('template = {}='.format(template))
    return template


def _name_result_adapter(name_result):
    valid_clause_list = []
    invalid_clause_list = []
    if name_result.is_parsable:
        valid_clause_list = [clause.get_message for clause in name_result._asdict().values() if clause.is_valid]
        invalid_clause_list = [clause.get_message for clause in name_result._asdict().values() if not clause.is_valid]

    nr_dict = {
        'name_to_validate': name_result.name_to_validate,
        'is_parsable': name_result.is_parsable,
        'valid_clause_list': [
            {'valid_clause': clause_msg} for clause_msg in sorted(valid_clause_list)],
        'invalid_clause_list': [
            {'invalid_clause': clause_msg} for clause_msg in sorted(invalid_clause_list)]
    }

    return nr_dict


def _recipe_adapter(recipe):
    pass


def _recipe_lyr_adapter(lyr):
    pass

# values = {
#     'regex': '^ken_carto_fea_py_(.?)_(.?)_([phm][phm])(.*?).shp$',
#     'shpfile_list': [
#         {'shpf': r'GIS\2_Active_Data\207_carto\ken_carto_fea_py_s0_mapaction_pp_100kfeather.shp'},
#         {'shpf': r'GIS\2_Active_Data\207_carto\ken_carto_fea_py_s0_mapaction_pp_50kfeather.shp'},
#         {'shpf': r'GIS\2_Active_Data\207_carto\ken_carto_fea_py_s0_mapaction_pp_75kfeather.shp'}
#     ],
#     'event_id': '2020ken01',
#     'lyr_stuff': {
#         'lyr_name': 'mainmap-carto-fea-py-s0-allmaps',
#         'lyr_file_path': r'GIS\3_Mapping\31_Resources\312_Layer_files\mainmap-carto-fea-py-s0-allmaps.lyr',
#         'lyr_props_path': r'GIS\3_Mapping\31_Resources\316_Automation\layerProperties.json'
#     }
# }


def render_task_description(task_template, values):
    return chevron.render(task_template, values, def_ldel='<%', def_rdel='%>')


# testing
if __name__ == "__main__":
    pass
    # print(get_task_template('check_gis_data_name'))
    # print(get_task_description())
