from jira.client import JIRA
import logging
import pyperclip as pc

def connect_jira(log, jira_server, jira_user, api_token):
    try:
        log.info("Connecting to JIRA: %s" % jira_server)
        jira_options = {'server': jira_server}
        jira = JIRA(options=jira_options, basic_auth=(jira_user, api_token))
        return jira
    except Exception(e):
        log.error("Failed to connect to JIRA: %s" % e)
        return None

def write_task(i):
	return i.key + ' ' + i.fields.summary + ' : ' + i.fields.status.name + '\n'


###
email = ""
api_token = ""
assignee_code = ""
exclude_track = True
###

standup = ""
log = logging.getLogger(__name__)
jira = connect_jira(log, "https://fnba.atlassian.net/", email, api_token)

issues_in_proj = jira.search_issues("assignee = " + assignee_code + " AND statusCategory != Done AND project = SD")

if(exclude_track):
	for i in issues_in_proj:
		if(i.fields.status.name != "Track"):
			standup += write_task(i)
else:
	for i in issues_in_proj:
		standup += write_task(i)

standup = standup[0:len(standup) -1]
print(standup)
pc.copy(standup)
print("Your standup has been copied to your clipboard")
