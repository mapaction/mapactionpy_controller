import unittest
from unittest import TestCase
from . import fixtures

import mapactionpy_controller

class TestMAController(TestCase):

    def setUp(self):
        self.iso3 = 'gbr'

    def test_alway_fail(self):
        self.assertTrue(False)

    def test_alway_pass(self):
        self.assertTrue(True)

    def test_substitute_iso3_in_regex(self):
        test_str_positive = mapactionpy_controller.substitute_iso3_in_regex(
            fixtures.fixture_regex_without_iso3_code, self.iso3)
        self.assertEqual(test_str_positive, fixtures.fixture_regex_with_iso3_code)

        test_str_negative = mapactionpy_controller.substitute_iso3_in_regex(
            fixtures.fixture_regex_with_negative_iso3_code, self.iso3)
        self.assertEqual(test_str_negative, fixtures.fixture_regex_with_negative_iso3_code)

        self.assertTrue(False,
                        "Test test_substitute_iso3_in_regex currently fail. The implenmentation"
                        " does not need to include a function"
                        " `mapactionpy_controller.substitute_iso3_in_regex`. This is included to"
                        " be _indicative_ of the tests required.")

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
