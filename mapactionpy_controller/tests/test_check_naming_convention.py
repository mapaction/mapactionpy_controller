from unittest import TestCase
import mapactionpy_controller.check_naming_convention as check_naming_convention
import mapactionpy_controller.name_convention as name_convention
from mapactionpy_controller.crash_move_folder import CrashMoveFolder

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

    def test_get_single_file_checker(self):
        cmf = CrashMoveFolder(self.cmf_descriptor_path)
        nc_desc_path = os.path.join(self.parent_dir, 'example', 'data_naming_convention.json')
        nc = name_convention.NamingConvention(nc_desc_path)

        passing_path = '/path/to/some/gisdata/206_bldg/ken_bldg_bdg_py_s4_osm_pp.shp'
        func = check_naming_convention.get_single_file_checker(passing_path, nc, cmf)
        self.assertIn('parsable and valid', func().get_message)

        failing_path = '/path/to/some/gisdata/202_admn/ken_admn_ad0_ln_s0_IEBC_pp_HDX.shp'
        func = check_naming_convention.get_single_file_checker(failing_path, nc, cmf)
        self.assertRaises(ValueError, func)
