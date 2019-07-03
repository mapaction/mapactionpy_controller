from unittest import TestCase
import fixtures

import mapactionpy_controller

class TestMAController(TestCase):
    def test_alway_fail(self):
        self.assertTrue(False)
		
    def test_alway_pass(self):
        self.assertTrue(True)

    def test_substitute_iso3_in_regex(self):
        iso3 = 'gbr'
        test_str_positive = mapactionpy_controller.substitute_iso3_in_regex(
            fixtures.fixture_regex_without_iso3_code, iso3)
        self.assertEqual(test_str_positive, fixtures.fixture_regex_with_iso3_code)

        test_str_negative = mapactionpy_controller.substitute_iso3_in_regex(
            fixtures.fixture_regex_with_negative_iso3_code, iso3)
        self.assertEqual(test_str_negative, fixtures.fixture_regex_with_negative_iso3_code)

        self.assertTrue(False,
                        "Test test_substitute_iso3_in_regex currently fail. The implenmentation"
                        " does not need to include a function"
                        " `mapactionpy_controller.substitute_iso3_in_regex`. This is included to"
                        " be _indicative_ of the tests required.")
