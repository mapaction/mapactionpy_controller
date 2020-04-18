import os
import six
from unittest import TestCase

from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.crash_move_folder import CrashMoveFolder
from mapactionpy_controller.map_cookbook import MapCookbook


class TestMapCookBook(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.path_to_valid_cmf_des = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        self.path_to_invalid_cmf_des = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_cmf_description_one_file_and_one_dir_not_valid.json')

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
        self.fail()
