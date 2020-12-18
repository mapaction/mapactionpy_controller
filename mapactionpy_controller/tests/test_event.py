from unittest import TestCase
import mapactionpy_controller.event as event
import os
from jsonschema import ValidationError
import json
import six


class TestEvent(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(
            os.path.dirname(os.path.realpath(__file__)))
        self.event_descriptor_path = os.path.join(
            self.parent_dir, 'example', 'event_description.json')
        self.failing_event_descriptor_path = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_event_description_missing_operation_id.json')

    def test_constructor(self):
        # test creation when using a valid json description:
        test_cmf = event.Event(self.event_descriptor_path)
        self.assertIsInstance(test_cmf, event.Event)

        # test exception is raised when passed a non-existant file
        self.assertRaises(IOError, event.Event, '/path/to/nonexistant/file.json')
        # test exception is raised for an invalid json file:
        self.assertRaises(ValidationError, event.Event, self.failing_event_descriptor_path)

    def test_fictional_country_name(self):
        with open(self.event_descriptor_path, 'r') as edf:
            base_event_def = json.load(edf)

        working_name_supplied = [
            ('ABC', u'Alphabet Land'),
            ('ABC', u'UNKNOWN'),
            ('GEO', u'Georgia'),
            ('MOZ', u'Mozambique'),
            ('COG', u'Congo'),
            ('COD', u'Congo'),
            ('GBR', u'United Kingdom'),
            ('GBR', u'England'),
            ('GBR', u'Ireland'),
            ('IRL', u'Ireland')
        ]

        for test_iso3, test_name in working_name_supplied:
            # Do supply the country name
            event_def = base_event_def.copy()
            event_def['affected_country_iso3'] = test_iso3
            event_def['country_name'] = test_name
            actual_name = event._parse_country_name(event_def)
            self.assertEqual(test_name, actual_name)

        working_name_not_supplied = [
            ('COG', u'Congo'),
            ('COD', u'Congo, The Democratic Republic of the'),
            ('GBR', u'United Kingdom'),
            ('IRL', u'Ireland')
        ]

        for test_iso3, test_name in working_name_not_supplied:
            # Don't supply the country name
            event_def = base_event_def.copy()
            event_def['affected_country_iso3'] = test_iso3
            actual_name = event._parse_country_name(event_def)
            self.assertEqual(test_name, actual_name)

        error_cases = [
            ('MOZ', u'Alphabet Land', 'supply a real ISO3 code with a fictional country name'),
            ('ABC', u'Mozambique', 'supply a real country name with a fictional ISO3 code'),
            ('ABC', None, 'A `country_name` value must be specified for fictional countries')
        ]

        for test_iso3, test_name, fail_msg in error_cases:
            event_def = base_event_def.copy()
            event_def['affected_country_iso3'] = test_iso3
            event_def['country_name'] = test_name
            with self.assertRaises(ValueError) as ve:
                event._parse_country_name(event_def)

            if six.PY2:
                self.assertRegexpMatches(str(ve.exception), fail_msg)
            else:
                self.assertRegex(str(ve.exception), fail_msg)
