import fixtures
import os
import six
from unittest import TestCase
import json

from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.map_cookbook import MapCookbook
from mapactionpy_controller.map_recipe import MapRecipe,  RecipeFrame
from mapactionpy_controller.recipe_layer import RecipeLayer


class TestMapCookBook(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.path_to_valid_cmf_des = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        self.path_to_invalid_cmf_des = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_cmf_description_one_file_and_one_dir_not_valid.json')

        self.cmf = CrashMoveFolder(self.path_to_valid_cmf_des, verify_on_creation=False)
        self.lyr_props = LayerProperties(self.cmf, '', verify_on_creation=False)

    def test_different_cmf_args(self):

        # 1) test with valid CMF and LayerProperties objects
        test_cmf = CrashMoveFolder(self.path_to_valid_cmf_des)
        test_lp = LayerProperties(test_cmf, "test", verify_on_creation=False)
        test_mcb = MapCookbook(test_cmf, test_lp, verify_on_creation=False)
        self.assertIsInstance(test_mcb, MapCookbook)

        # 2) test with invalid cmf object (eg and CrashMoveFolder object
        #    where verify_paths() returns False)
        test_cmf = CrashMoveFolder(self.path_to_invalid_cmf_des, verify_on_creation=False)
        self.assertRaises(ValueError, MapCookbook, test_cmf, test_lp)

    def test_layer_props_and_cmf_mismatch(self):

        # create and test_cmf and test_lp which refer different layer_prop.json files
        cmf1 = CrashMoveFolder(self.path_to_valid_cmf_des)
        test_lp = LayerProperties(cmf1, "test", verify_on_creation=False)
        # now point the test_cmf to a different layer_props.json
        cmf2 = CrashMoveFolder(self.path_to_valid_cmf_des)
        cmf2.layer_properties = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_layer_properties_four_layers.json'
        )

        # check that a ValueError is raised when `verify_on_creation=True`
        with self.assertRaises(ValueError) as ve:
            MapCookbook(cmf2, test_lp, verify_on_creation=True)

        if six.PY2:
            self.assertRegexpMatches(str(ve.exception), "strange results")
        else:
            self.assertRegex(str(ve.exception), "strange results")

        # check that a ValueError is not raised when `verify_on_creation=False`
        test_mcb = MapCookbook(cmf2, test_lp, verify_on_creation=False)
        self.assertIsInstance(test_mcb, MapCookbook)

    def test_layer_props_and_cookbook_mismatch(self):
        cmf = CrashMoveFolder(self.path_to_valid_cmf_des)
        cmf.layer_properties = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_layer_properties_four_layers.json'
        )
        cmf.map_definitions = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_cookbook_1map_4layers.json'
        )
        test_lp = LayerProperties(cmf, "test", verify_on_creation=False)

        # 1) map_cb and lp match
        test_mcb = MapCookbook(cmf, test_lp, verify_on_creation=True)
        self.assertIsInstance(test_mcb, MapCookbook)

        # 2) layer in map_cb but not in lp
        # 3) layer in lp but not in map_cb
        # 4) unmatched layers in both lp and map_cb
        testcases = (
            ('fixture_cookbook_1map_5layers.json', ("mainmap-tran-rds-ln-s0-allmaps")),
            ('fixture_cookbook_1map_3layers.json', ("locationmap_stle_stl_pt_s0_locationmaps")),
            ('fixture_cookbook_1map_mismatch_layers.json',
                ("mainmap-tran-rds-ln-s0-allmaps", "locationmap_stle_stl_pt_s0_locationmaps")
             ),
        )

        for cb_file, strings_in_ex_msg in testcases:
            cmf.map_definitions = os.path.join(self.parent_dir, 'tests', 'testfiles', cb_file)

            with self.assertRaises(ValueError) as ve:
                MapCookbook(cmf, test_lp, verify_on_creation=True)

            if six.PY2:
                self.assertRegexpMatches(str(ve.exception), "One or more layer names occur in only one of these files")
                for s in strings_in_ex_msg:
                    self.assertRegexpMatches(str(ve.exception), s)
            else:
                self.assertRegex(str(ve.exception), "One or more layer names occur in only one of these files")
                for s in strings_in_ex_msg:
                    self.assertRegex(str(ve.exception), s)

    def test_recipe_atlas_constructor(self):
        cmf = CrashMoveFolder(
            os.path.join(self.parent_dir, 'example', 'cmf_description_relative_paths_test.json'))
        cmf.layer_properties = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'cookbooks', 'fixture_layer_properties_for_atlas.json'
        )

        # 1) atlas matches other sections 'fixture_cookbook_good_with_atlas.json'
        cmf.map_definitions = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'cookbooks', 'fixture_cookbook_good_with_atlas.json'
        )
        test_lp = LayerProperties(cmf, ".lyr", verify_on_creation=False)
        MapCookbook(cmf, test_lp, verify_on_creation=True)
        self.assertTrue(True)

        # 2) mismatch map_frame name 'fixture_cookbook_atlas_mismatch_map_frame.json'
        # 3) mismatch layer name (but present in other map frame) 'fixture_cookbook_atlas_mismatch_layer1.json'
        # 4) mismatch layer name, not present elsewhere in the recipe. 'fixture_cookbook_atlas_mismatch_layer2.json'
        # 5) mismatch column_names
        test_cb_names = (
            'fixture_cookbook_atlas_mismatch_map_frame.json',
            'fixture_cookbook_atlas_mismatch_layer1.json',
            'fixture_cookbook_atlas_mismatch_layer2.json',
            'fixture_cookbook_atlas_mismatch_column_name.json'
        )

        for test_cb in test_cb_names:
            cmf.map_definitions = os.path.join(
                self.parent_dir, 'tests', 'testfiles', 'cookbooks', test_cb
            )
            test_lp = LayerProperties(cmf, ".lyr", verify_on_creation=False)
            with self.assertRaises(ValueError):
                MapCookbook(cmf, test_lp, verify_on_creation=True)

    def test_load_recipe_with_layer_props_inc(self):
        # Test that a MapRecipe read form json with only a layername, combined with the
        # relevant LayerProperties is equal to a MapRecipe with all of the layerdetails embeded.

        # layerpros with
        cmf = CrashMoveFolder(
            os.path.join(self.parent_dir, 'example', 'cmf_description_relative_paths_test.json'))
        cmf.layer_properties = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'cookbooks', 'fixture_layer_properties_for_atlas.json'
        )
        test_lp = LayerProperties(cmf, ".lyr", verify_on_creation=False)

        # recipe with layer name only
        recipe1 = MapRecipe(fixtures.recipe_with_layer_name_only, test_lp)
        # combined recipe with layer props
        recipe2 = MapRecipe(fixtures.recipe_with_layer_details_embedded, test_lp)

        self.assertEqual(recipe1, recipe2)

        # 2) with non-matching layer props schema
        recipe3 = MapRecipe(fixtures.recipe_with_positive_iso3_code, test_lp)
        self.assertNotEqual(recipe1, recipe3)

    def test_check_for_dup_text_elements(self):
        cmf = CrashMoveFolder(
            os.path.join(self.parent_dir, 'example', 'cmf_description_relative_paths_test.json'))
        cmf.layer_properties = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'cookbooks', 'fixture_layer_properties_for_atlas.json'
        )

        # 1) Pass with "good" text elements in just one map_frame
        cmf.map_definitions = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'cookbooks', 'fixture_cookbook_good_with_atlas.json'
        )
        test_lp = LayerProperties(cmf, ".lyr", verify_on_creation=False)
        MapCookbook(cmf, test_lp, verify_on_creation=True)
        self.assertTrue(True)

        # 2) Fail with duplicate text elements in multiple map_frames
        cmf.map_definitions = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'cookbooks', 'fixture_cookbook_with_dup_text_elements.json'
        )
        test_lp = LayerProperties(cmf, ".lyr", verify_on_creation=False)
        with self.assertRaises(ValueError) as ve:
            MapCookbook(cmf, test_lp, verify_on_creation=True)

        fail_msg = 'More than one "map_frame" is linked to the Scale text element "scale"'
        if six.PY2:
            self.assertRegexpMatches(str(ve.exception), fail_msg)
        else:
            self.assertRegex(str(ve.exception), fail_msg)

    def test_check_for_dup_layers_and_mapframs(self):
        cmf = CrashMoveFolder(
            os.path.join(self.parent_dir, 'example', 'cmf_description_relative_paths_test.json'))
        cmf.layer_properties = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'cookbooks', 'fixture_layer_properties_for_atlas.json'
        )

        # Fail with multiple layer with the same name in the same mapframe.
        test_cookbooks = (
            ('fixture_cookbook_with_dup_layers.json', 'mainmap_tran_por_pt_s0_allmaps'),
            ('fixture_cookbook_with_dup_mapframes.json', 'Main map')
        )

        for cb_filename, fail_msg in test_cookbooks:
            cmf.map_definitions = os.path.join(
                self.parent_dir, 'tests', 'testfiles', 'cookbooks', cb_filename
            )
            test_lp = LayerProperties(cmf, ".lyr", verify_on_creation=False)
            with self.assertRaises(ValueError) as ve:
                MapCookbook(cmf, test_lp, verify_on_creation=True)

            if six.PY2:
                self.assertRegexpMatches(str(ve.exception), fail_msg)
            else:
                self.assertRegex(str(ve.exception), fail_msg)

    def test_atlas_get_layer(self):
        recipe_def = json.loads(fixtures.recipe_with_positive_iso3_code)
        test_recipe = MapRecipe(recipe_def, self.lyr_props)
        atlas = test_recipe.get_frame('Main map')

        self.assertTrue(atlas.contains_layer('mainmap_stle_stl_pt_s0_allmaps'))
        self.assertFalse(atlas.contains_layer('not-existant'))

        lyr = atlas.get_layer('mainmap_stle_stl_pt_s0_allmaps')
        self.assertIsInstance(lyr, RecipeLayer)

        self.assertRaises(ValueError, atlas.get_layer, 'not-existant')

    def test_get_atlas(self):
        recipe_def = json.loads(fixtures.recipe_with_positive_iso3_code)
        test_recipe = MapRecipe(recipe_def, self.lyr_props)

        self.assertTrue(test_recipe.contains_frame('Main map'))
        self.assertFalse(test_recipe.contains_frame('not-existant'))

        lyr = test_recipe.get_frame('Main map')
        self.assertIsInstance(lyr, RecipeFrame)

        self.assertRaises(ValueError, test_recipe.get_frame, 'not-existant')

    def test_map_recipe_backward_compat(self):
        # This is required in order to get hold of a recipe object. This is because the method being
        # tested is a member of the class.
        recipe_obj = MapRecipe(fixtures.recipe_with_layer_name_only, self.lyr_props)

        test_cases = [
            (fixtures.recipe_schema_v2_0_with_layer_name_only, 0.2),
            (fixtures.recipe_with_layer_name_only, 0.3)
        ]

        for recipe_str, expected_result in test_cases:
            recipe_def = json.loads(recipe_str)
            self.assertEqual(recipe_obj._check_schemas_with_backward_compat(recipe_def), expected_result)

    def test_map_recipe_with_artbitary_principal_frame_name(self):
        # Test cases where the principal map frame is not called "Main map"
        # This should load without error
        MapRecipe(fixtures.recipe_with_non_standard_principal_map_frame_name, self.lyr_props)

        # This should raise a ValueError
        with self.assertRaises(ValueError):
            MapRecipe(fixtures.recipe_with_invalid_principal_map_frame_name, self.lyr_props)

    def test_filter_lyr_for_use_in_frame_extent(self):
        # Have included the digit at the start of the string, so that can be sorted easily.
        cmf = CrashMoveFolder(
            os.path.join(self.parent_dir, 'example', 'cmf_description_relative_paths_test.json'))
        cmf.layer_properties = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'cookbooks', 'fixture_layer_properties_for_atlas.json'
        )
        test_lp = LayerProperties(cmf, ".lyr", verify_on_creation=False)

        # recipe with layer name only
        with open(os.path.join(self.parent_dir, 'tests', 'testfiles',
                               'fixture_cookbook_1map_5layers_1frame.json')) as rf:
            cookbook_def = json.load(rf)
        # get the first (only) recipe in the cookbook
        recipe_def = cookbook_def['recipes'].pop()

        generic_lyr_def = json.loads('''{
            "name": "the_name",
            "reg_exp": "^wrl_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(.+)shp$",
            "schema_definition": "admin1_reference.yml",
            "definition_query": "",
            "display": true,
            "add_to_legend": true,
            "label_classes": []
        }''')

        # Case 1
        # test white list
        test_white_list1 = [
            ('1a', True),
            ('1b', False),
            ('1c', None),
            ('1d', True),
            ('1e', False)
        ]
        expected_white_result1 = ['1a', '1d']

        test_white_list2 = [
            ('2a', True),
            ('2b', None),
            ('2c', None),
            ('2d', True),
            ('2e', None)
        ]
        expected_white_result2 = ['2a', '2d']

        # Case 2
        # Black List
        test_black_list = [
            ('3a', None),
            ('3b', False),
            ('3c', None),
            ('3d', None),
            ('3e', False)
        ]
        expected_black_result = ['3a', '3c', '3d']

        # Case 3
        # Default
        test_default_list = [
            ('4a', None),
            ('4b', None),
            ('4c', None),
            ('4d', None),
            ('4e', None)
        ]
        expected_default_result = ['4a', '4b', '4c', '4d', '4e']

        all_test_params = [
            (test_white_list1, expected_white_result1),
            (test_white_list2, expected_white_result2),
            (test_black_list, expected_black_result),
            (test_default_list, expected_default_result)
        ]

        for test_list, expected_result in all_test_params:
            test_recipe = MapRecipe(recipe_def, test_lp)

            # Build up a mock list of layer to test
            replacement_lyrs = []
            for test_lyr_details in test_list:
                new_lyr = RecipeLayer(generic_lyr_def, test_lp, verify_on_creation=False)
                new_lyr.name = test_lyr_details[0]
                new_lyr.use_for_frame_extent = test_lyr_details[1]
                # vaugely near Lebanon
                new_lyr.extent = (35, 33, 36, 34)
                new_lyr.crs = 'epsg:4326'

                replacement_lyrs.append(new_lyr)

            test_frame = test_recipe.map_frames.pop()
            test_frame.layers = replacement_lyrs
            result_lyrs = test_frame._filter_lyr_for_use_in_frame_extent()
            actual_result = [lyr.name for lyr in result_lyrs]
            self.assertEqual(actual_result, expected_result)

    def test_get_map_frame_extents(self):
        cmf = CrashMoveFolder(
            os.path.join(self.parent_dir, 'example', 'cmf_description_relative_paths_test.json'))
        cmf.layer_properties = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'cookbooks', 'fixture_layer_properties_for_atlas.json'
        )
        test_lp = LayerProperties(cmf, ".lyr", verify_on_creation=False)

        # recipe with layer name only
        with open(os.path.join(self.parent_dir, 'tests', 'testfiles',
                               'fixture_cookbook_1map_5layers_1frame.json')) as rf:
            cookbook_def = json.load(rf)
        # get the first (only) recipe in the cookbook
        recipe_def = cookbook_def['recipes'].pop()

        generic_lyr_def = json.loads('''{
            "name": "the_name",
            "reg_exp": "^wrl_admn_ad0_py_(.*?)_(.*?)_([phm][phm])(.+)shp$",
            "schema_definition": "admin1_reference.yml",
            "definition_query": "",
            "display": true,
            "add_to_legend": true,
            "label_classes": []
        }''')

        # Case 1
        # One or more layers does not have it's extent defined
        case1_list = [
            ('case1_lyrA', (35, 33, 36, 34), 'epsg:4326'),
            ('case1_lyrB', None, None)
        ]
        case1_result = (35, 33, 36, 34)

        # Case 2
        # Simple union with two lyrs of same crs
        case2_list = [
            ('case2_lyrA', (33, 51, 36, 58), 'epsg:4326'),
            ('case2_lyrB', (15, 52, 35, 55),  'epsg:4326')
        ]
        case2_result = (15, 51, 36, 58)

        # Case 3
        # Union with two lyrs of with different crs
        # 'epsg:4326'== WGS1984, 'epsg:3785' == Web Mercator
        case3_list = [
            ('case3_lyrA', (33, 51, 36, 58), 'epsg:4326'),
            ('case3_lyrB', (1669792.36, 6800125.45, 3896182.18, 7361866.11),  'epsg:3785')
        ]
        case3_result = (15, 51, 36, 58)

        # Case 4
        # One layer which stradles 180 degree meridian

        all_test_params = [
            (case1_list, case1_result),
            (case2_list, case2_result),
            (case3_list, case3_result)
        ]

        for test_list, expected_result in all_test_params:
            test_recipe = MapRecipe(recipe_def, test_lp)

            # Build up a mock list of layer to test
            replacement_lyrs = []
            for name, extent, crs in test_list:
                new_lyr = RecipeLayer(generic_lyr_def, test_lp, verify_on_creation=False)
                new_lyr.name = name
                new_lyr.use_for_frame_extent = bool(extent)
                # vaugely near Lebanon
                new_lyr.extent = extent
                new_lyr.crs = crs

                replacement_lyrs.append(new_lyr)

            print('test_get_map_frame_extents')
            print('expected_result = {}'.format(expected_result))
            test_frame = test_recipe.map_frames.pop()
            test_frame.crs = 'epsg:4326'
            test_frame.layers = replacement_lyrs
            test_frame.calc_extent(state=test_recipe)
            actual_result = test_frame.extent
            print('actual_result = {}'.format(actual_result))
            for actual, expected in zip(actual_result, expected_result):
                self.assertAlmostEqual(actual, expected)
