import json
import os
# from jsonschema import validate


class CrashMoveFolder:
    def __init__(self, cmf_path, verify_on_creation=True):

        self.path = os.path.dirname(cmf_path)

        with open(cmf_path, 'r') as f:
            obj = json.loads(f.read())

            # Doubtless there is a more elegant way to do this.
            # 7 directories (alphabeltical order just for readablity)
            self.original_data = os.path.join(self.path, obj['original_data'])
            self.active_data = os.path.join(self.path, obj['active_data'])
            self.layer_rendering = os.path.join(self.path, obj['layer_rendering'])
            self.mxd_templates = os.path.join(self.path, obj['mxd_templates'])
            self.mxd_products = os.path.join(self.path, obj['mxd_products'])
            self.qgis_templates = os.path.join(self.path, obj['qgis_templates'])
            self.export_dir = os.path.join(self.path, obj['export_dir'])
            # 5 files (alphabeltical order just for readablity)
            self.data_nc_definition = os.path.join(self.path, obj['data_nc_definition'])
            self.layer_nc_definition = os.path.join(self.path, obj['layer_nc_definition'])
            self.layer_properties = os.path.join(self.path, obj['layer_properties'])
            self.map_definitions = os.path.join(self.path, obj['map_definitions'])
            self.mxd_nc_definition = os.path.join(self.path, obj['mxd_nc_definition'])
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

        # 7 dirs (alphabeltical order just for readablity)
        results['active_data'] = os.path.isdir(self.active_data)
        results['export_dir'] = os.path.isdir(self.export_dir)
        results['layer_rendering'] = os.path.isdir(self.layer_rendering)
        results['mxd_products'] = os.path.isdir(self.mxd_products)
        results['mxd_templates'] = os.path.isdir(self.mxd_templates)
        results['original_data'] = os.path.isdir(self.original_data)
        results['qgis_templates'] = os.path.isdir(self.qgis_templates)
        # 5 files (alphabeltical order just for readablity)
        results['data_nc_definition'] = os.path.exists(self.data_nc_definition)
        results['layer_nc_definition'] = os.path.exists(self.layer_nc_definition)
        results['layer_properties'] = os.path.exists(self.layer_properties)
        results['map_definitions'] = os.path.exists(self.map_definitions)
        results['mxd_nc_definition'] = os.path.exists(self.mxd_nc_definition)

        return results

    def verify_paths(self):
        # return all(all(_verify_paths().values()), self.verify_mxds())
        return all(self._get_path_verification_as_dict().values())

    def verify_mxds(self):
        result = True
        for category in (self.categories):
            for orientation in ['landscape', 'portrait']:
                templateFileName = self.arcgis_version + "_" + category + "_" + orientation

                if (category == "reference"):
                    templateFileName = templateFileName + "_bottom"
                templateFileName = templateFileName + ".mxd"
                if not os.path.exists(self.mxd_templates):
                    result = False
        return result
