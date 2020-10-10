import os

import chevron

from mapactionpy_controller import TASK_TEMPLATES_DIR


"""
Module `task_renderer`

There are some "adapter" functions available, which can be used extract key information from common
objects from within `mapactionpy_controller` into a format suitable for `self.context_data`. The
constructors for sub-classes of TaskReferralBase may used these as appropriate.

The adapter functions only cater for a single object of each type.
```
context_data = {}
context_data.expend(adapter1.(foo))
context_data.expend(adapter2.(bar))
```

Each adapter function maps an object to a key within `context_data`:
* `_name_result_adapter`; NamingResult -> 'name_result'
* `_cmf_description_adapter`; CrashMoveFolder -> `cmf`

"""


class TaskReferralBase(object):
    """
    Represents a senario where a task would need to be referred to a human. The class provides a unique
    identifer for the task, which must be useful by the external task-tracking system and the bolierplate
    description of the underlying problem that needs to be resolved.

    Different senarios are represented by subclassing this class. For example:
    * `DataFileNameTask` : A category of problems which relate to filenames.
    * `FixSchemaErrorTask` : A category of problems which relate to errors in the schema.

    Specific instances of thes object represent specific problems that require human intervention:
    * 'the file "foo.txt" is incorrectly named'
    * 'the file "bar.shp" is missing the attribute "place_name"'

    Subclasses must:
    A) Either:
        * Override the `_task_template_filename`. This should be the name of a file (excluding the extension).
          This file (which must have the extension `.mustache`) must exist in `TASK_TEMPLATES_DIR`.
        * Overide `_get_task_template` so that it returns the contents of a mustache template. This option
          allows for template files which exist in locations other than TASK_TEMPLATES_DIR, and hence can to
          more appropriate for plugins.
    B) Override `_primary_key_template` with a string mustache.io template as a string. When rendered template
       should provide a unique identifier for an instance of the class. This unique identifier must be valid
       (and meaningful) within the external task management system.
    C) Set `self.context_data` from within the constructor. `self.context_data` is a dict object that contains
       the relevant centextual information to be able to render the templates. The keys of `context_data` must
       match the tags within the mustache template for both the `_primary_key_template and the
       `_task_template_filename`. There are some adapter functions to help with this. These adapters take
       common objects from within `mapactionpy_controller` and extract key information into a format suitable
       for `self.context_data`.

    Note:
    The templates use the mustache.io format. However it is assumed the delimters left=`<%` and right=`%>` are
    used, rather than the eponymous defaults `{{` and `}}`. This is aviod ambiguity with JIRA's markup which
    also assigns special meaning to double-curly brackets.
    """
    _primary_key_template = 'Major Configuration Error'
    _task_template_filename = 'major-configuration-error'
    context_data = {}

    def __init__(self):
        self.template = self._get_task_template()

    def _get_task_template(self):
        m_path = os.path.join(TASK_TEMPLATES_DIR, '{}.mustache'.format(self._task_template_filename))
        with open(m_path, 'r') as m_file:
            template = m_file.read()

        return template

    def get_task_unique_summary(self):
        return chevron.render(self._primary_key_template, self.context_data, def_ldel='<%', def_rdel='%>')

    def get_task_description(self):
        return chevron.render(self.template, self.context_data, def_ldel='<%', def_rdel='%>')


class FixDataNameTask(TaskReferralBase):
    _task_template_filename = 'misnamed-gis-file'
    _primary_key_template = 'gisdata : <%name_result.name_to_validate%> : Incorrectly Named'

    def __init__(self, name_result, cmf):
        super(FixDataNameTask, self).__init__()
        self.context_data.update(_name_result_adapter(name_result))
        self.context_data.update(_cmf_description_adapter(cmf))


class FixFileInWrongDirTask(TaskReferralBase):
    _task_template_filename = 'file-in-wrong-directory'
    _primary_key_template = 'gisdata : ->TBC.folder_name<-'


class FixMissingGISDataTask(TaskReferralBase):
    _task_template_filename = 'gis-data-missing'
    _primary_key_template = 'TBC'


class FixSchemaErrorTask(TaskReferralBase):
    _task_template_filename = 'schema-error'
    _primary_key_template = 'TBC'


class FixMultipleMatchingFilesTask(TaskReferralBase):
    _task_template_filename = 'multiple-matching-files'
    _primary_key_template = 'TBC'


# def extract_context_data(status, step_func_name, **kwargs):
#     """
#     Returns the "dict of values" used by the mustache rendering
#     """
#     context_data = kwargs.copy()

#     if status < logging.WARNING:
#         # We just have an "INFO"
#         # Therefore expect this kwarg:
#         source_data = kwargs['result']
#     else:
#         # Something more serious
#         # Therefore expect these kwargs:
#         exp = kwargs['exp']
#         # stack_trace = kwargs['stack_trace']
#         # This _may_ be present but not guaranteed
#         # state = kwargs.get('result', None)
#         source_data = exp.args[0]

#     # TODO:
#     # In each case there may be a single item OR a list of items. If it is a list of items
#     # then there will be one JIRA task per item in the list.

#     if step_func_name == 'check_data_name' or step_func_name == 'check_dir':
#         context_data.update(_name_result_adapter(source_data))

#     if step_func_name == 'check_file_in_wrong_directory':
#         context_data.update(_misplaced_file_list_adapter(source_data))
#     if step_func_name == 'update_recipe_with_datasources':
#         context_data.update(_gis_data_missing_adapter(source_data))
#     if step_func_name == 'schema_error':
#         context_data.update(_schema_error_adapter(source_data))
#     if step_func_name == 'multiple_matching_files':
#         context_data.update(_multiple_matching_files_adapter(source_data))
#     if step_func_name == '_runner.build_project_files':
#         context_data.update(_build_project_files(source_data))

#     return context_data


def _build_project_files(map_report):
    pass


def _multiple_matching_files_adapter(lyr_results):
    pass


def _schema_error_adapter(schema_error):
    pass


def _misplaced_file_list_adapter(file_list):
    pass


def _gis_data_missing_adapter(missing_lyr):
    pass


def _cmf_description_adapter(cmf):
    return {'cmf': cmf.__dict__.copy()}


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

    return {'name_result': nr_dict}


def _recipe_adapter(recipe):
    # Example of return value style
    #
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
    pass


def _recipe_lyr_adapter(lyr):
    pass


# # testing
# if __name__ == "__main__":
#     pass
#     # print(get_task_template('check_gis_data_name'))
#     # print(get_task_description())
