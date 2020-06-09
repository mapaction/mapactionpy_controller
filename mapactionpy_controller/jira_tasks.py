import netrc
import os
from jira import JIRA

JIRA_URL = 'https://mapaction.atlassian.net'
PROJECT_KEY = 'TMIT2'

try:
    secrets = netrc.netrc()
except IOError:
    netrc_path = os.path.join(os.environ['USERPROFILE'], '.netrc')
    secrets = netrc.netrc(netrc_path)

username, account, apikey = secrets.authenticators('mapaction.atlassian.net')
print(secrets)
print(username, account, apikey)

ma_jira = JIRA(options={'server': account}, basic_auth=(username, apikey))

# ma_jira = JIRA(JIRA_URL)




common_fields = {
    'project': PROJECT_KEY,
    'issuetype': 'automation-human-intervention'
}
#    'opid': '2020test01'



def create_mapping_task():
    pass


def update_mapping_task():
    pass


def search_for_data_task():
    some_issues = ma_jira.search_issues('project=TMIT2 AND map_number ~ "MA0123"')
    print (some_issues)


def create_data_task(lyr_name, map_num):
    flds = common_fields.copy()

    # flds['layername'] = lyr_name
    # flds['map_number'] = map_num
    flds['summary'] = 'A summary'
    flds['description'] = 'Where do we go from here?'
    new_task = ma_jira.create_issue(fields=flds)
    print (new_task)
    print('new_task.fields = {}'.format(new_task.fields))
    cusflds = {}
    cusflds['customfield_10076'] = map_num
    new_task.update(cusflds)

    print (new_task)

def update_data_task():
    my_issue = ma_jira.issue('TMIT2-3')
    print (my_issue)
    print('my_issue.fields = {}'.format(my_issue.fields))
    emd = ma_jira.editmeta('TMIT2-3')
    print(emd)

if __name__ == "__main__":
    # print(ma_jira.client_info())
    print(ma_jira.myself()['emailAddress'])
    # print(ma_jira.projects())
    # update_data_task()
    # create_data_task('my-layer','MA0123')
    search_for_data_task()
