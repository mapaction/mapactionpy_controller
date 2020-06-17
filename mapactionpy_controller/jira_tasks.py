import netrc
import os
from jira import JIRA
import logging
from mapactionpy_controller.map_recipe import MapRecipe

logging.basicConfig(level=logging.DEBUG)

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

        # Check that the user is actually authenticated
        if not ja.jira_con.myself()['emailAddress'] == username:
            raise ValueError('Unable to authenticate with JIRA. Please check details in `.netrc` file.')

    def __del__(self):
        self.jira_con.close()

    def task_handler(self, status, msg, step, **kwargs):
        logging.debug('JiraClient.task_handler called with status="{}", step.func=`{}` and msg="{}"'.format(
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

    # def create_data_task(self, lyr_name, map_num):
    #     flds = common_task_fields.copy()

    #     # flds['layername'] = lyr_name
    #     # flds['map_number'] = map_num
    #     flds['summary'] = 'A summary'
    #     flds['description'] = 'Where do we go from here?'
    #     new_task = self.jira_con.create_issue(fields=flds)
    #     print(new_task)
    #     print('new_task.fields = {}'.format(new_task.fields))
    #     cusflds = {}
    #     cusflds['customfield_10076'] = map_num
    #     new_task.update(cusflds)

    #     print(new_task)

    # def update_data_task(self):
    #     my_issue = self.jira_con.issue('TMIT2-3')
    #     print(my_issue)
    #     print('my_issue.fields = {}'.format(my_issue.fields))
    #     emd = self.jira_con.editmeta('TMIT2-3')
    #     print(emd)


# testing
# if __name__ == "__main__":
    # print(ja.jira_con.myself()['emailAddress'])
    # print(ja.jira_con.projects())
    # update_data_task()
    # create_data_task('my-layer','MA0123')
    # search_for_data_task()
