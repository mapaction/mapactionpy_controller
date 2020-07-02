from mapactionpy_controller.plugin_base import BaseRunnerPlugin
from unittest import TestCase


class DummyRunner(BaseRunnerPlugin):
    def __init__(self, **kwargs):
        pass

    def get_templates(self, **kwargs):
        return kwargs['state']

    def export_maps(self, **kwargs):
        return kwargs['state']

    def build_project_files(self, **kwargs):
        return kwargs['state']

    def get_projectfile_extension(self):
        return '.dummy_project_file'

    def get_lyr_render_extension(self):
        return '.dummy_lyr_file'

    def create_ouput_map_project(self, **kwargs):
        return kwargs['state']


class TestPluginBase(TestCase):
    def setUp(self):
        pass

    def test_get_all_templates_by_regex(self):
        pass

    def test_get_templates(self):
        pass

    def test_get_next_map_version_number(self):
        pass

    def test_create_ouput_map_project(self):
        pass

    def test_export_maps(self):
        pass

    def test_create_export_dir(self):
        pass

    def test_zip_exported_files(self):
        pass
