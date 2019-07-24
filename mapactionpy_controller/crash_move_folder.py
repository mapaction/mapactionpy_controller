import json
import os
# from jsonschema import validate


class CrashMoveFolder:
    def __init__(self, cmf_path):
        # cd = os.path.dirname(os.path.realpath(__file__))
        # schema_path = os.path.join(cd, 'schemas', 'cmf-v0.1.schema')
        # json_schema = open(schema_path, 'r').read()
        # print(json_schema)

        self.path = os.path.dirname(cmf_path)

        with open(cmf_path, 'r') as f:
            txt = f.read()
            # print(txt)
            # validate(txt, json_schema)
            obj = json.loads(txt)

            # Doubtless there is a more elegant way to do this.
            self.event_description_file = os.path.join(
                self.path, obj['event_description_file'])
            self.original_data = os.path.join(
                self.path, obj['original_data'])
            self.active_data = os.path.join(self.path, obj['active_data'])
            self.layer_redering = os.path.join(
                self.path, obj['layer_redering'])
            self.mxd_templates = os.path.join(
                self.path, obj['mxd_templates'])
            self.qgis_templates = os.path.join(
                self.path, obj['qgis_templates'])
            self.export_dir = os.path.join(self.path, obj['export_dir'])
            self.dnc_definition = os.path.join(
                self.path, obj['dnc_definition'])
            self.default_jpeg_red_dpi = obj['default_jpeg_red_dpi']
            self.default_pdf_red_dpi = obj['default_pdf_red_dpi']
            self.default_emf_red_dpi = obj['default_emf_red_dpi']
