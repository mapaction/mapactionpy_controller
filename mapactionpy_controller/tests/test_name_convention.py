import os.path
import six
from unittest import TestCase
from mapactionpy_controller.name_convention import NamingConvention, NamingException
from mapactionpy_controller.name_clause_validators import NamingClause, NamingLookupClause
from mapactionpy_controller.crash_move_folder import CrashMoveFolder

# works differently for python 2.7 and python 3.x
if six.PY2:
    import mock  # noqa: F401
else:
    from unittest import mock  # noqa: F401


class DummyClass(object):
    """
    Used within TestNamingConvention.test_load_dnc_definition() to test the case
    that a valid class is supplied, but one which doesn't inherit from
    mapactionpy_controller.name_convention.NameClause
    """

    def __init__(self, dummy_path, **kwargs):
        pass


class TestNamingConvention(TestCase):

    def setUp(self):
        parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

        self.dnc_json_path = os.path.join(
            parent_dir, 'example', 'data_naming_convention.json')

        self.test_files_dir = os.path.join(parent_dir, 'tests', 'testfiles', '.')

        cmf_descriptor_path = os.path.join(
            parent_dir, 'example', 'cmf_description.json')
        self.cmf = CrashMoveFolder(cmf_descriptor_path, verify_on_creation=False)
        self.cmf.dnc_lookup_dir = os.path.join(parent_dir, 'example')

    def test_load_csv_files_for_data_name_validator(self):
        # Test with a valid csv table
        dnlc = NamingLookupClause(self.dnc_json_path, filename='06_source.csv', name='test', lookup_field='Value')
        self.assertEqual(dnlc.lookup_field, 'Value')

        # Test with an valid csv file but a mismatch between primary key parameter and file contents
        self.assertRaises(NamingException, NamingLookupClause,
                          self.dnc_json_path, filename='06_source.csv', name='test',
                          lookup_field='non-existant-primary-key')

        # Test with an invalid csv table (duplicate primary key)
        self.assertRaises(NamingException, NamingLookupClause, self.test_files_dir,
                          filename='06_source_lookup_duplicate_prikey.csv',
                          name='test', lookup_field='Value')

    def test_load_dnc_definition(self):

        test_convention_files = (
            'fixture_name_convention_clause_def_and_regex_groupname_mismatch.json',
            'fixture_name_convention_clause_def_not_in_regex_groupname.json',
            'fixture_name_convention_missing_clause_def.json',
            'fixture_name_convention_incorrect_validation_class.json',
            'fixture_name_convention_nonexistant_validation_class.json'
        )

        for test_filename in test_convention_files:
            test_filepath = os.path.join(self.test_files_dir, test_filename)
            self.assertRaises(NamingException, NamingConvention, test_filepath)

    def test_abstract_validator(self):
        self.assertRaises(NotImplementedError, NamingClause, self.dnc_json_path)

        # Dummy implenmentation of calling the validate() method on NamingClause
        class DummyTestNameClause(NamingClause):
            def validate(self, clause_value, **kwargs):
                if six.PY2:
                    return super(DummyTestNameClause, self).validate(clause_value, **kwargs)
                else:
                    return super().validate(clause_value, **kwargs)

        tdnc = DummyTestNameClause(self.dnc_json_path)
        self.assertRaises(NotImplementedError, tdnc.validate, 'test')

    def test_get_other_dnc_attributes(self):
        # pylint: disable=no-member
        dnc = NamingConvention(self.dnc_json_path)
        # dnr.is_parsable is False if no match with regex
        dnr = dnc.validate(r'lka_admnad3_py_s0_wfpocha.pp.shp')
        self.assertFalse(dnr.is_parsable)

        # dnr.is_valid is False as not all clauses are found in lookups,
        # but details for the valid clauses are found.
        dnr = dnc.validate(r'aaa_admn_ad3_py_s0_wfp_pp')
        self.assertTrue(dnr.is_parsable)
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
        ref_datatheme = {'Value': 'ad3', 'Description': 'Administrative boundary (level 3)', 'Category': 'admn'}
        self.assertEqual(ref_datatheme, dnr.datatheme._asdict())
        # self.assertEqual(ref_datatheme, dnr.datatheme._asdict())

        ref_source = {'Value': 'wfp', 'Organisation': 'World Food Program', 'url': '',
                      'admn1Name': '', 'admn1PCode': '', 'admn2Name': '', 'admn2PCode': ''}
        self.assertEqual(ref_source, dnr.source._asdict())

        # with Free text clause present
        dnr = dnc.validate(r'aaa_admn_ad3_py_s0_wfp_pp_myfreetext')
        self.assertFalse(dnr.is_valid)
        # self.assertEqual(dnr.freetext.Value, 'myfreetext')

        # Fully valid name without Free text clause
        dnr = dnc.validate(r'lka_admn_ad3_py_s0_wfp_pp')
        self.assertTrue(dnr.is_valid)
        self.assertEqual(dnr.freetext.is_valid, True)
        self.assertIsNone(dnr.freetext.Value)

        # Fully valid name with Free text clause present
        dnr = dnc.validate(r'lka_admn_ad3_py_s0_wfp_pp_myfreetext')
        self.assertTrue(dnr.is_valid)
        self.assertEqual(dnr.freetext.Value, 'myfreetext')

    def test_name_validation(self):
        dnc = NamingConvention(self.dnc_json_path)
        # # pass valid names
        # dnr = dnc.validate(r'lka_admn_ad2_py_s5_unocha_pp_myfreetext')
        self.assertTrue(dnc.validate(r'lka_admn_ad2_py_s5_unocha_pp_freetext').is_parsable)
        self.assertTrue(dnc.validate(r'lka_admn_ad2_py_s5_unocha_pp_free_text').is_parsable)
        self.assertTrue(dnc.validate(r'lka_admn_ad3_py_s0_wfp_pp').is_parsable)
        # fail - fail regex
        self.assertFalse(dnc.validate(r'lka_admnad3_py_s0_wfpocha.pp.shp').is_parsable)
        # fail - clauses not listed in csv
        self.assertFalse(dnc.validate(r'aaa_admn_ad3_py_s0_wfp_pp').is_valid)
        self.assertFalse(dnc.validate(r'lka_bbbb_ad2_py_s5_ocha_pp_freetext').is_valid)
        self.assertFalse(dnc.validate(r'lka_admn_ccc_py_s5_ocha_pp_free_text').is_valid)
        # fail - clauses listed in wrong order
        dnr = dnc.validate(r'lka_admn_ad3_py_s0_wfpocha_pp')
        self.assertFalse(False if dnr is None else dnr.is_valid)
        dnr = dnc.validate(r'lka_ad3_admn_py_s0_wfpocha_pp')
        self.assertFalse(False if dnr is None else dnr.is_valid)
        dnr = dnc.validate(r'lka_admn_ad3_py_0s_pp_wfpocha')
        self.assertFalse(False if dnr is None else dnr.is_valid)

        # Clauses in upper case
        # Clauses with mixed case
        # Entire name in upper case
        self.assertTrue(dnc.validate(r'lKa_admn_ad3_py_s0_wfp_pp').is_valid)
        self.assertTrue(dnc.validate(r'LKA_admn_ad3_py_s0_wfp_pp').is_valid)
        self.assertTrue(dnc.validate(r'lka_aDmn_ad3_py_s0_wfp_pp').is_valid)
        self.assertTrue(dnc.validate(r'lka_ADMN_ad3_py_s0_wfp_pp').is_valid)
        self.assertTrue(dnc.validate(r'lka_admn_aD3_py_s0_wfp_pp').is_valid)
        self.assertTrue(dnc.validate(r'lka_admn_AD3_py_s0_wfp_pp').is_valid)
        self.assertTrue(dnc.validate(r'lka_admn_ad3_Py_s0_wfp_pp').is_valid)
        self.assertTrue(dnc.validate(r'lka_admn_ad3_PY_s0_wfp_pp').is_valid)
        self.assertTrue(dnc.validate(r'lka_admn_ad3_py_S0_wfp_pp').is_valid)
        self.assertTrue(dnc.validate(r'lka_admn_ad3_py_s0_wFp_pp').is_valid)
        self.assertTrue(dnc.validate(r'lka_admn_ad3_py_s0_WFP_pp').is_valid)
        self.assertTrue(dnc.validate(r'lka_admn_ad3_py_s0_wfp_pP').is_valid)
        self.assertTrue(dnc.validate(r'lka_admn_ad3_py_s0_wfp_PP').is_valid)
        self.assertTrue(dnc.validate(r'LKA_ADMN_AD3_PY_S0_WFP_PP').is_valid)

    def test_name_to_validate_property(self):
        dnc = NamingConvention(self.dnc_json_path)

        # test the full name is retrivable for a parsable name
        dnr = dnc.validate(r'aaa_admn_ad3_py_s0_wfp_pp')
        self.assertTrue(dnr.is_parsable)
        self.assertEqual(dnr.name_to_validate, r'aaa_admn_ad3_py_s0_wfp_pp')
        # test the full name is retrivable for a non-parsable name
        dnr = dnc.validate(r'lka_admnad3_py_s0_wfpocha.pp.shp')
        self.assertFalse(dnr.is_parsable)
        self.assertEqual(dnr.name_to_validate, r'lka_admnad3_py_s0_wfpocha.pp.shp')

    def test_get_message_property(self):
        dnc = NamingConvention(self.dnc_json_path)

        # message when dnr.is_parsable is False
        dnr = dnc.validate(r'lka_admnad3_py_s0_wfpocha.pp.shp')
        self.assertFalse(dnr.is_parsable)
        # print(dnr.get_message)
        self.assertRegexpMatches(dnr.get_message, r'not parsable')

        # message when dnr.is_parsable is True but dnr.is_valid is False
        dnr = dnc.validate(r'aaa_admn_ad3_py_s0_wfp_pp')
        self.assertTrue(dnr.is_parsable)
        self.assertFalse(dnr.is_valid)
        self.assertRegexpMatches(dnr.get_message, r'is parsable')
        self.assertRegexpMatches(dnr.get_message, r'not valid')
        # print(dnr.get_message)

        # message when dnr.is_valid is True
        dnr = dnc.validate(r'lka_admn_ad3_py_s0_wfp_pp')
        self.assertTrue(dnr.is_valid)
        self.assertRegexpMatches(dnr.get_message, r'is valid')
        # print(dnr.get_message)
