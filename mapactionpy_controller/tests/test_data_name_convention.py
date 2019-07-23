import os.path
import unittest
from unittest import TestCase
import fixtures
# works differently for python 2.7 and python 3.x
try:
    from unittest import mock
except ImportError as ie:
    import mock

from mapactionpy_controller.data_name_convention import DataNameConvention
from mapactionpy_controller.data_name_convention import DataNameException
from mapactionpy_controller.data_name_convention import DataNameInstance
from mapactionpy_controller.data_name_validators import DataNameClause
from mapactionpy_controller.data_name_validators import DataNameFreeTextClause
from mapactionpy_controller.data_name_validators import DataNameLookupClause
from mapactionpy_controller.crash_move_folder import CrashMoveFolder

class TestDataNameConvention(TestCase):

    def setUp(self):
        parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        
        self.dnc_json_path = os.path.join(
            parent_dir, 'example', 'data_naming_convention.json')

        cmf_descriptor_path = os.path.join(
            parent_dir, 'example', 'cmf_description.json')
        self.cmf = CrashMoveFolder(cmf_descriptor_path)
        self.cmf.dnc_lookup_dir = os.path.join(parent_dir, 'example')


    @unittest.SkipTest
    def test_alway_fail(self):

        self.assertTrue(False)
    @unittest.SkipTest
    def test_alway_pass(self):
        self.assertTrue(True)

    @unittest.SkipTest
    def test_load_csv_files_for_data_name_validator(self):
        self.assertTrue(False)

    @unittest.SkipTest
    def test_load_dnc_definition(self):
        # dnc = DataNameConvention(self.dnc_json_path)
        # mismatch between key listed in json file and columns in csv files
        # mismatch between csv file described in json file.
        self.assertTrue(False)
    
    @unittest.SkipTest
    def test_get_other_dnc_attributes(self):
        self.assertTrue(False)

    def test_name_validation(self):
        dnc = DataNameConvention(self.dnc_json_path)
        # pass valid names
        self.assertTrue(dnc.validate(r'lka_admn_ad2_py_s5_unocha_pp_freetext'))
        self.assertTrue(dnc.validate(r'lka_admn_ad2_py_s5_unocha_pp_free_text'))
        self.assertTrue(dnc.validate(r'lka_admn_ad3_py_s0_wfp_pp'))
        # fail - fail regex
        self.assertFalse(dnc.validate(r'lka_admnad3_py_s0_wfpocha.pp.shp'))
        # fail - clauses not listed in csv
        self.assertFalse(dnc.validate(r'aaa_admn_ad3_py_s0_wfp_pp'))
        self.assertFalse(dnc.validate(r'lka_bbbb_ad2_py_s5_ocha_pp_freetext'))
        self.assertFalse(dnc.validate(r'lka_admn_ccc_py_s5_ocha_pp_free_text'))
        # fail - clauses listed in wrong order
        self.assertFalse(dnc.validate(r'lka_admn_ad3_py_s0_wfpocha_pp'))
        self.assertFalse(dnc.validate(r'lka_ad3_admn_py_s0_wfpocha_pp'))
        self.assertFalse(dnc.validate(r'lka_admn_ad3_py_0s_pp_wfpocha'))
 

if __name__ == '__main__':
    unittest.main()
