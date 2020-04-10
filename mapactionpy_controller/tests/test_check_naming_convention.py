from unittest import TestCase
import mapactionpy_controller.check_naming_convention as check_naming_convention
import sys
import os
import six

# works differently for python 2.7 and python 3.x
if six.PY2:
    import mock  # noqa: F401
    from mock import mock_open, patch
else:
    from unittest import mock  # noqa: F401
    from unittest.mock import mock_open, patch  # noqa: F401


class TestCheckNamingConventionTool(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(
            os.path.dirname(os.path.realpath(__file__)))
        self.cmf_descriptor_path = os.path.join(
            self.parent_dir, 'example', 'cmf_description_flat_test.json')

    def test_get_args(self):
        sys.argv[1:] = [self.cmf_descriptor_path]

        args = check_naming_convention.get_args()
        self.assertEqual(self.cmf_descriptor_path, args.cmf_config_path)

        sys.argv[1:] = []
        with self.assertRaises(SystemExit):
            check_naming_convention.get_args()

    def test_check_naming_convention_check_dir(self):
        nc_desc_path = os.path.join(self.parent_dir, 'example', 'data_naming_convention.json')

        dir_of_valid_names = os.path.join(self.parent_dir, 'tests',
                                          'testfiles', 'test_naming_convention', 'valid'
                                          )

        dir_of_invalid_names = os.path.join(self.parent_dir, 'tests',
                                            'testfiles', 'test_naming_convention', 'invalid'
                                            )

        # point to empty directories
        tmp_result = check_naming_convention.check_dir(self.parent_dir, nc_desc_path, '.shp', False)
        self.assertEqual(tmp_result, 0)

        # point to a compliant, populated directory
        tmp_result = check_naming_convention.check_dir(dir_of_valid_names, nc_desc_path, '.shp', False)
        self.assertEqual(tmp_result, 0)

        # point to a non-compliant, populated directory
        tmp_result = check_naming_convention.check_dir(dir_of_invalid_names, nc_desc_path, '.shp', True)
        self.assertGreater(tmp_result, 0)

        # point to a non-compliant, populated directory
        tmp_result = check_naming_convention.check_dir(dir_of_invalid_names, nc_desc_path, '.shp', False)
        self.assertGreater(tmp_result, 0)
