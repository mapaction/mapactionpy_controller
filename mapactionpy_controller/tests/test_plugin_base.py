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
        self.dummy_runner = DummyRunner()

    def test_get_all_templates_by_regex(self):
        pass

    def test_get_templates(self):
        pass

    def test_get_template_by_aspect_ratio(self):
        template_aspect_ratios = [
            ('one',   1.1),
            ('two',   2),
            ('three', 2.32),
            ('four',  3.1415),
            ('five',  5),
            ('six',   10)
        ]

        test_aspect_ratios = [
            (5.0, 'five'),
            (4.9, 'five'),
            (5.1, 'five'),
            (100, 'six'),
            (0.0001, 'one'),
            (7.5, 'six'),
            (7.49998, 'five')
        ]

        for target_ar, expect_result in test_aspect_ratios:
            actual_result = self.dummy_runner._get_template_by_aspect_ratio(template_aspect_ratios, target_ar)
            print(target_ar, expect_result, actual_result)
            self.assertEqual(expect_result, actual_result)

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
