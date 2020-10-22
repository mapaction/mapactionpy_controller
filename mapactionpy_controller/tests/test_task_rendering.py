import os
from unittest import TestCase

import mapactionpy_controller.task_renderer as task_renderer
from mapactionpy_controller.name_convention import NamingConvention
from mapactionpy_controller.task_renderer import FixDataNameTask, TaskReferralBase
from mapactionpy_controller.crash_move_folder import CrashMoveFolder


class TestTaskRendering(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.dir_to_valid_cmf_des = os.path.join(self.parent_dir, 'example')
        self.path_to_valid_cmf_des = os.path.join(self.dir_to_valid_cmf_des, 'cmf_description_flat_test.json')

    def test_get_task_unique_summary(self):
        dnc_json_path = os.path.join(self.parent_dir, 'example', 'data_naming_convention.json')
        nc = NamingConvention(dnc_json_path)
        cmf = CrashMoveFolder(self.path_to_valid_cmf_des)

        # Three cases
        # 1. Parsable and Valid
        # 2. Parsable and Not Valid
        # 3. Not Parsable
        #
        # key= is the name to test
        # value= is a list of expected results from rendering the mustache elements in `mustache_tmpls`
        test_cases = {
            'lka_admn_ad2_py_s5_unocha_pp_freetext': [
                'lka_admn_ad2_py_s5_unocha_pp_freetext',
                'parsable but not valid',
                (
                    '* "ad2" is a recognised value for the clause "datatheme" found in "03_theme.csv"\n'
                    '* "admn" is a recognised value for the clause "datacat" found in "02_category.csv"\n'
                    '* "freetext" is valid for freetext (as is almost anything)\n'
                    '* "lka" is a recognised value for the clause "geoext" found in "01_geoextent.csv"\n'
                    '* "pp" is a recognised value for the clause "perm" found in "07_permission.csv"\n'
                    '* "py" is a recognised value for the clause "geom" found in "04_geometry.csv"\n'
                    '* "s5" is a recognised value for the clause "scale" found in "05_scale.csv"\n'
                    '* "unocha" is a recognised value for the clause "source" found in "06_source.csv"\n'
                ),
                ''
            ],
            'lka_admn_ad77_py_s5_unocha_pp_freetext': [
                'lka_admn_ad77_py_s5_unocha_pp_freetext',
                'parsable but not valid',
                (
                    '* "admn" is a recognised value for the clause "datacat" found in "02_category.csv"\n'
                    '* "freetext" is valid for freetext (as is almost anything)\n'
                    '* "lka" is a recognised value for the clause "geoext" found in "01_geoextent.csv"\n'
                    '* "pp" is a recognised value for the clause "perm" found in "07_permission.csv"\n'
                    '* "py" is a recognised value for the clause "geom" found in "04_geometry.csv"\n'
                    '* "s5" is a recognised value for the clause "scale" found in "05_scale.csv"\n'
                    '* "unocha" is a recognised value for the clause "source" found in "06_source.csv"\n'
                ),
                '* "ad77" is not a recognised value for the clause "datatheme" found in "03_theme.csv"\n'
            ],
            'unparsable-name': [
                'unparsable-name',
                'not parsable',
                '',
                ''
            ]
        }

        mustache_tmpls = [
            '<%name_result.name_to_validate%>',
            ('<%#name_result.is_parsable%>parsable but not valid<%/name_result.is_parsable%>'
             '<%^name_result.is_parsable%>not parsable<%/name_result.is_parsable%>'),
            '<%#name_result.valid_clause_list%>* <%&valid_clause%>\n<%/name_result.valid_clause_list%>',
            '<%#name_result.invalid_clause_list %>* <%&invalid_clause%>\n<%/name_result.invalid_clause_list %>'
        ]

        # for name_to_test, expected_result_list in test_cases.iteritems():
        while test_cases:
            name_to_test, expected_result_list = test_cases.popitem()
            # print(name_to_test)
            nr = nc.validate(name_to_test)
            fdnt = FixDataNameTask(nr, cmf)

            for test_template, expected_result in zip(mustache_tmpls, expected_result_list):
                # create the Task object
                # override the unique identifier for test purposes
                fdnt._primary_key_template = test_template

                actual_result = fdnt.get_task_unique_summary()
                self.assertEqual(actual_result, expected_result)

    def test_get_task_description(self):
        trb = TaskReferralBase()
        self.assertIn('Major Configuration Error', trb.get_task_description())

    def test_cmf_description_adapter(self):
        test_cmf = CrashMoveFolder(self.path_to_valid_cmf_des)
        test_cd = task_renderer.cmf_description_adapter(test_cmf)
        self.assertEqual(self.dir_to_valid_cmf_des, test_cd['cmf']['path'])

    def test_render_with_schema_error(self):
        pass
