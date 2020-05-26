from unittest import TestCase
import mapactionpy_controller.event as event
import os
from jsonschema import ValidationError


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
