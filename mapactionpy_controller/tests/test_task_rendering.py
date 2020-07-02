import os
from unittest import TestCase

import mapactionpy_controller.task_renderer as task_renderer
from mapactionpy_controller.name_convention import NamingConvention


class TestTaskRendering(TestCase):

    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def test_render_with_name_result(self):
        dnc_json_path = os.path.join(self.parent_dir, 'example', 'data_naming_convention.json')
        nc = NamingConvention(dnc_json_path)

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
                    '* "ad2" is a recognised value for the clause "datatheme"\n'
                    '* "admn" is a recognised value for the clause "datacat"\n'
                    '* "freetext" is valid for freetext (as is almost anything)\n'
                    '* "lka" is a recognised value for the clause "geoext"\n'
                    '* "pp" is a recognised value for the clause "perm"\n'
                    '* "py" is a recognised value for the clause "geom"\n'
                    '* "s5" is a recognised value for the clause "scale"\n'
                    '* "unocha" is a recognised value for the clause "source"\n'
                ),
                ''
            ],
            'lka_admn_ad77_py_s5_unocha_pp_freetext': [
                'lka_admn_ad77_py_s5_unocha_pp_freetext',
                'parsable but not valid',
                (
                    '* "admn" is a recognised value for the clause "datacat"\n'
                    '* "freetext" is valid for freetext (as is almost anything)\n'
                    '* "lka" is a recognised value for the clause "geoext"\n'
                    '* "pp" is a recognised value for the clause "perm"\n'
                    '* "py" is a recognised value for the clause "geom"\n'
                    '* "s5" is a recognised value for the clause "scale"\n'
                    '* "unocha" is a recognised value for the clause "source"\n'
                ),
                '* "ad77" is not a recognised value for the clause "datatheme"\n'
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
            context_data = task_renderer._name_result_adapter(nr)

            for test_template, expected_result in zip(mustache_tmpls, expected_result_list):
                # do render
                actual_result = task_renderer.render_task_description(test_template, context_data)
                # print('actual_result')
                # print(actual_result)
                # print('expected_result')
                # print(expected_result)
                self.assertEqual(actual_result, expected_result)

    def test_render_with_recipe_layer(self):
        pass

    def test_render_with_schema_error(self):
        pass
