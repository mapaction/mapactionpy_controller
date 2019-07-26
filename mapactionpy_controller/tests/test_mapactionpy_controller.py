import os
from unittest import TestCase
import fixtures
from mapactionpy_controller.product_bundle_definition import MapRecipe
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.data_search import DataSearch
import jsonpickle
# works differently for python 2.7 and python 3.x
try:
    from unittest import mock
except ImportError:
    import mock


class TestMAController(TestCase):

    def setUp(self):
        parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        recipe_descriptor_path = os.path.join(
            parent_dir, 'example', 'product_bundle_example.json')
        self.recipe = MapRecipe(recipe_descriptor_path)

        cmf_descriptor_path = os.path.join(
            parent_dir, 'example', 'cmf_description.json')
        self.cmf = CrashMoveFolder(cmf_descriptor_path)

    def test_serialise_and_deserialise_map_recipe(self):
        recipes_fixtures = [
            fixtures.recipe_with_positive_iso3_code,
            fixtures.recipe_result_one_dataset_per_layer,
            fixtures.recipe_without_positive_iso3_code
        ]

        for fixture_str in recipes_fixtures:
            test_recipe = MapRecipe(None, str_def=fixture_str)

            self.assertEqual(test_recipe,
                             jsonpickle.decode(jsonpickle.encode(test_recipe)))
            self.assertEqual(test_recipe,
                             MapRecipe(None, str_def=jsonpickle.encode(test_recipe, unpicklable=False)))
            self.assertEqual(test_recipe,
                             MapRecipe(None, str_def=jsonpickle.encode(test_recipe)))
            self.assertNotEqual(test_recipe,
                                MapRecipe(None, str_def=fixtures.recipe_with_negative_iso3_code))

    def test_substitute_iso3_in_regex(self):
        ds = DataSearch(self.cmf)

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
        ds = DataSearch(self.cmf)

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
