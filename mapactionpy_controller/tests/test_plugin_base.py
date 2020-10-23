from mapactionpy_controller.plugin_base import BaseRunnerPlugin
from mapactionpy_controller.event import Event
import os
from unittest import TestCase
import six

# works differently for python 2.7 and python 3.x
if six.PY2:
    import mock  # noqa: F401
else:
    from unittest import mock  # noqa: F401


class DummyRunner(BaseRunnerPlugin):
    def __init__(self, hum_event):
        super(DummyRunner, self).__init__(hum_event)

    def get_templates(self, **kwargs):
        return kwargs['state']

    def export_maps(self, **kwargs):
        return kwargs['state']

    def build_project_files(self, **kwargs):
        return kwargs['state']

    def get_projectfile_extension(self):
        return '.dummy_project_file'

    def get_lyr_render_extension(self):
        return '.lyr'

    def create_ouput_map_project(self, **kwargs):
        return kwargs['state']


class TestPluginBase(TestCase):
    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.dir_to_valid_cmf_des = os.path.join(self.parent_dir, 'example')
        self.path_to_valid_cmf_des = os.path.join(self.dir_to_valid_cmf_des, 'cmf_description_flat_test.json')
        self.path_to_event_des = os.path.join(self.dir_to_valid_cmf_des, 'event_description.json')
        self.dummy_runner = DummyRunner(Event(self.path_to_event_des))

    def test_get_all_templates_by_regex(self):
        recipe = mock.Mock(name='mock_recipe')
        recipe.template = 'abcde'

        self.dummy_runner.cmf.map_templates = '/xyz/'

        available_templates = [
            'one-two-three.dummy_project_file',
            'one-two-three.txt',
            'abcde.dummy_project_file',
            'abcde.txt'
        ]

        expect_result = [
            '/xyz/abcde.dummy_project_file'
        ]

        with mock.patch('mapactionpy_controller.plugin_base.os.listdir') as mock_listdir:
            with mock.patch('mapactionpy_controller.plugin_base.os.path.isfile') as mock_isfile:
                mock_listdir.return_value = available_templates
                mock_isfile.return_value = True

                actual_result = self.dummy_runner._get_all_templates_by_regex(recipe)

        self.assertEqual(actual_result, expect_result)

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
