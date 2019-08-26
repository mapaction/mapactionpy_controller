import os.path
import unittest
import six
from unittest import TestCase
from mapactionpy_controller.data_name_convention import DataNameConvention, DataNameException
from mapactionpy_controller.data_name_validators import DataNameClause, DataNameLookupClause
from mapactionpy_controller.crash_move_folder import CrashMoveFolder

# works differently for python 2.7 and python 3.x
if six.PY2:
    import mock  # noqa: F401
else:
    from unittest import mock  # noqa: F401


class TestDataNameConvention(TestCase):

    def setUp(self):
        parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        self.dnc_json_path = os.path.join(
            parent_dir, 'example', 'data_naming_convention.json')

        self.test_files_dir = os.path.join(parent_dir, 'tests', 'testfiles')

        cmf_descriptor_path = os.path.join(
            parent_dir, 'example', 'cmf_description.json')
        self.cmf = CrashMoveFolder(cmf_descriptor_path)
        self.cmf.dnc_lookup_dir = os.path.join(parent_dir, 'example')

    def test_load_csv_files_for_data_name_validator(self):
        failing_csv = os.path.join(self.test_files_dir, '06_source_lookup_duplicate_prikey.csv')
        working_csv = os.path.join(self.cmf.dnc_lookup_dir, '06_source.csv')

        # Test with a valid csv table
        dnlc = DataNameLookupClause('test', working_csv, 'Value')
        self.assertEqual(dnlc.lookup_field, 'Value')

        # Test with an valid csv file but a mismatch between primary key parameter and file contents
        self.assertRaises(DataNameException, DataNameLookupClause,
                          'test', working_csv, 'inexistant-primary-key')

        # Test with an invalid csv table (duplicate primary key)
        self.assertRaises(DataNameException, DataNameLookupClause, 'test', failing_csv, 'Value')

    @unittest.SkipTest
    def test_load_dnc_definition(self):
        # dnc = DataNameConvention(self.dnc_json_path)
        # mismatch between key listed in json file and columns in csv files
        # mismatch between csv file described in json file.
        self.assertTrue(False)

    def test_abstract_validator(self):
        self.assertRaises(NotImplementedError, DataNameClause)

    def test_get_other_dnc_attributes(self):
        # pylint: disable=no-member
        dnc = DataNameConvention(self.dnc_json_path)
        # dni is None if no match with regex
        dnr = dnc.validate(r'lka_admnad3_py_s0_wfpocha.pp.shp')
        self.assertIsNone(dnr)

        # dni.is_valid is False as not all clauses are found in lookups,
        # but details for the valid clauses are found.
        dnr = dnc.validate(r'aaa_admn_ad3_py_s0_wfp_pp')
        self.assertFalse(dnr.is_valid)
        self.assertFalse(dnr.geoext.is_valid)
        self.assertFalse(dnr.geoext.is_valid)
        self.assertTrue(dnr.datacat.is_valid)
        self.assertTrue(dnr.datatheme.is_valid)
        self.assertTrue(dnr.geom.is_valid)
        self.assertTrue(dnr.scale.is_valid)
        self.assertTrue(dnr.source.is_valid)
        self.assertTrue(dnr.perm.is_valid)
        self.assertTrue(dnr.freetext.is_valid)

        # clause details are found
        ref_datatheme = {'Description': 'Administrative boundary (level 3)', 'Category': 'admn'}
        self.assertEqual(ref_datatheme, dnr.datatheme._asdict())
        ref_source = {'Organisation': 'World Food Program', 'url': '',
                      'admn1Name': '', 'admn1PCode': '', 'admn2Name': '', 'admn2PCode': ''}
        self.assertEqual(ref_source, dnr.source._asdict())

        # with Free text clause present
        dnr = dnc.validate(r'aaa_admn_ad3_py_s0_wfp_pp_myfreetext')
        self.assertFalse(dnr.is_valid)
        self.assertEqual(dnr.freetext.text, 'myfreetext')

        # Fully valid name without Free text clause
        dnr = dnc.validate(r'lka_admn_ad3_py_s0_wfp_pp')
        self.assertTrue(dnr.is_valid)
        self.assertEqual(dnr.freetext.is_valid, True)
        self.assertIsNone(dnr.freetext.text)

        # Fully valid name with Free text clause present
        dnr = dnc.validate(r'lka_admn_ad3_py_s0_wfp_pp_myfreetext')
        self.assertTrue(dnr.is_valid)
        self.assertEqual(dnr.freetext.text, 'myfreetext')

    def test_name_validation(self):
        dnc = DataNameConvention(self.dnc_json_path)
        # pass valid names
        dnr = dnc.validate(r'lka_admn_ad2_py_s5_unocha_pp_myfreetext')
        self.assertTrue(dnc.validate(r'lka_admn_ad2_py_s5_unocha_pp_freetext'))
        self.assertTrue(dnc.validate(r'lka_admn_ad2_py_s5_unocha_pp_free_text'))
        self.assertTrue(dnc.validate(r'lka_admn_ad3_py_s0_wfp_pp'))
        # fail - fail regex
        self.assertFalse(dnc.validate(r'lka_admnad3_py_s0_wfpocha.pp.shp'))
        # fail - clauses not listed in csv
        self.assertFalse(dnc.validate(r'aaa_admn_ad3_py_s0_wfp_pp').is_valid)
        self.assertFalse(dnc.validate(
            r'lka_bbbb_ad2_py_s5_ocha_pp_freetext').is_valid)
        self.assertFalse(dnc.validate(
            r'lka_admn_ccc_py_s5_ocha_pp_free_text').is_valid)
        # fail - clauses listed in wrong order
        dnr = dnc.validate(r'lka_admn_ad3_py_s0_wfpocha_pp')
        self.assertFalse(False if dnr is None else dnr.is_valid)
        dnr = dnc.validate(r'lka_ad3_admn_py_s0_wfpocha_pp')
        self.assertFalse(False if dnr is None else dnr.is_valid)
        dnr = dnc.validate(r'lka_admn_ad3_py_0s_pp_wfpocha')
        self.assertFalse(False if dnr is None else dnr.is_valid)
