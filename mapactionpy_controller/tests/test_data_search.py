import unittest
import mapactionpy_controller.data_search as data_search
from mapactionpy_controller.map_recipe import MapRecipe
from mapactionpy_controller.event import Event
from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
import fixtures
import os
import six
import platform


# works differently for python 2.7 and python 3.x
if six.PY2:
    import mock  # noqa: F401
    # from mock import mock_open, patch
else:
    from unittest import mock  # noqa: F401
    # from unittest.mock import mock_open, patch  # noqa: F401


class TestDataSearch(unittest.TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.cmf_descriptor_path = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        self.event_descriptor_path = os.path.join(self.parent_dir, 'example', 'event_description.json')
        self.recipe_file = os.path.join(self.parent_dir, 'example', 'example_single_map_recipe.json')
        self.non_existant_file = os.path.join(self.parent_dir, 'example', 'non-existant-file.json')
        self.cmf = CrashMoveFolder(self.cmf_descriptor_path, verify_on_creation=False)
        self.event = Event(self.event_descriptor_path)
        # self.cmf = CrashMoveFolder(self.cmf_descriptor_path)
        self.lyr_props = LayerProperties(self.cmf, '', verify_on_creation=False)
        # self.ds = data_search.DataSearch(cmf_descriptor_path)

    def test_substitute_fields_in_recipe_strings(self):
        recipe_updater = data_search.get_recipe_event_updater(self.event)

        # An example with an iso code within a positive regex lookup
        # (eg '^{e.affected_country_iso3}_stle.....')
        reference_recipe = MapRecipe(
            fixtures.recipe_with_positive_iso3_code, self.lyr_props)
        pos_recipe = MapRecipe(
            fixtures.recipe_without_positive_iso3_code, self.lyr_props)
        updated_pos_recipe = recipe_updater(state=pos_recipe)
        self.assertEqual(updated_pos_recipe, reference_recipe)

        # An example with an iso code within a negitive regex lookup
        # (eg '^(?!({e.affected_country_iso3}))_admn.....')
        reference_recipe = MapRecipe(
            fixtures.recipe_with_negative_iso3_code, self.lyr_props)
        neg_recipe = MapRecipe(
            fixtures.recipe_without_negative_iso3_code, self.lyr_props)
        recipe_updater = data_search.get_recipe_event_updater(self.event)
        updated_neg_recipe = recipe_updater(state=neg_recipe)

        self.assertEqual(updated_neg_recipe, reference_recipe)

        # Reverse of the first example to test a case where nothing needs updating. In this case the same json
        # definition is used for both recipes. There are not string replacement fields within the json definition.
        reference_recipe = MapRecipe(
            fixtures.recipe_with_positive_iso3_code, self.lyr_props)
        pos_recipe = MapRecipe(
            fixtures.recipe_with_positive_iso3_code, self.lyr_props)
        updated_pos_recipe = recipe_updater(state=pos_recipe)
        self.assertEqual(updated_pos_recipe, reference_recipe)

    def test_search_for_shapefiles(self):
        # ds = data_search.DataSearch(self.event)

        with mock.patch('mapactionpy_controller.data_search.glob.glob') as mock_glob:
            # We use two different mock values becuase we are matching absolute paths as strings
            # The underlying production code does not differencate between platforms.
            if platform.system() == 'Windows':
                mock_single_file_glob = fixtures.glob_single_stle_file_search_windows
                mock_multiple_file_glob = fixtures.glob_multiple_stle_file_search_windows
                mock_no_file_glob = fixtures.glob_no_stle_file_search_windows
                ref_recipe_str = fixtures.recipe_result_one_dataset_per_layer_windows
            else:
                mock_single_file_glob = fixtures.glob_single_stle_file_search_linux
                mock_multiple_file_glob = fixtures.glob_multiple_stle_file_search_linux
                mock_no_file_glob = fixtures.glob_no_stle_file_search_linux
                ref_recipe_str = fixtures.recipe_result_one_dataset_per_layer_linux

            reference_recipe = MapRecipe(ref_recipe_str, self.lyr_props)

            # Case A
            # where there is exactly one dataset per query
            test_recipe = MapRecipe(fixtures.recipe_test_for_search_for_shapefiles, self.lyr_props)
            mock_glob.return_value = mock_single_file_glob
            self.assertNotEqual(test_recipe, reference_recipe)

            # get the first layer from the test_recipe
            test_lyr = test_recipe.all_layers().pop()
            data_finder = data_search.get_lyr_data_finder(self.cmf, test_lyr)
            updated_test_recipe = data_finder(state=test_recipe)

            self.assertEqual(updated_test_recipe, test_recipe)
            self.assertTrue(updated_test_recipe == test_recipe)
            self.assertEqual(updated_test_recipe, reference_recipe)

            # Case B
            # where there is multiple matching datasets
            test_recipe = MapRecipe(fixtures.recipe_test_for_search_for_shapefiles, self.lyr_props)
            mock_glob.return_value = mock_multiple_file_glob
            self.assertNotEqual(test_recipe, reference_recipe)

            # get the first layer from the test_recipe
            test_lyr = test_recipe.all_layers().pop()
            data_finder = data_search.get_lyr_data_finder(self.cmf, test_lyr)
            with self.assertRaises(ValueError) as arcm:
                updated_test_recipe = data_finder(state=test_recipe)

            ve = arcm.exception
            print('ve.args[0] is instance of: {}'.format(type(ve.args[0])))
            self.assertIsInstance(ve.args[0], data_search.FixMultipleMatchingFilesTask)

            # Case C
            # where there are no matching datasets
            test_recipe = MapRecipe(fixtures.recipe_test_for_search_for_shapefiles, self.lyr_props)
            mock_glob.return_value = mock_no_file_glob
            self.assertNotEqual(test_recipe, reference_recipe)

            # get the first layer from the test_recipe
            test_lyr = test_recipe.all_layers().pop()
            data_finder = data_search.get_lyr_data_finder(self.cmf, test_lyr)
            with self.assertRaises(ValueError) as arcm:
                updated_test_recipe = data_finder(state=test_recipe)

            ve = arcm.exception
            print('ve.args[0] is instance of: {}'.format(type(ve.args[0])))
            self.assertIsInstance(ve.args[0], data_search.FixMissingGISDataTask)

    def test_check_layer(self):

        recipe = MapRecipe(fixtures.recipe_with_layer_details_embedded, self.lyr_props)
        lyr = recipe.all_layers().pop()

        # This will pass silently if the lyr is of the right type
        self.assertIsNone(data_search._check_layer(lyr))

        # This case should raise a ValueError
        with self.assertRaises(ValueError):
            data_search._check_layer('string-to-represent-a-layer')
