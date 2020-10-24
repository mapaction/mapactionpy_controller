import json
import os
from unittest import TestCase
import fixtures
from jsonschema import ValidationError
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.event import Event
from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.map_recipe import MapRecipe
import jsonpickle
import six
# works differently for python 2.7 and python 3.x
try:
    from unittest import mock
except ImportError:
    import mock


class TestMAController(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.cmf_descriptor_path = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        self.cmf = CrashMoveFolder(self.cmf_descriptor_path, verify_on_creation=False)
        self.event_descriptor_path = os.path.join(self.parent_dir, 'example', 'event_description.json')
        self.event = Event(self.event_descriptor_path)
        # self.cmf = CrashMoveFolder(self.cmf_descriptor_path)
        self.lyr_props = LayerProperties(self.cmf, '', verify_on_creation=False)

        self.recipe_descriptor_path = os.path.join(self.parent_dir, 'example', 'example_single_map_recipe.json')
        with open(self.recipe_descriptor_path) as json_file:
            self.recipe_def = json.load(json_file)

        self.recipe = MapRecipe(self.recipe_def, self.lyr_props)

    def test_equality_of_map_recipes(self):
        recipe_def = json.loads(fixtures.recipe_with_positive_iso3_code)
        test_recipe1 = MapRecipe(recipe_def, self.lyr_props)
        test_recipe2 = MapRecipe(recipe_def, self.lyr_props)

        self.assertEqual(test_recipe1, test_recipe2)
        test_recipe1.summary = "something different"
        self.assertNotEqual(test_recipe1, test_recipe2)

        test_recipe3 = MapRecipe(recipe_def, self.lyr_props)
        self.assertEqual(test_recipe2, test_recipe3)
        # Remove an arbitary layer from each Map Frame
        for m_frames in test_recipe3.map_frames:
            m_frames.layers.pop()
        self.assertNotEqual(test_recipe2, test_recipe3)

    def test_serialise_and_deserialise_map_recipe(self):
        recipes_fixtures = [
            fixtures.recipe_with_positive_iso3_code,
            fixtures.recipe_result_one_dataset_per_layer_windows,
            fixtures.recipe_without_positive_iso3_code
        ]

        with mock.patch('mapactionpy_controller.map_recipe.path.exists') as mock_path:
            mock_path.return_value = True

            for fixture_str in recipes_fixtures:
                test_recipe = MapRecipe(fixture_str, self.lyr_props)

                self.assertEqual(
                    test_recipe,
                    jsonpickle.decode(jsonpickle.encode(test_recipe))
                )
                self.assertEqual(
                    test_recipe,
                    MapRecipe(jsonpickle.encode(test_recipe, unpicklable=False), self.lyr_props)
                )
                self.assertNotEqual(
                    test_recipe,
                    MapRecipe(fixtures.recipe_with_negative_iso3_code, self.lyr_props)
                )

    def test_cmf_schema_validation(self):

        test_files = ('fixture_cmf_description_extra_field.json',
                      'fixture_cmf_description_missing_field.json')

        for test_f in test_files:
            cmf_partial_fail = os.path.join(self.parent_dir, 'tests', 'testfiles', test_f)
            self.assertRaises(ValidationError, CrashMoveFolder, cmf_partial_fail)

    def test_cmf_path_validation(self):

        cmf_partial_fail = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_cmf_description_one_file_and_one_dir_not_valid.json')

        # test validation on creation (for failing case) using default parameters
        self.assertRaises(ValueError, CrashMoveFolder, cmf_partial_fail)
        # force validation on creation, for a json file we know would otherwise fail:
        self.assertRaises(ValueError, CrashMoveFolder, cmf_partial_fail, verify_on_creation=True)
        # test validation is correctly disabled on creation, for a json file we know would otherwise fail:
        test_cmf = CrashMoveFolder(cmf_partial_fail, verify_on_creation=False)
        self.assertIsInstance(test_cmf, CrashMoveFolder)

        # check message included in the ValueError:
        with self.assertRaises(ValueError) as cm:
            test_cmf = CrashMoveFolder(cmf_partial_fail, verify_on_creation=True)

        if six.PY2:
            self.assertRegexpMatches(str(cm.exception), "map_templates")
            self.assertNotRegexpMatches(str(cm.exception), "original_data")
        else:
            self.assertRegex(str(cm.exception), "map_templates")
            self.assertNotRegex(str(cm.exception), "original_data")

        # create a valid CMF object and then test paths, after creation
        test_cmf_path = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        test_cmf = CrashMoveFolder(test_cmf_path)
        self.assertTrue(test_cmf.verify_paths())
        test_cmf_path = os.path.join(self.parent_dir, 'example', 'cmf_description_relative_paths_test.json')
        test_cmf = CrashMoveFolder(test_cmf_path)
        self.assertTrue(test_cmf.verify_paths())
        test_cmf.active_data = os.path.join(self.parent_dir, 'DOES-NOT-EXIST')
        self.assertFalse(test_cmf.verify_paths())
