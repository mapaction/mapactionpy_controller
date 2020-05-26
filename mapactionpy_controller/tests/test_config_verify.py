from jsonschema import ValidationError
import os
from unittest import TestCase
import mapactionpy_controller.config_verify as config_verify


class TestConfigVerify(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.all_matching_cmf_path = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_cmf_pointing_to_matching_lp_mcb_and_lyrs.json')
        self.mismatching_cmf_path = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_cmf_pointing_to_mismatching_lp_mcb_and_lyrs.json')
        self.path_to_valid_cmf_des = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        self.path_to_invalid_cmf_des = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_cmf_description_one_file_and_one_dir_not_valid.json')

    def test_check_cmf_description(self):
        # A valid cmf description
        cv = config_verify.ConfigVerifier(self.path_to_valid_cmf_des, ['.lyr'])
        try:
            cv.check_cmf_description()
            self.assertTrue(True)
        except ValueError as ve:
            self.fail(ve)

        # An Invalid cmf description
        cv = config_verify.ConfigVerifier(self.path_to_invalid_cmf_des, ['.lyr'])
        with self.assertRaises(ValueError):
            cv.check_cmf_description()

    def test_check_lyr_props_vs_rendering_dir(self):
        cv = config_verify.ConfigVerifier(self.mismatching_cmf_path, ['.lyr'])

        with self.assertRaises(ValueError):
            cv.check_lyr_props_vs_rendering_dir()

        cv = config_verify.ConfigVerifier(self.all_matching_cmf_path, ['.lyr'])
        try:
            cv.check_lyr_props_vs_rendering_dir()
            self.assertTrue(True)
        except ValueError as ve:
            self.fail(ve)

    def test_check_lyr_props_vs_map_cookbook(self):
        cv = config_verify.ConfigVerifier(self.mismatching_cmf_path, ['.lyr'])

        with self.assertRaises(ValueError):
            cv.check_lyr_props_vs_map_cookbook()

        cv = config_verify.ConfigVerifier(self.all_matching_cmf_path, ['.lyr'])
        try:
            cv.check_lyr_props_vs_map_cookbook()
            self.assertTrue(True)
        except ValueError as ve:
            self.fail(ve)

    def test_check_config_file_schemas(self):
        schema_errors_cmf_path = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'config_schemas',
            'fixture_cmf_pointing_schema_errors.json'
        )

        cv = config_verify.ConfigVerifier(schema_errors_cmf_path, ['.lyr'])
        with self.assertRaises(ValidationError):
            cv.check_json_file_schemas()

        cv = config_verify.ConfigVerifier(self.all_matching_cmf_path, ['.lyr'])
        cv.check_json_file_schemas()
        self.assertTrue(True)
