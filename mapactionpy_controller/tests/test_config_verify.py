import os
import sys
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
        # No parameter given at commandline
        sys.argv[1:] = []
        with self.assertRaises(SystemExit):
            config_verify.run_checks(None)

        # A valid cmf description
        sys.argv[1:] = ['--cmf', self.path_to_valid_cmf_des, 'cmf-only']
        try:
            config_verify.run_checks(None)
            self.assertTrue(True)
        except SystemExit as se:
            self.fail(se)

        # An Invalid cmf description
        sys.argv[1:] = ['--cmf', self.path_to_invalid_cmf_des, 'cmf-only']
        with self.assertRaises(SystemExit):
            config_verify.run_checks(None)

    def test_check_lyr_props_vs_rendering_dir(self):
        sys.argv[1:] = ['-c', self.mismatching_cmf_path, 'lp-vs-rendering', '-e', 'lyr']

        with self.assertRaises(SystemExit):
            config_verify.run_checks(None)

        sys.argv[1:] = ['--cmf', self.all_matching_cmf_path, 'lp-vs-rendering', '-e', 'lyr']
        try:
            config_verify.run_checks(None)
            self.assertTrue(True)
        except SystemExit as se:
            self.fail(se)

    def test_check_lyr_props_vs_map_cookbook(self):
        sys.argv[1:] = ['-c', self.mismatching_cmf_path, 'lp-vs-cb']

        with self.assertRaises(SystemExit):
            config_verify.run_checks(None)

        sys.argv[1:] = ['--cmf', self.all_matching_cmf_path, 'lp-vs-cb']
        try:
            config_verify.run_checks(None)
            self.assertTrue(True)
        except SystemExit as se:
            self.fail(se)

    def test_check_config_file_schemas(self):
        schema_errors_cmf_path = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'config_schemas',
            'fixture_cmf_pointing_schema_errors.json'
        )
        sys.argv[1:] = ['-c', schema_errors_cmf_path, 'check-schemas']

        with self.assertRaises(SystemExit):
            config_verify.run_checks(None)

        sys.argv[1:] = ['--cmf', self.all_matching_cmf_path, 'check-schemas']
        config_verify.run_checks(None)
        self.assertTrue(True)
