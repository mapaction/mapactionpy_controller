import os.path
import unittest
from unittest import TestCase
# import fixtures
# import fixtures_dnc

from mapactionpy_controller.data_name_convention import DataNameConvention
from mapactionpy_controller.data_name_validators import DataNameClause
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
    def test_load_csv_files_for_data_name_validator(self):
        self.assertTrue(False)

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
        self.assertIsNone(dnr.geoext)
        self.assertFalse(dnr.geoext)
        self.assertTrue(dnr.datacat)
        self.assertTrue(dnr.datatheme)
        self.assertTrue(dnr.geom)
        self.assertTrue(dnr.scale)
        self.assertTrue(dnr.source)
        self.assertTrue(dnr.perm)
        self.assertTrue(dnr.freetext)

        # clause details are found
        ref_datatheme = {'Description': 'Administrative boundary (level 3)', 'Category': 'admn'}
        self.assertEqual(ref_datatheme, dnr.datatheme._asdict())
        ref_source = {'Organisation': 'World Food Program', 'url': '',
                      'admn1Name': '', 'admn1PCode': '', 'admn2Name': '', 'admn2PCode': ''}
        self.assertEqual(ref_source, dnr.source._asdict())

        # with Free text clause present
        dnr = dnc.validate(r'aaa_admn_ad3_py_s0_wfp_pp_myfreetext')
        self.assertFalse(dnr.is_valid)
        self.assertEqual(dnr.freetext, 'myfreetext')

        # Fully valid name without Free text clause
        dnr = dnc.validate(r'lka_admn_ad3_py_s0_wfp_pp')
        self.assertTrue(dnr.is_valid)
        self.assertEqual(dnr.freetext, True)

        # Fully valid name with Free text clause present
        dnr = dnc.validate(r'lka_admn_ad3_py_s0_wfp_pp_myfreetext')
        self.assertTrue(dnr.is_valid)
        self.assertEqual(dnr.freetext, 'myfreetext')

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
