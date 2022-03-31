# -*- coding: utf-8 -*-
import logging
import netrc
import os
from datetime import datetime

import pytz
#from jira import JIRA

from mapactionpy_controller.task_renderer import TaskReferralBase

logger = logging.getLogger(__name__)


def _get_secrets_from_netrc():
    """
    If `MAPCHEF_NETRC` exists as an environment varible then that value will be used as the
    absolute path to the .netrc file.
    If `MAPCHEF_NETRC` does not exists as an environment varible, then the 'HOME' and 'USERPROFILE'
    locations will be searched for `.netrc` files.
    """
    possible_netrc_locations = [os.path.join(os.environ[envar], '.netrc')
                                for envar in ['HOME', 'USERPROFILE'] if envar in os.environ]

    if 'MAPCHEF_NETRC' in os.environ:
        possible_netrc_locations = [os.environ['MAPCHEF_NETRC']]

    secrets = None
    for netrc_path in possible_netrc_locations:
        try:
            secrets = netrc.netrc(netrc_path)
        except IOError:
            pass

    return secrets


def _check_jira_con(jira_con, username):
    # Check that the user is actually authenticated
    if not jira_con.myself()['emailAddress'] == username:
        err_msg = 'JIRA Connection. Unable to authenticate with JIRA. Please check details in `.netrc` file.'
        logger.error(err_msg)
        raise ValueError(err_msg)


class JiraClient():
    jira_con = None
    board_details = None

    def __init__(self):
        self._get_jira_board_details()
        secrets = _get_secrets_from_netrc()

        if not secrets:
            err_msg = 'Unable to locate or load suitable `.netrc` file for JIRA integration'
            logger.error(err_msg)
            raise ValueError(err_msg)

        try:
            username, account, apikey = secrets.authenticators(self.jira_hostname)
        except TypeError:
            err_msg = 'JIRA Connection. Unable to find details for machine "{}" `.netrc` file.'.format(
                self.jira_hostname)
            logger.error(err_msg)
            raise ValueError(err_msg)

        self.jira_con = JIRA(options={'server': account}, basic_auth=(username, apikey))
        _check_jira_con(self.jira_con, username)
        logger.debug('JIRA Connection. Details = {}'.format(self.jira_con.myself()))

    def _get_jira_board_details(self):
        # TODO read these in from a config file
        self.jira_hostname = 'mapaction.atlassian.net'
        self.project_key = 'PIPET'
        # The target column should be were the column where new issues are created
        self.target_column = '10110'
        self.common_task_fields = {
            'project': self.project_key,
            'issuetype': {'id': '10235'}
        }

    def __del__(self):
        try:
            self.jira_con.kill_session()
        except (TypeError, AttributeError):
            pass

    def task_handler(self, fail_threshold, msg, task_referal=None):
        logger.debug('JiraClient.task_handler called with status="{}", and msg="{}"'.format(
            fail_threshold, msg))

        assured_referal = self.ensure_task_referal_type(task_referal, msg, fail_threshold)

        if not assured_referal:
            logger.debug('JiraClient.task_handler; `None` value passed for task_referal parameter. Nothing to handle.')
            return

        unique_summary = assured_referal.get_task_unique_summary()
        task_desc = assured_referal.get_task_description()
        op_id = assured_referal.get_operation_id()

        j_issue = self.search_issue_by_unique_summary(unique_summary, op_id)

        if j_issue:
            # Update existing card and maybe move it back into "Doing" column
            self.update_jira_issue(j_issue, task_desc, fail_threshold)
        else:
            if fail_threshold > logging.INFO:
                # Create a new task
                self.create_new_jira_issue(unique_summary, task_desc, op_id)

    def ensure_task_referal_type(self, task_referal, msg, fail_threshold):
        """
        Check whether or not the `task_referal` is an instance of TaskReferralBase object. If it is the object is
        then it is returned unchanged. If not then an generic TaskReferralBase will be created and returned. The
        value of `str(task_referal)` will be used.

        @param task_referal: An object that may or may not be a TaskReferralBase object.
        @returns: If the `task_referal` param is an instance of TaskReferralBase object, then `task_referal` is
                  returned.
                  If `task_referal` param is NOT an instance of TaskReferralBase AND fail_threshold is logging.ERROR
                  then a new TaskReferralBase object is created (using `msg` and `str(task_referal)` for context).
                  Else `None` is returned.
        """
        if isinstance(task_referal, TaskReferralBase):
            logger.debug('JiraClient.ensure_task_referal_type found a TaskReferralBase object')
            return task_referal

        if task_referal and (fail_threshold > logging.WARNING):
            logger.debug('JiraClient.ensure_task_referal_type created a new TaskReferralBase object')
            return TaskReferralBase(None, msg=msg, other=str(task_referal))

        logger.debug('JiraClient.ensure_task_referal_type passed "{}" but returned `None`'.format(
            str(task_referal)
        ))
        return None

    def search_issue_by_unique_summary(self, search_summary, op_id):
        # Default if `op_id` is None
        jql_op_id = 'operational_id is EMPTY'
        if op_id:
            jql_op_id = 'operational_id ~ "{}"'.format(op_id)

        jql_str = 'project={} AND {} AND summary ~ "{}"'.format(self.project_key, jql_op_id, search_summary)
        found_issues = self.jira_con.search_issues(jql_str, maxResults=2)

        if found_issues:
            if len(found_issues) > 1:
                raise ValueError(
                    'More than one JIRA Issue found with the summary "{}". This suggests that additional'
                    ' issues have been raised manualy on the board "{}". Please ensure that there is exactly'
                    ' one issues with this summary, by deleting those which have not been created by the'
                    ' user "{}"'.format(
                        search_summary,
                        self.project_key,
                        self.jira_con.myself()['emailAddress']
                    )
                )
            else:
                return found_issues[0]
        else:
            return None

    def create_new_jira_issue(self, unique_summary, task_desc, op_id):
        flds = self.common_task_fields.copy()
        flds['summary'] = unique_summary
        flds['description'] = task_desc
        # This is the JIRA API's field ID for operational_id. To work this out execute:
        # ```
        # a = j.jira_con.createmeta(projectKeys=['PIPET'], issuetypeIds=[10235], expand='projects.issuetypes.fields')
        # print(a)
        # ```
        # Then search the output for your custom field name. Doubtless there is a programmatic way to do this.
        flds['customfield_10234'] = op_id

        new_task = self.jira_con.create_issue(fields=flds)
        # new_task.update(fields={'operational_id':op_id})
        # new_task.update(operational_id=op_id)
        print(new_task)
        # print('desc', new_task.fields.description)
        # print('opid', new_task.fields.operational_id)
        # for f in new_task.fields:
        #     print('field itr', f)

    def update_jira_issue(self, j_issue, task_desc, fail_threshold):
        now_utc = pytz.utc.localize(datetime.now())
        time_stamp = now_utc.strftime('%Y-%m-%d %H:%M:%S %Z%z')

        # prev_desc =
        if task_desc != j_issue.fields.description:
            j_issue.update(description=task_desc)

        if fail_threshold > logging.INFO:
            self.jira_con.add_comment(
                j_issue.id,
                'This Issue was still current when MapChef was run at {}'.format(time_stamp))

        # if (fail_threshold <= logging.INFO)   eg *is not* an warning or an error
        # and (j_issue.fields.status.id == self.target_column):  eg and still in the todo column
        # and (j_issue.fields.status.id == self.target_column):  eg and still in the todo column
        # then add comment (and possibly automatically close).
        # self.jira_con.add_comment(
        #     j_issue.id,
        #     'This Issue appeared to be resolved when MapChef was run at {}. Please manually'
        #     ' check that the outputs are as expected and then close this Issue.'.format(
        #         time_stamp))

        # if (fail_threshold > logging.INFO)   eg *IS* an warning or an error
        # and (not j_issue.fields.status.id == self.target_column):  # Not in the todo column
        # then it may be necessary to re-open the ticket.
        # self.jira_con.transition_issue(
        #     j_issue.id,
        #     comment='This Issue was still current on MapChef run at {}.'
        #     ' Moving the issue to the DOING column'.format(time_stamp))
        # )
