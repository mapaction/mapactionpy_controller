import os
import unittest
from unittest import TestCase
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
        # ds.update_search_with_event_details(recipe, event)

        pos_recipe = MapRecipe(
            None, str_def=fixtures.recipe_without_positive_iso3_code)
        updated_pos_recipe = ds.update_search_with_event_details(pos_recipe, self.event)
        test_str_positive = updated_pos_recipe.layers[0].search_definition
        self.assertEqual(test_str_positive, fixtures.fixture_regex_with_iso3_code)

        neg_recipe = MapRecipe(
            None, str_def=fixtures.recipe_without_negative_iso3_code)
        #test_str_negative = ds.update_search_with_event_details(neg_recipe, self.event)
        updated_neg_recipe = ds.update_search_with_event_details(
            neg_recipe, self.event)
        test_str_negative = updated_neg_recipe.layers[0].search_definition

        self.assertEqual(test_str_negative, fixtures.fixture_regex_with_negative_iso3_code)


    @unittest.SkipTest
    def test_search_for_shapefiles(self):
        # case where there is exactly one dataset per query
        test_result_success = mapactionpy_controller.find_datasource(
            fixtures.fixture_datasource_intermediatory_query)

        self.assertEqual(test_result_success,
                         fixtures.fixture_datasource_result_one_dataset_per_layer)

        # case where there is a missing dataset for one or more query
        test_result_success = mapactionpy_controller.find_datasource(
            fixtures.fixture_datasource_intermediatory_query)

        self.assertEqual(test_result_success,
                         fixtures.fixture_datasource_result_missing_layer)


if __name__ == '__main__':
    unittest.main()


r""" 
'''
if __name__ == '__main__':
    recipe=MapRecipe(r"D:\code\github\mapactionpy_controller\mapactionpy_controller\example\product_bundle_example.json")
    cmf=CrashMoveFolder(
        r"D:\code\github\mapactionpy_controller\mapactionpy_controller\example\cmf_description.json")
    event = Event(cmf)

    ds = DataSearch(cmf)
    ds.update_search_with_event_details(recipe, event)

    #for lyr in recipe.layers:
    #print('{l.map_frame}\t{l.layer_display_name}'.format(l=lyr))
'''
"""
