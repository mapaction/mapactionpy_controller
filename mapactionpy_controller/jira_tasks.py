# -*- coding: utf-8 -*-
import logging
import netrc
import os
from datetime import datetime

import pytz
from jira import JIRA

import mapactionpy_controller.task_renderer as task_renderer

logger = logging.getLogger(__name__)

# TODO read these in from a config file
jira_hostname = 'mapaction.atlassian.net'
PROJECT_KEY = 'PIPET'
TODO_COLUMN_ID = '10110'

common_task_fields = {
    'project': PROJECT_KEY,
    'issuetype': {'id': '10096'}
}
# 'issuetype': 'automation-human-intervention'


class JiraClient():
    def __init__(self):
        # TODO review the various error types that are possible
        # here and act appropriately:
        # https: // docs.python.org/3.8/library/netrc.html
        #
        # eg FileNotFoundError, NetrcParseError
        try:
            secrets = netrc.netrc()
        except IOError:
            netrc_path = os.path.join(os.environ['USERPROFILE'], '.netrc')
            secrets = netrc.netrc(netrc_path)

        username, account, apikey = secrets.authenticators(jira_hostname)
        self.jira_con = JIRA(options={'server': account}, basic_auth=(username, apikey))

        logger.debug('JIRA Connection. Details = {}'.format(self.jira_con.myself()))

        # Check that the user is actually authenticated
        if not self.jira_con.myself()['emailAddress'] == username:
            raise ValueError('Unable to authenticate with JIRA. Please check details in `.netrc` file.')

    def __del__(self):
        # self.jira_con.close()
        self.jira_con.kill_session()

    def task_handler(self, fail_threshold, msg, step, **kwargs):
        try:
            step_func_name = step.func.__name__
        except AttributeError:
            step_func_name = ''

        logger.debug('JiraClient.task_handler called with status="{}", step.func=`{}` and msg="{}"'.format(
            fail_threshold, step_func_name, msg))

        context_data = task_renderer.extract_context_data(fail_threshold, step_func_name, **kwargs)
        unique_summary = task_renderer.get_task_unique_summary(step_func_name, context_data)

        task_template = task_renderer.get_task_template(step_func_name)
        task_desc = task_renderer.render_task_description(task_template, context_data)

        j_issue = self.search_issue_by_unique_summary(unique_summary)

        if j_issue:
            # Update existing card and maybe move it back into "Doing" column
            self.update_jira_issue(j_issue, task_desc, fail_threshold)
        else:
            if fail_threshold > logging.INFO:
                # Create a new task
                self.create_new_jira_issue(unique_summary, task_desc)

    def search_issue_by_unique_summary(self, search_summary):
        found_issues = self.jira_con.search_issues(
            'project={} AND summary ~ "{}"'.format(PROJECT_KEY, search_summary), maxResults=2)

        if found_issues:
            if len(found_issues) > 1:
                raise ValueError(
                    'More than one JIRA Issue found with the summary "{}". This suggests that additional'
                    ' issues have been raised manualy on the board "{}". Please ensure that there is exactly'
                    ' one issues with this summary, by deleting those which have not been created by the'
                    ' user "{}"'.format(
                        search_summary,
                        PROJECT_KEY,
                        self.jira_con.myself()['emailAddress']
                    )
                )
            else:
                return found_issues[0]
        else:
            return None

    #     some_issues = self.jira_con.search_issues('project=TMIT2 AND map_number ~ "MA0123"')
    #     print(some_issues)

    def create_new_jira_issue(self, unique_summary, task_desc):
        flds = common_task_fields.copy()
        flds['summary'] = unique_summary
        flds['description'] = task_desc

        new_task = self.jira_con.create_issue(fields=flds)
        print(new_task)

    def update_jira_issue(self, j_issue, task_desc, fail_threshold):

        # now_utc = datetime.now()
        # time_stamp = now_utc.isoformat('%Y-%m-%d %H:%M:%S %Z%z')

        now_utc = pytz.utc.localize(datetime.now())
        time_stamp = now_utc.strftime('%Y-%m-%d %H:%M:%S %Z%z')

        if fail_threshold > logging.INFO:
            prev_desc = j_issue.fields.description
            if task_desc != prev_desc:
                j_issue.update(description=task_desc)

            if j_issue.fields.status.id == TODO_COLUMN_ID:
                self.jira_con.add_comment(
                    j_issue.id,
                    'This Issue was still current when MapChef was run at {}'.format(time_stamp))

            else:
                self.jira_con.add_comment(
                    j_issue.id,
                    'This Issue was still current on MapChef run at {}.'
                    ' Moving the issue to the TODO column'.format(time_stamp))
                # do transition
        else:
            if j_issue.fields.status.id == TODO_COLUMN_ID:
                self.jira_con.add_comment(
                    j_issue.id,
                    'This Issue appeared to be resolved when MapChef was run at {}. Please manually'
                    ' check that the outputs are as expected and then close this Issue.'.format(
                        time_stamp))

        # Column name in:
        # jssue.fields.status.id
        # if not in "doing"
        #     move...

    # def search_for_data_task(self):
    #     some_issues = self.jira_con.search_issues('project=TMIT2 AND map_number ~ "MA0123"')
    #     print(some_issues)

    # def create_task_from_template(self):
    #     flds = common_task_fields.copy()

        # flds['layername'] = lyr_name
        # flds['map_number'] = map_num
        # flds['summary'] = 'Task created from template'
        # # flds['description'] = 'Where do we go from here?'
        # # flds['description'] =

        # new_task = self.jira_con.create_issue(fields=flds)
        # print(new_task)
    #     print('new_task.fields = {}'.format(new_task.fields))
    #     cusflds = {}
    #     cusflds['customfield_10076'] = map_num
    #     new_task.update(cusflds)

    #     print(new_task)

    # def update_task(self):
    #     my_issue = self.jira_con.issue('TMIT2-3')
    #     print(my_issue)
    #     print('my_issue.fields = {}'.format(my_issue.fields))
    #     emd = self.jira_con.editmeta('TMIT2-3')
    #     print(emd)

# jira_client = JiraClient()


# testing
if __name__ == "__main__":
    my = JiraClient()
    # my.create_task_from_template()
    my_issue = my.jira_con.issue('TMIT2-4')
    # my_issue.update(description=task_renderer.get_task_description())

    print(my_issue)
    my_desc = my_issue.fields.description

    my_desc = my_desc.encode('ascii', 'backslashreplace')
    # replace(u'\u201c', '"')
    # my_desc.replace(u'\u201d', '"')
    print(u'my_issue.field.description = {}'.format(my_desc))
    print(u'my_issue.field.summary = {}'.format(my_issue.fields.summary))
    # emd = my.jira_con.editmeta('TMIT2-8')
    # print(emd)
    # print(ja.jira_con.myself()['emailAddress'])
    # print(ja.jira_con.projects())
    # update_data_task()
    # create_data_task('my-layer','MA0123')
    # search_for_data_task()
