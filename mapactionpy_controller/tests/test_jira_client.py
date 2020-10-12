import os
import six
from unittest import TestCase
# import jira

from mapactionpy_controller.jira_tasks import JiraClient

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
            JiraClient()

        if six.PY2:
            self.assertRegexpMatches(str(ve.exception), fail_msg)
        else:
            self.assertRegex(str(ve.exception), fail_msg)
