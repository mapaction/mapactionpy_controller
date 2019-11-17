import os
from unittest import TestCase
import fixtures
from mapactionpy_controller.product_bundle_definition import MapRecipe
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.data_search import DataSearch
from mapactionpy_controller.event import Event
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

        self.recipe_descriptor_path = os.path.join(self.parent_dir, 'example', 'product_bundle_example.json')
        self.recipe = MapRecipe(self.recipe_descriptor_path)

        self.cmf_descriptor_path = os.path.join(self.parent_dir, 'example', 'cmf_description.json')
        # self.cmf = CrashMoveFolder(self.cmf_descriptor_path, verify_on_creation=False)
        self.event_descriptor_path = os.path.join(self.parent_dir, 'example', 'event_description.json')
        self.event = Event(self.event_descriptor_path)

    def test_equality_of_map_recipes(self):
        test_recipe1 = MapRecipe(None, fixtures.recipe_with_positive_iso3_code)
        test_recipe2 = MapRecipe(None, fixtures.recipe_with_positive_iso3_code)

        self.assertEqual(test_recipe1, test_recipe2)
        test_recipe1.title = "something different"
        self.assertNotEqual(test_recipe1, test_recipe2)

        test_recipe3 = MapRecipe(None, fixtures.recipe_with_positive_iso3_code)
        self.assertEqual(test_recipe2, test_recipe3)
        test_recipe3.layers.pop()
        self.assertNotEqual(test_recipe2, test_recipe3)

    def test_serialise_and_deserialise_map_recipe(self):
        recipes_fixtures = [
            fixtures.recipe_with_positive_iso3_code,
            fixtures.recipe_result_one_dataset_per_layer,
            fixtures.recipe_without_positive_iso3_code
        ]

        for fixture_str in recipes_fixtures:
            test_recipe = MapRecipe(None, str_def=fixture_str)

            self.assertEqual(test_recipe, jsonpickle.decode(jsonpickle.encode(test_recipe)))
            self.assertEqual(test_recipe, MapRecipe(None, str_def=jsonpickle.encode(test_recipe, unpicklable=False)))
            self.assertEqual(test_recipe, MapRecipe(None, str_def=jsonpickle.encode(test_recipe)))
            self.assertNotEqual(test_recipe, MapRecipe(None, str_def=fixtures.recipe_with_negative_iso3_code))

    def test_substitute_iso3_in_regex(self):
        ds = DataSearch(self.event)

        reference_recipe = MapRecipe(
            None, str_def=fixtures.recipe_with_positive_iso3_code)
        pos_recipe = MapRecipe(
            None, str_def=fixtures.recipe_without_positive_iso3_code)
        updated_pos_recipe = ds.update_search_with_event_details(pos_recipe)
        self.assertEqual(updated_pos_recipe, reference_recipe)

        reference_recipe = MapRecipe(
            None, str_def=fixtures.recipe_with_negative_iso3_code)
        neg_recipe = MapRecipe(
            None, str_def=fixtures.recipe_without_negative_iso3_code)
        updated_neg_recipe = ds.update_search_with_event_details(neg_recipe)
        self.assertEqual(updated_neg_recipe, reference_recipe)

    @mock.patch('mapactionpy_controller.data_search.os.path')
    @mock.patch('mapactionpy_controller.data_search.os')
    def test_search_for_shapefiles(self, mock_os, mock_path):
        ds = DataSearch(self.event)

        # case where there is exactly one dataset per query
        mock_os.walk.return_value = fixtures.walk_single_admn_file_search_search
        mock_path.join.return_value = \
            r'D:/MapAction/2019MOZ01/GIS/2_Active_Data/202_admn/moz_admn_ad0_py_s0_unknown_pp.shp'
        mock_path.normpath.return_value = \
            r'D:/MapAction/2019MOZ01/GIS/2_Active_Data/202_admn/moz_admn_ad0_py_s0_unknown_pp.shp'
        mock_path.splitext.return_value = (r'moz_admn_ad0_py_s0_unknown_pp', r'.shp')
        reference_recipe = MapRecipe(
            None, str_def=fixtures.recipe_result_one_dataset_per_layer)
        test_recipe = MapRecipe(None, str_def=fixtures.recipe_with_positive_iso3_code)
        self.assertNotEqual(test_recipe, reference_recipe)
        updated_test_recipe = ds.update_recipe_with_datasources(test_recipe)

        self.assertEqual(updated_test_recipe, reference_recipe)

    def test_cmf_path_validation(self):

        cmf_partial_fail = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_cmf_description_one_file_and_one_dir_not_valid.json')

        # test validation on creation (for failing case) using default parameters
        self.assertRaises(ValueError, CrashMoveFolder, self.cmf_descriptor_path)
        # force validation on creation, for a json file we know would otherwise fail:
        self.assertRaises(ValueError, CrashMoveFolder, self.cmf_descriptor_path, verify_on_creation=True)
        # test validation is correctly disabled on creation, for a json file we know would otherwise fail:
        test_cmf = CrashMoveFolder(self.cmf_descriptor_path, verify_on_creation=False)
        self.assertIsInstance(test_cmf, CrashMoveFolder)

        # check message included in the ValueError:
        with self.assertRaises(ValueError) as cm:
            test_cmf = CrashMoveFolder(cmf_partial_fail, verify_on_creation=True)

        if six.PY2:
            self.assertRegexpMatches(str(cm.exception), "mxd_templates")
            self.assertNotRegexpMatches(str(cm.exception), "original_data")
        else:
            self.assertRegex(str(cm.exception), "mxd_templates")
            self.assertNotRegex(str(cm.exception), "original_data")

        # create a valid CMF object and then test paths, after creation
        test_cmf_path = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        test_cmf = CrashMoveFolder(test_cmf_path)
        self.assertTrue(test_cmf.verify_paths())
        test_cmf_path = os.path.join(self.parent_dir, 'example', 'cmf_description_reletive_paths_test.json')
        test_cmf = CrashMoveFolder(test_cmf_path)
        self.assertTrue(test_cmf.verify_paths())
        test_cmf.active_data = os.path.join(self.parent_dir, 'DOES-NOT-EXIST')
        self.assertFalse(test_cmf.verify_paths())
