
from unittest import TestCase
import fixtures
import jsonschema
import os
import six
import yaml

from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.map_recipe import MapRecipe
import mapactionpy_controller.recipe_layer as recipe_layer

try:
    from unittest import mock
except ImportError:
    import mock


class TestRecipeLayer(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.path_to_valid_cmf_des = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        self.path_to_invalid_cmf_des = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_cmf_description_one_file_and_one_dir_not_valid.json')

        self.cmf = CrashMoveFolder(self.path_to_valid_cmf_des, verify_on_creation=False)
        self.lyr_props = LayerProperties(self.cmf, '', verify_on_creation=False)

    def test_layer_data_schema(self):

        null_schema = True

        passing_schema = yaml.safe_load(r"""
required:
    - name_en
properties:
    geometry_type:
        items:
            enum:
                - MultiPolygon
                - Polygon
        additionalItems: false
    crs:
        items:
            enum:
                - EPSG:2090
        additionalItems: false
""")

        # Note the missing `enum` blocks
        failing_schema = yaml.safe_load(r"""
required:
    - name_en
properties:
    geometry_type:
        items:
            - MultiPolygon
            - Polygon
        additionalItems: false
    crs:
        items:
            - EPSG:2090
        additionalItems: false
""")

        cmf = CrashMoveFolder(
            os.path.join(self.parent_dir, 'example', 'cmf_description_relative_paths_test.json'))
        cmf.layer_properties = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'cookbooks', 'fixture_layer_properties_for_atlas.json'
        )

        # Two cases where data schema is valid yaml
        for test_schema in [null_schema, passing_schema]:
            with mock.patch('mapactionpy_controller.data_schemas.yaml.safe_load') as mock_safe_load:
                mock_safe_load.return_value = test_schema
                test_lp = LayerProperties(cmf, ".lyr", verify_on_creation=False)

                MapRecipe(fixtures.recipe_with_positive_iso3_code, test_lp)
                self.assertTrue(True, 'validated jsonschema')

        # case where data schema file itself malformed somehow
        with mock.patch('mapactionpy_controller.data_schemas.yaml.safe_load') as mock_safe_load:
            mock_safe_load.return_value = failing_schema

            self.assertRaises(
                jsonschema.exceptions.SchemaError,
                MapRecipe,
                fixtures.recipe_with_positive_iso3_code,
                test_lp
            )

    def test_verify_layer_file_path(self):
        """
        Test the case that a recipe is re-stored with the layer_file_paths already populated, and
        whether or not that path is valid.
        """
        fail_msg = 'The expected layer file'
        with self.assertRaises(ValueError) as arcm:
            MapRecipe(fixtures.recipe_with_invalid_layer_file_path, self.lyr_props)

        if six.PY2:
            self.assertRegexpMatches(str(arcm.exception), fail_msg)
        else:
            self.assertRegex(str(arcm.exception), fail_msg)

    def test_check_lyr_is_in_recipe(self):
        """
        Check that an error is raised if any `step.funcs` attempt to act on a layer object that
        isn't part of the relevant recipe object.
        """
        # Two recipes without a common layer
        recipe_A = MapRecipe(fixtures.recipe_with_layer_name_only, self.lyr_props)
        recipe_B = MapRecipe(fixtures.recipe_with_positive_iso3_code, self.lyr_props)

        test_lyr = recipe_A.all_layers().pop()

        # This should pass without error
        test_lyr._check_lyr_is_in_recipe(recipe_A)

        # This should fail because test_lyr is not from recipe_B
        fail_msg = 'which is not part of the recipe'
        with self.assertRaises(ValueError) as arcm:
            test_lyr._check_lyr_is_in_recipe(recipe_B)

        if six.PY2:
            self.assertRegexpMatches(str(arcm.exception), fail_msg)
        else:
            self.assertRegex(str(arcm.exception), fail_msg)

    def test_calc_layer_file_checksum(self):
        test_recipe = MapRecipe(fixtures.recipe_with_layer_name_only, self.lyr_props)

        test_lyr = test_recipe.all_layers().pop()
        # This is an empty .lyr file
        test_lyr.layer_file_path = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'test_layer_rendering', 'four_files_exact_match',
            'locationmap_stle_stl_pt_s0_locationmaps.lyr')

        test_lyr._calc_layer_file_checksum()
        hash_of_empty_str = 'd41d8cd98f00b204e9800998ecf8427e'
        self.assertEqual(test_lyr.layer_file_checksum, hash_of_empty_str)

    def test_calc_data_source_checksum(self):
        test_recipe = MapRecipe(fixtures.recipe_with_layer_name_only, self.lyr_props)

        test_lyr = test_recipe.all_layers().pop()
        # Use a simple test shapefile
        test_lyr.data_source_path = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'test_shp_files',
            'lbn_admn_ad0_py_s1_pp_cdr.shp')

        actual_has_of_shp_file = test_lyr._calc_data_source_checksum()
        expected_hash_of_shp_file = '1acb212b47c8ccb3006ae9b4c5f1cfc0'
        self.assertEqual(actual_has_of_shp_file, expected_hash_of_shp_file)

    def test_get_schema_checker(self):
        test_recipe = MapRecipe(fixtures.recipe_with_layer_name_only, self.lyr_props)

        test_lyr = test_recipe.all_layers().pop()
        # Use a simple test shapefile
        test_lyr.data_source_path = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'test_shp_files',
            'lbn_admn_ad0_py_s1_pp_cdr.shp')

        passing_schema = yaml.safe_load(r"""
required:
    - admin0Name
    - admin0Na_1
    - admin0Pcod
    - admin0RefN
    - admin0AltN
properties:
    geometry_type:
        items:
            enum:
                - MultiPolygon
                - Polygon
        additionalItems: false
    additionalItems: true
""")

        incorrect_geom_schema = yaml.safe_load(r"""
required:
    - admin0Name
    - admin0Na_1
    - admin0Pcod
    - admin0RefN
    - admin0AltN
properties:
    geometry_type:
        items:
            enum:
                - Point
        additionalItems: false
    additionalItems: true
""")

        incorrect_columns_schema = yaml.safe_load(r"""
required:
    - county_name,
    - parish_name
properties:
    geometry_type:
        items:
            enum:
                - MultiPolygon
                - Polygon
        additionalItems: false
    additionalItems: true
""")

        incorrect_columns_and_geom_schema = yaml.safe_load(r"""
required:
    - county_name,
    - parish_name
properties:
    geometry_type:
        items:
            enum:
                - Point
        additionalItems: false
    additionalItems: true
""")

        # Case where data matches schema
        for test_schema in [passing_schema]:
            test_lyr.data_schema = test_schema
            result = test_lyr.check_data_against_schema(state=test_recipe)
            self.assertTrue(result)

        # Cases where data doesn't match schema
        for test_schema in [incorrect_geom_schema, incorrect_columns_schema, incorrect_columns_and_geom_schema]:
            test_lyr.data_schema = test_schema
            with self.assertRaises(ValueError) as arcm:
                test_lyr.check_data_against_schema(state=test_recipe)

            ve = arcm.exception
            self.assertIsInstance(ve.args[0], recipe_layer.FixSchemaErrorTask)

    def test_calc_extent(self):
        test_recipe = MapRecipe(fixtures.recipe_with_layer_name_only, self.lyr_props)

        test_lyr = test_recipe.all_layers().pop()
        # Use a simple test shapefile
        test_lyr.data_source_path = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'test_shp_files',
            'lbn_admn_ad0_py_s1_pp_cdr.shp')

        # Get the extents shapefile and update the test_lyr object
        test_lyr.calc_extent(state=test_recipe)

        expected_extent = [35.10348736558511, 33.054996785738204, 36.62291533501688, 34.69206915371]
        # expected_crs = (
        #     'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",'
        #     'SPHEROID["WGS_1984",6378137.0,298.257223563]],'
        #     'PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]')
        # expected_crs = {'init': 'epsg:4326'}
        expected_crs = 'epsg:4326'

        for actual, expected in zip(test_lyr.extent, expected_extent):
            self.assertEqual(actual, expected)

        self.assertEqual(test_lyr.crs, expected_crs)
