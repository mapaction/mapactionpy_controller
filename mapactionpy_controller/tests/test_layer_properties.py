import os
from unittest import TestCase

from mapactionpy_controller.layer_properties import LayerProperties
from mapactionpy_controller.crash_move_folder import CrashMoveFolder


class TestLayerProperties(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.path_to_valid_cmf_des = os.path.join(self.parent_dir, 'example', 'cmf_description_flat_test.json')
        self.path_to_invalid_cmf_des = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_cmf_description_one_file_and_one_dir_not_valid.json')

    def test_different_cmf_args(self):
        # 1) test with valid cmf object
        test_cmf = CrashMoveFolder(self.path_to_valid_cmf_des)
        test_lp = LayerProperties(test_cmf, "test", verify_on_creation=False)
        self.assertIsInstance(test_lp, LayerProperties)

        # 2) test with valid cmd file
        test_lp = LayerProperties(self.path_to_valid_cmf_des, "test", verify_on_creation=False)
        self.assertIsInstance(test_lp, LayerProperties)

        # 3) test with invalid cmf object (eg and CrashMoveFolder object
        #    where verify_paths() returns False)
        test_cmf = CrashMoveFolder(self.path_to_invalid_cmf_des, verify_on_creation=False)
        self.assertRaises(ValueError, LayerProperties, test_cmf, "test")

        # 4) test with invalid cmd file
        self.assertRaises(ValueError, LayerProperties, self.path_to_invalid_cmf_des, "test")

    def test_verify_with_rendering_files(self):
        self.fail()

        # list_four_lyr_files = [
        #     'mainmap-tran-rds-ln-s0-allmaps.lyr',
        #     'mainmap-tran-rds-ln-s1-allmaps.lyr',
        #     'mainmap-tran-rds-ln-s2-allmaps.lyr',
        #     'mainmap-tran-rrd-ln-s0-allmaps.lyr'
        # ]

        # 1) Exact match of .lyr files and layer properties
        # 2) .lyr files which don't have layer properties entries
        # 3) layer properties entries which don't have cooresponding .lyr files.
        # 4) Both 2 & 3 combined
        # 5) Both 2 & 3 combined, but for .qml files
