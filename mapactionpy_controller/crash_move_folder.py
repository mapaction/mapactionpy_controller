import json
import os
from event import Event

class CrashMoveFolder:
    def __init__(self, cmf_path):

        try:
            with open(cmf_path, 'r') as f:
                self.path = os.path.dirname(cmf_path)
                print(self.path)
                obj = json.loads(f.read())
                print(obj.keys())

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
                self.dnc_lookup_dir = os.path.join(
                    self.path, obj['dnc_lookup_dir'])
                self.default_jpeg_red_dpi = os.path.join(
                    self.path, obj['default_jpeg_red_dpi'])
                self.default_pdf_red_dpi = os.path.join(
                    self.path, obj['default_pdf_red_dpi'])
                self.default_emf_red_dpi = os.path.join(
                    self.path, obj['default_emf_red_dpi'])

        finally:
            f.close()


if __name__ == '__main__':
    cmf = CrashMoveFolder(
        r"D:\code\github\mapactionpy_controller\mapactionpy_controller\example\cmf_description.json")
    e = Event(cmf)
