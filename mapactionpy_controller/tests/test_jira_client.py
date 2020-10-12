import os
import six
from unittest import TestCase
# import jira

from mapactionpy_controller import jira_tasks

# works differently for python 2.7 and python 3.x
if six.PY2:
    import mock  # noqa: F401
else:
    from unittest import mock  # noqa: F401


class TestJiraClient(TestCase):
    def setUp(self):
        self.parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.dir_to_valid_cmf_des = os.path.join(self.parent_dir, 'example')
        self.path_to_valid_cmf_des = os.path.join(self.dir_to_valid_cmf_des, 'cmf_description_flat_test.json')

    def test_jira_client_constructor(self):
        # Test without .netrc present
        fail_msg = 'Unable to locate or load suitable `.netrc` file for JIRA integration'
        mock_env = mock.patch.dict(os.environ, {"MAPCHEF_NETRC": "file-that-does-not-exist"})
        mock_env.start()
        print('env-var = {}'.format(os.environ["MAPCHEF_NETRC"]))
        self.call_jira_constrcutor(fail_msg)
        mock_env.stop()

        # Test with .netrc present but without matching machinename
        fail_msg = 'Unable to find details for machine'
        test_failing_netrc_path = os.path.join(self.parent_dir, 'tests', 'testfiles', 'test_netrc_wrong_machine_name')
        print(test_failing_netrc_path)
        mock_env = mock.patch.dict(os.environ, {"MAPCHEF_NETRC": test_failing_netrc_path})
        mock_env.start()
        print('env-var = {}'.format(os.environ["MAPCHEF_NETRC"]))
        self.call_jira_constrcutor(fail_msg)
        mock_env.stop()

        # Test with .netrc present but without correct authentication details
        with mock.patch('mapactionpy_controller.jira_tasks.JIRA'):
            fail_msg = 'Unable to authenticate with JIRA'
            test_failing_netrc_path = os.path.join(self.parent_dir, 'tests', 'testfiles', 'test_netrc_failing_auth')
            print(test_failing_netrc_path)
            mock_env = mock.patch.dict(os.environ, {"MAPCHEF_NETRC": test_failing_netrc_path})
            mock_env.start()
            print('env-var = {}'.format(os.environ["MAPCHEF_NETRC"]))
            self.call_jira_constrcutor(fail_msg)
            mock_env.stop()

    def call_jira_constrcutor(self, fail_msg):
        with self.assertRaises(ValueError) as ve:
            jira_tasks.JiraClient()

        if six.PY2:
            self.assertRegexpMatches(str(ve.exception), fail_msg)
        else:
            self.assertRegex(str(ve.exception), fail_msg)

    @mock.patch('mapactionpy_controller.jira_tasks._check_jira_con')
    @mock.patch('mapactionpy_controller.jira_tasks.JIRA')
    def test_search_issue_by_unique_summary(self, mock_JIRA, mock_check_jira_con):
        test_failing_netrc_path = os.path.join(self.parent_dir, 'tests', 'testfiles', 'test_netrc_failing_auth')
        with mock.patch.dict(os.environ, {"MAPCHEF_NETRC": test_failing_netrc_path}):
            # This overrides JiraClient's own self check that it has a valid connection
            mock_check_jira_con.return_value = None
            jira_client = jira_tasks.JiraClient()

            # test case were extact one task returned
            single_result = ['a']
            jira_client.jira_con.search_issues = mock.MagicMock(return_value=single_result)
            self.assertEqual('a', jira_client.search_issue_by_unique_summary('serach-string'))

            # test case where no tasks returned
            jira_client.jira_con.search_issues = mock.MagicMock(return_value=None)
            self.assertIsNone(jira_client.search_issue_by_unique_summary('serach-string'))
            jira_client.jira_con.search_issues = mock.MagicMock(return_value=[])
            self.assertIsNone(jira_client.search_issue_by_unique_summary('serach-string'))

            # test case where multiple task returned
            multi_result = ['a', 'b']
            jira_client.jira_con.search_issues = mock.MagicMock(return_value=multi_result)

            with self.assertRaises(ValueError) as ve:
                fail_msg = 'More than one JIRA Issue found'
                jira_client.search_issue_by_unique_summary('serach-string')

                if six.PY2:
                    self.assertRegexpMatches(str(ve.exception), fail_msg)
                else:
                    self.assertRegex(str(ve.exception), fail_msg)

    # def test_task_handler(self):
    #     with mock.patch('mapactionpy_controller.jira_tasks.JIRA') as mock_JIRA:
    #         while mock_lp.call_args_list:
    #             call = mock_lp.call_args_list.pop()
    #             # print('call={}'.format('\n'.join([str(c) for c in call])))
    #             # print('\n')
    #             running_msg = call[0][1]
    #             # print('running_msg = {}'.format(running_msg))

    #             # Does running_msg inc a MapID that is a failure:
    #             for f_id in fail_list:
    #                 fail_id = f_id.lower()
    #                 if fail_id in running_msg.lower():
    #                     self.fail('Found unexpected mapID "{}" in running_msg "{}".\n'
    #                             'Only expected mapIDs "{}" with arg "{}"'.format(
    #                                 fail_id, running_msg, should_create, mapid_arg))

    #             for pass_id in should_create:
    #                 if pass_id in running_msg:
    #                     found_map_ids.add(pass_id)

    #         self.assertEqual(should_create_set, found_map_ids)
