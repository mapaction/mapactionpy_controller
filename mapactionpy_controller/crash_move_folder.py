import json
import os
# from jsonschema import validate


class CrashMoveFolder:
    def __init__(self, cmf_path, verify_on_creation=True):

        self.path = os.path.dirname(cmf_path)

        with open(cmf_path, 'r') as f:
            obj = json.loads(f.read())

            # Doubtless there is a more elegant way to do this.
            # 7 dirs
            self.original_data = os.path.join(self.path, obj['original_data'])
            self.active_data = os.path.join(self.path, obj['active_data'])
            self.layer_rendering = os.path.join(self.path, obj['layer_rendering'])
            self.mxd_templates = os.path.join(self.path, obj['mxd_templates'])
            self.mxd_products = os.path.join(self.path, obj['mxd_products'])
            self.qgis_templates = os.path.join(self.path, obj['qgis_templates'])
            self.export_dir = os.path.join(self.path, obj['export_dir'])
            # 4 files
            self.event_description_file = os.path.join(self.path, obj['event_description_file'])
            self.data_nc_definition = os.path.join(self.path, obj['dnc_definition'])
            self.layer_nc_definition = os.path.join(self.path, obj['layer_nc_definition'])
            self.mxd_nc_definition = os.path.join(self.path, obj['mxd_nc_definition'])
            # other values
            self.default_jpeg_red_dpi = obj['default_jpeg_red_dpi']
            self.default_pdf_red_dpi = obj['default_pdf_red_dpi']
            self.default_emf_red_dpi = obj['default_emf_red_dpi']

        # paths_checked = self._verify_paths()
        if verify_on_creation and (not self.verify_paths()):
            failing_paths = [path for path, valid in self._verify_paths().items() if not valid]
            failing_paths_str = "\n\t".join(failing_paths)
            raise ValueError("Unable to verify existence of all files and directories defined in "
                             "CrashMoveFolder '{}'. The values for these parameters could not be located:\n\t"
                             "{}".format(cmf_path, failing_paths_str))

    def _verify_paths(self):
        results = {}

        # 7 dirs
        results['original_data'] = os.path.isdir(self.original_data)
        results['active_data'] = os.path.isdir(self.active_data)
        results['active_data'] = os.path.isdir(self.active_data)
        results['mxd_templates'] = os.path.isdir(self.mxd_templates)
        results['mxd_products'] = os.path.isdir(self.mxd_products)
        results['qgis_templates'] = os.path.isdir(self.qgis_templates)
        results['export_dir'] = os.path.isdir(self.export_dir)
        # 4 files
        results['event_description_file'] = os.path.exists(self.event_description_file)
        results['data_nc_definition'] = os.path.exists(self.data_nc_definition)
        results['layer_nc_definition'] = os.path.exists(self.layer_nc_definition)
        results['mxd_nc_definition'] = os.path.exists(self.mxd_nc_definition)

        return results

    def verify_paths(self):
        return all(self._verify_paths().values())
