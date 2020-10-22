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

        # 2) test with valid cmf file
        test_lp = LayerProperties(self.path_to_valid_cmf_des, "test", verify_on_creation=False)
        self.assertIsInstance(test_lp, LayerProperties)

        # 3) test with invalid cmf object (eg and CrashMoveFolder object
        #    where verify_paths() returns False)
        test_cmf = CrashMoveFolder(self.path_to_invalid_cmf_des, verify_on_creation=False)
        self.assertRaises(ValueError, LayerProperties, test_cmf, "test")

        # 4) test with invalid cmd file
        self.assertRaises(ValueError, LayerProperties, self.path_to_invalid_cmf_des, "test")

    def test_zero_length_file_extention(self):
        test_cmf = CrashMoveFolder(self.path_to_valid_cmf_des)

        test_lp1 = LayerProperties(test_cmf, '', verify_on_creation=False)
        self.assertIsInstance(test_lp1, LayerProperties)

        layer_rendering_test_root = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'test_layer_rendering')
        test_cmf.layer_properties = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_layer_properties_four_layers.json')
        test_cmf.layer_rendering = os.path.join(layer_rendering_test_root, 'four_files_exact_match')
        test_lp2 = LayerProperties(test_cmf, '', verify_on_creation=True)
        self.assertIsInstance(test_lp2, LayerProperties)

    def test_verify_with_rendering_files(self):
        # self.fail()

        # load a valid CMF
        test_cmf = CrashMoveFolder(self.path_to_valid_cmf_des)
        # Overwright the Layer Properties file path with
        # mapactionpy_controller\tests\testfiles\fixture_layer_properties_four_layers.json
        test_cmf.layer_properties = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'fixture_layer_properties_four_layers.json')

        layer_rendering_test_root = os.path.join(
            self.parent_dir, 'tests', 'testfiles', 'test_layer_rendering')
        test_cmf.layer_rendering

        # 1) Exact match of .lyr files and layer properties
        test_cmf.layer_rendering = os.path.join(layer_rendering_test_root, 'four_files_exact_match')
        lyr_lp = LayerProperties(test_cmf, '.lyr', verify_on_creation=True)
        self.assertFalse(lyr_lp.is_difference_with_layer_rendering_dir())

        qml_lp = LayerProperties(test_cmf, '.qml', verify_on_creation=True)
        self.assertFalse(qml_lp.is_difference_with_layer_rendering_dir())

        # 2) .lyr files which don't have layer properties entries
        test_cmf.layer_rendering = os.path.join(layer_rendering_test_root, 'five_files')
        self.assertRaises(ValueError, LayerProperties, test_cmf, '.lyr')
        self.assertRaises(ValueError, LayerProperties, test_cmf, '.qml')

        # 3) layer properties entries which don't have cooresponding .lyr files.
        test_cmf.layer_rendering = os.path.join(layer_rendering_test_root, 'three_files')
        self.assertRaises(ValueError, LayerProperties, test_cmf, '.lyr')
        self.assertRaises(ValueError, LayerProperties, test_cmf, '.qml')

        # 4) Both 2 & 3 combined
        test_cmf.layer_rendering = os.path.join(layer_rendering_test_root, 'four_files_mis_match')
        self.assertRaises(ValueError, LayerProperties, test_cmf, '.lyr')
        self.assertRaises(ValueError, LayerProperties, test_cmf, '.qml')

        # 6) Overrided validation checks in constructor
        test_cmf.layer_rendering = os.path.join(layer_rendering_test_root, 'four_files_mis_match')
        long_lived_lp = LayerProperties(test_cmf, '.lyr', verify_on_creation=False)
        self.assertTrue(long_lived_lp.is_difference_with_layer_rendering_dir())
        long_lived_lp.cmf.layer_rendering = os.path.join(layer_rendering_test_root, 'four_files_exact_match')
        self.assertFalse(long_lived_lp.is_difference_with_layer_rendering_dir())

        # 7) Same results whether or not the '.' character is included in the file extension
        test_cmf.layer_rendering = os.path.join(layer_rendering_test_root, 'four_files_exact_match')
        # passing example with dot
        lyr_lp = LayerProperties(test_cmf, '.lyr', verify_on_creation=True)
        self.assertFalse(lyr_lp.is_difference_with_layer_rendering_dir())
        # passing example without dot
        lyr_lp = LayerProperties(test_cmf, 'lyr', verify_on_creation=True)
        self.assertFalse(lyr_lp.is_difference_with_layer_rendering_dir())
        # failing example with dot
        test_cmf.layer_rendering = os.path.join(layer_rendering_test_root, 'four_files_mis_match')
        self.assertRaises(ValueError, LayerProperties, test_cmf, '.lyr')
        # failing example without dot
        test_cmf.layer_rendering = os.path.join(layer_rendering_test_root, 'four_files_mis_match')
        self.assertRaises(ValueError, LayerProperties, test_cmf, 'lyr')
