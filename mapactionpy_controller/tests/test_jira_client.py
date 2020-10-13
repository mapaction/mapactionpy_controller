import os
import logging
import six
from unittest import TestCase

from mapactionpy_controller import jira_tasks
from mapactionpy_controller.task_renderer import TaskReferralBase

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
            mock_env = mock.patch.dict(os.environ, {"MAPCHEF_NETRC": test_failing_netrc_path})
            mock_env.start()
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

    @mock.patch('mapactionpy_controller.jira_tasks._check_jira_con')
    @mock.patch('mapactionpy_controller.jira_tasks.JIRA')
    def test_task_handler(self, mock_JIRA, mock_check_jira_con):
        test_failing_netrc_path = os.path.join(self.parent_dir, 'tests', 'testfiles', 'test_netrc_failing_auth')
        with mock.patch.dict(os.environ, {"MAPCHEF_NETRC": test_failing_netrc_path}):
            # This overrides JiraClient's own self check that it has a valid connection
            mock_check_jira_con.return_value = None
            jira_client = jira_tasks.JiraClient()

            # Case 1)
            # where there is no task object, therefore should pass sliently
            jira_client.jira_con.search_issues = mock.MagicMock(return_value=None)
            # This isn't a particularly diagnostic test, but in this case litterialy nothing happens
            self.assertIsNone(jira_client.task_handler(logging.ERROR, 'test-case', None))

            # Case 2)
            # where there is no existing issue for the task, therefore a new JIRA issue should be created
            jira_client.jira_con.search_issues = mock.MagicMock(return_value=None)
            with mock.patch.object(jira_client.jira_con, 'create_issue', return_value=None) as mock_method:
                test_task = TaskReferralBase()
                jira_client.task_handler(logging.ERROR, 'test-case', test_task)

            # assert that jira_client.create_new_jira_issue is called once
            mock_method.assert_called_once()

            # Case 3)
            # where there was an existing *open* task, which is in the correct column, that requires commenting on.
            test_task = TaskReferralBase()

            mock_issue = mock.Mock(name='mock_issue')
            mock_issue.id = "123"  # issue ID
            mock_issue.fields.summary = test_task.get_task_unique_summary()
            mock_issue.fields.description = test_task.get_task_description()
            mock_issue.fields.status.id = jira_client.target_column

            jira_client.jira_con.search_issues = mock.MagicMock(return_value=[mock_issue])
            with mock.patch.object(jira_client.jira_con, 'add_comment', return_value=None) as mock_add_comment_method:
                with mock.patch.object(jira_client.jira_con, 'update', return_value=None) as mock_update_method:
                    jira_client.task_handler(logging.ERROR, 'test-case', test_task)

            mock_update_method.assert_not_called()
            mock_add_comment_method.assert_called_once()
            comment_arg = mock_add_comment_method.call_args[0][1]

            target_msg = 'This Issue was still current'
            if six.PY2:
                self.assertRegexpMatches(comment_arg, target_msg)
            else:
                self.assertRegex(comment_arg, target_msg)

            # Case 4)
            # where the issue description requires updating
            test_task = TaskReferralBase()

            mock_issue = mock.Mock(name='mock_issue')
            mock_issue.id = "123"  # issue ID
            mock_issue.fields.summary = test_task.get_task_unique_summary()
            # Gaurentee that the description for the issue is different to the task.
            mock_issue.fields.description = 'description is different. {}'.format(test_task.get_task_description())
            mock_issue.fields.status.id = jira_client.target_column

            jira_client.jira_con.search_issues = mock.MagicMock(return_value=[mock_issue])
            with mock.patch.object(jira_client.jira_con, 'add_comment', return_value=None) as mock_add_comment_method:
                with mock.patch.object(mock_issue, 'update', return_value=None) as mock_update_method:
                    jira_client.task_handler(logging.ERROR, 'test-case', test_task)

            mock_update_method.assert_called_once()
            mock_add_comment_method.assert_called_once()

            # Case 5)
            # where there was an existing *closed* task, that requires *re-opening* and commenting on.

            # Case 6)
            # where there is an no-longer relevant *open* task, that requires (possibly closing) an commenting on
