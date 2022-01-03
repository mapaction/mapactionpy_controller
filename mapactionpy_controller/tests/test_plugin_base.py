from mapactionpy_controller.plugin_base import BaseRunnerPlugin
from mapactionpy_controller.event import Event
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.map_recipe import MapRecipe
import fixtures
import os
from unittest import TestCase, skip
import six
import sys

# works differently for python 2.7 and python 3.x
if six.PY2:
    import mock  # noqa: F401
else:
    from unittest import mock  # noqa: F401


class DummyRunner(BaseRunnerPlugin):
    def __init__(self, hum_event):
        super(DummyRunner, self).__init__(hum_event)

    def get_aspect_ratios_of_templates(self, possible_templates, recipe):
        return [
            ('one', 1.0),
            ('two', 2.0)
        ]

    def export_maps(self, **kwargs):
        return kwargs['state']

    def build_project_files(self, **kwargs):
        return kwargs['state']

    def get_projectfile_extension(self):
        return '.dummy_project_file'

    def get_lyr_render_extension(self):
        return '.lyr'

    def create_output_map_project(self, **kwargs):
        return kwargs['state']


class TestPluginBase(TestCase):
    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.dir_to_valid_cmf_des = os.path.join(self.parent_dir, 'example')
        self.path_to_valid_cmf_des = os.path.join(self.dir_to_valid_cmf_des, 'cmf_description_flat_test.json')
        self.path_to_event_des = os.path.join(self.dir_to_valid_cmf_des, 'event_description.json')
        self.cmf = CrashMoveFolder(self.path_to_valid_cmf_des)
        self.lyr_props = LayerProperties(self.cmf, '', verify_on_creation=False)
        self.dummy_runner = DummyRunner(Event(self.path_to_event_des))

    def test_get_all_templates_by_regex(self):
        recipe = mock.Mock(name='mock_recipe')
        recipe.template = 'abcde'

        dummy_map_templates = '/xyz/'

        if sys.platform == 'win32':
            dummy_map_templates = 'C:\\xyz\\'

        self.dummy_runner.cmf.map_templates = dummy_map_templates

        available_templates = [
            'one-two-three.dummy_project_file',
            'one-two-three.txt',
            'abcde.dummy_project_file',
            'abcde.txt'
        ]

        expect_result = [
            '{}abcde.dummy_project_file'.format(dummy_map_templates)
        ]

        with mock.patch('mapactionpy_controller.plugin_base.os.listdir') as mock_listdir:
            with mock.patch('mapactionpy_controller.plugin_base.os.path.isfile') as mock_isfile:
                mock_listdir.return_value = available_templates
                mock_isfile.return_value = True

                actual_result = self.dummy_runner._get_all_templates_by_regex(recipe)

        self.assertEqual(actual_result, expect_result)

    def test_get_template_by_aspect_ratio(self):
        template_aspect_ratios = [
            ('one',   1.1),
            ('two',   2),
            ('three', 2.32),
            ('four',  3.1415),
            ('five',  5),
            ('six',   10)
        ]

        # half way between 5.0 and 10.0 ==> 10^(0.5*(log(10)+LOG(5)) = 7.071067812
        test_aspect_ratios = [
            (5.0, 'five'),
            (4.9, 'five'),
            (5.1, 'five'),
            (100, 'six'),
            (0.0001, 'one'),
            (7.0711, 'six'),
            (7.0710, 'five')
        ]

        for target_ar, expect_result in test_aspect_ratios:
            actual_result = self.dummy_runner._get_template_by_aspect_ratio(template_aspect_ratios, target_ar)
            # print('expect_result={}, actual_result={}'.format(expect_result, actual_result))
            self.assertEqual(expect_result, actual_result)

        template_aspect_ratios = [
            ('landscape_bottom', 1.975),
            ('landscape_side', 1.294117647),
            ('portrait', 0.816816817)
        ]

        # linear_aspect_ratios = [
        #     (1.623, 'landscape_side'),
        #     (1.036, 'portrait'),
        #     (1.038, 'portrait'),
        #     (1.031, 'portrait')
        # ]

        log_aspect_ratios = [
            (1.623, 'landscape_bottom'),
            (1.036, 'landscape_side'),
            (1.038, 'landscape_side'),
            (1.031, 'landscape_side')
        ]

        for target_ar, expect_result in log_aspect_ratios:
            actual_result = self.dummy_runner._get_template_by_aspect_ratio(template_aspect_ratios, target_ar)
            # print('expect_result={}, actual_result={}'.format(expect_result, actual_result))
            self.assertEqual(expect_result, actual_result)

    def test_get_templates(self):

        # Case 1
        # Pre-existing valid `map_project_path` value
        expect_result = MapRecipe(fixtures.recipe_test_for_search_for_shapefiles, self.lyr_props)
        test_recipe = MapRecipe(fixtures.recipe_test_for_search_for_shapefiles, self.lyr_props)
        expect_result.map_project_path = '/path/that/exists.mxd'
        test_recipe.map_project_path = '/path/that/exists.mxd'

        with mock.patch('mapactionpy_controller.plugin_base.os.path.exists') as mock_path_exists:
            mock_path_exists.return_value = True
            actual_result = self.dummy_runner.get_templates(state=test_recipe)

        self.assertEqual(actual_result, expect_result)

        # Case 2
        # Non-None `map_project_path` value which points of non-existing file
        test_recipe = MapRecipe(fixtures.recipe_test_for_search_for_shapefiles, self.lyr_props)
        test_recipe.map_project_path = '/path/that/does/not/exists.mxd'

        with mock.patch('mapactionpy_controller.plugin_base.os.path.exists') as mock_path_exists:
            mock_path_exists.return_value = False
            with self.assertRaises(ValueError):
                self.dummy_runner.get_templates(state=test_recipe)

        # Case 3 & 4
        # mf.extent exists and has a valid value
        # mf.entent is None
        test_extents = [
            ('one', (1, 1, 5, 5)),
            ('two', (1, 1, 9, 5)),
            ('one', None)
        ]

        for expected_result, extent in test_extents:
            print(expected_result, extent)
            test_recipe = MapRecipe(fixtures.recipe_test_for_search_for_shapefiles, self.lyr_props)
            test_recipe.map_frames[0].extent = extent
            # mf.extent = extent
            actual_recipe = self.dummy_runner.get_templates(state=test_recipe)
            self.assertEquals(expected_result, actual_recipe.template_path)

    @skip('Not ready yet')
    def test_get_next_map_version_number(self):
        self.fail()

    @skip('Not ready yet')
    def test_create_output_map_project(self):
        self.fail()

    @skip('Not ready yet')
    def test_export_maps(self):
        self.fail()

    def test_create_export_dir(self):
        test_recipe = MapRecipe(fixtures.recipe_test_for_search_for_shapefiles, self.lyr_props)
        test_recipe.map_project_path = '/path/that/does/not/exists.mxd'

        dummy_export_dir = '/xyz/'

        if sys.platform == 'win32':
            dummy_export_dir = 'C:\\xyz\\'

        test_cases = [
            ((dummy_export_dir, 'MA1234', 1), '{}MA1234{}v01'.format(dummy_export_dir, os.path.sep)),
            ((dummy_export_dir, 'MA1234', 22), '{}MA1234{}v22'.format(dummy_export_dir, os.path.sep)),
            ((dummy_export_dir, 'MA1234', 333), '{}MA1234{}v333'.format(dummy_export_dir, os.path.sep))
        ]

        with mock.patch('mapactionpy_controller.plugin_base.os.makedirs') as mock_makedirs:
            mock_makedirs.return_value = None
            for input_params, expect_result in test_cases:
                self.dummy_runner.cmf.export_dir, test_recipe.mapnumber, test_recipe.version_num = input_params
                actual_result = self.dummy_runner._create_export_dir(test_recipe)

                self.assertEqual(actual_result.export_path, expect_result)

    def test_check_paths_for_zip_contents(self):
        test_recipe = MapRecipe(fixtures.recipe_test_for_search_for_shapefiles, self.lyr_props)

        # Case 1: No files have been specified
        test_recipe.zip_file_contents = []
        fail_msg = 'No paths are specified'

        with self.assertRaises(ValueError) as ve:
            self.dummy_runner._check_paths_for_zip_contents(test_recipe)

        if six.PY2:
            self.assertRegexpMatches(str(ve.exception), fail_msg)
        else:
            self.assertRegex(str(ve.exception), fail_msg)

        # Case 2: Two valid and two invalid paths. The invalid paths are correctly idenified in the error message.
        # Mocking this across different platforms is too complex. Therefore use two arbitary files that exist within
        # the repo and two fictional paths
        invalid_path1 = '/xyz/abc'
        invalid_path2 = '/abc/xyz'
        test_recipe.zip_file_contents = [
            self.path_to_valid_cmf_des,
            invalid_path1,
            self.path_to_event_des,
            invalid_path2
        ]

        with self.assertRaises(ValueError) as ve:
            self.dummy_runner._check_paths_for_zip_contents(test_recipe)

        if six.PY2:
            self.assertRegexpMatches(str(ve.exception), invalid_path1)
            self.assertRegexpMatches(str(ve.exception), invalid_path2)
            self.assertNotRegexpMatches(str(ve.exception), self.path_to_valid_cmf_des)
            self.assertNotRegexpMatches(str(ve.exception), self.path_to_event_des)
        else:
            self.assertRegex(str(ve.exception), invalid_path1)
            self.assertRegex(str(ve.exception), invalid_path2)
            self.assertNotRegex(str(ve.exception), 'cmf_description_flat_test.json')
            self.assertNotRegex(str(ve.exception), 'event_description.json')

        # Case 3: two valid paths, hence no exception raised
        # Hence just call the method and pass is no exception is handled
        test_recipe.zip_file_contents = [
            self.path_to_valid_cmf_des,
            self.path_to_event_des
        ]
        self.dummy_runner._check_paths_for_zip_contents(test_recipe)
        self.assertTrue(True)

    @skip('Not ready yet')
    def test_zip_exported_files(self):
        self.fail()
