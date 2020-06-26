# -*- coding: utf-8 -*-
import netrc
import os
from jira import JIRA
import logging
from mapactionpy_controller.map_recipe import MapRecipe
import mapactionpy_controller.task_renderer as task_renderer

# logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


# TODO read these in from a config file
jira_hostname = 'mapaction.atlassian.net'
PROJECT_KEY = 'TMIT2'

common_task_fields = {
    'project': PROJECT_KEY,
    'issuetype': 'automation-human-intervention'
}


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
        self.jira_con.close()

    def task_handler(self, status, msg, step, **kwargs):
        logger.debug('JiraClient.task_handler called with status="{}", step.func=`{}` and msg="{}"'.format(
            status, step.func.__name__, msg
        ))
        if kwargs:
            state = kwargs['state']
            if isinstance(state, MapRecipe):
                pass

    # def create_mapping_task(self):
    #     pass

    # def update_mapping_task(self):
    #     pass

    # def search_for_data_task(self):
    #     some_issues = self.jira_con.search_issues('project=TMIT2 AND map_number ~ "MA0123"')
    #     print(some_issues)

    def create_task_from_template(self):
        flds = common_task_fields.copy()

        # flds['layername'] = lyr_name
        # flds['map_number'] = map_num
        flds['summary'] = 'Task created from template'
        # flds['description'] = 'Where do we go from here?'
        # flds['description'] =

        new_task = self.jira_con.create_issue(fields=flds)
        print(new_task)
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
    my_issue = my.jira_con.issue('TMIT2-11')
    my_issue.update(description=task_renderer.get_task_description())

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
