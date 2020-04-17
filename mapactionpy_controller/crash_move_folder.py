import json
import os
# from jsonschema import validate


class CrashMoveFolder:
    def __init__(self, cmf_path, verify_on_creation=True):

        self.path = os.path.dirname(cmf_path)

        with open(cmf_path, 'r') as f:
            obj = json.loads(f.read())

            # Doubtless there is a more elegant way to do this.
            # 8 directories (alphabetical order just for readability)
            self.original_data = os.path.join(self.path, obj['original_data'])
            self.active_data = os.path.join(self.path, obj['active_data'])
            self.layer_rendering = os.path.join(self.path, obj['layer_rendering'])
            self.legend_images = os.path.join(self.path, obj['legend_images'])
            self.map_templates = os.path.join(self.path, obj['map_templates'])
            self.map_projects = os.path.join(self.path, obj['map_projects'])
            self.export_dir = os.path.join(self.path, obj['export_dir'])
            # 5 files (alphabetical order just for readablity)
            self.data_nc_definition = os.path.join(self.path, obj['data_nc_definition'])
            self.layer_nc_definition = os.path.join(self.path, obj['layer_nc_definition'])
            self.layer_properties = os.path.join(self.path, obj['layer_properties'])
            self.map_definitions = os.path.join(self.path, obj['map_definitions'])
            self.map_projects_nc_definition = os.path.join(self.path, obj['map_projects_nc_definition'])
            self.map_template_nc_definition = os.path.join(self.path, obj['map_template_nc_definition'])
            # others
            self.arcgis_version = obj['arcgis_version']
            # self.categories = obj['categories']

        if verify_on_creation and (not self.verify_paths()):
            failing_paths = [path for path, valid in self._get_path_verification_as_dict().items() if not valid]
            failing_paths_str = "\n\t".join(failing_paths)
            raise ValueError("Unable to verify existence of all files and directories defined in "
                             "CrashMoveFolder '{}'. The values for these parameters could not be located:\n\t"
                             "{}".format(cmf_path, failing_paths_str))

    def _get_path_verification_as_dict(self):
        results = {}

        # 8 dirs (alphabetical order just for readability)
        results['active_data'] = os.path.isdir(self.active_data)
        results['export_dir'] = os.path.isdir(self.export_dir)
        results['layer_rendering'] = os.path.isdir(self.layer_rendering)
        results['legend_images'] = os.path.isdir(self.legend_images)
        results['map_projects'] = os.path.isdir(self.map_projects)
        results['map_templates'] = os.path.isdir(self.map_templates)
        results['original_data'] = os.path.isdir(self.original_data)
        # 6 files (alphabetical order just for readability)
        results['data_nc_definition'] = os.path.exists(self.data_nc_definition)
        results['layer_nc_definition'] = os.path.exists(self.layer_nc_definition)
        results['layer_properties'] = os.path.exists(self.layer_properties)
        results['map_definitions'] = os.path.exists(self.map_definitions)
        results['map_projects_nc_definition'] = os.path.exists(self.map_projects_nc_definition)
        results['map_template_nc_definition'] = os.path.exists(self.map_template_nc_definition)

        return results

    def verify_paths(self):
        # return all(all(_verify_paths().values()), self.verify_mxds())
        return all(self._get_path_verification_as_dict().values())
