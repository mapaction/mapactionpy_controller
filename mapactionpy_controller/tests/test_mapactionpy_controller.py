import jsonpickle
import os
import unittest
from unittest import TestCase
from unittest import mock
import fixtures
from mapactionpy_controller.product_bundle_definition import MapRecipe, LayerSpec
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.data_search import DataSearch
from mapactionpy_controller.event import Event


class TestMAController(TestCase):

    def setUp(self):
        parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        recipe_descriptor_path = os.path.join(
            parent_dir, 'example', 'product_bundle_example.json')
        self.recipe = MapRecipe(recipe_descriptor_path)

        cmf_descriptor_path = os.path.join(
            parent_dir, 'example', 'cmf_description.json')
        self.cmf = CrashMoveFolder(cmf_descriptor_path)
        self.event = Event(self.cmf)

    @unittest.SkipTest
    def test_alway_fail(self):
        self.assertTrue(False)

    @unittest.SkipTest
    def test_alway_pass(self):
        self.assertTrue(True)

    def test_substitute_iso3_in_regex(self):
        ds = DataSearch(self.cmf)

        reference_recipe = MapRecipe(
            None, str_def=fixtures.recipe_with_positive_iso3_code)
        pos_recipe = MapRecipe(
            None, str_def=fixtures.recipe_without_positive_iso3_code)
        updated_pos_recipe = ds.update_search_with_event_details(pos_recipe, self.event)
        self.assertEqual(updated_pos_recipe, reference_recipe)

        reference_recipe = MapRecipe(
            None, str_def=fixtures.recipe_with_negative_iso3_code)
        neg_recipe = MapRecipe(
            None, str_def=fixtures.recipe_without_negative_iso3_code)
        updated_neg_recipe = ds.update_search_with_event_details(
            neg_recipe, self.event)
        self.assertEqual(updated_neg_recipe, reference_recipe)

    @mock.patch('mapactionpy_controller.data_search.os.path')
    @mock.patch('mapactionpy_controller.data_search.os')
    def test_search_for_shapefiles(self, mock_os, mock_path):
        ds = DataSearch(self.cmf)

        # case where there is exactly one dataset per query
        mock_os.walk.return_value = fixtures.walk_single_admn_file_search_search
        mock_path.join.return_value = r'D:/MapAction/2019MOZ01/GIS/2_Active_Data/202_admn/moz_admn_ad0_py_s0_unknown_pp.shp'
        mock_path.normpath.return_value = r'D:/MapAction/2019MOZ01/GIS/2_Active_Data/202_admn/moz_admn_ad0_py_s0_unknown_pp.shp'
        reference_recipe = MapRecipe(
            None, str_def=fixtures.recipe_result_one_dataset_per_layer)
        test_recipe = MapRecipe(None, str_def=fixtures.recipe_with_positive_iso3_code)
        self.assertNotEqual(test_recipe, reference_recipe)
        updated_test_recipe = ds.update_recipe_with_datasources(test_recipe)
        
        self.assertEqual(updated_test_recipe, reference_recipe)


if __name__ == '__main__':
    unittest.main()
