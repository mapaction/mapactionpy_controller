import os
from unittest import TestCase

from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.crash_move_folder import CrashMoveFolder


class TestMapCookBook(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.path_to_valid_cmf_des = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        self.path_to_invalid_cmf_des = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_cmf_description_one_file_and_one_dir_not_valid.json')

    def test_different_cmf_args(self):
        self.fail()

    def test_layer_props_and_cmf_mismatch(self):
        self.fail()

    def test_layer_props_and_cookbook_mismatch(self):
        self.fail()
