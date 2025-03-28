from jira.client import JIRA
import logging
import klembord

color_dict = {
	"Track": "black",
	"Specify": "black",
	"Specify Done": "#BDCB4C",
	"Implement": "#2B9B62",
	"Implement Done": "#37797B", 
	"Review": "#FDC030",
	"Review Done": "#CD5937",
	"Ready to validate" : "#B6424C",
	"Validate" : "#B6424C",
	"Validate Done" : "#1E53A3",
	"Done" : "#A5397A"
}

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
	return '<b>' + i.key + ' </b> ' + i.fields.summary + ' : <span style="color: ' + color_dict[i.fields.status.name] + '">' + ("<u><b><i>" + i.fields.status.name + "</i></b></u>" if i.fields.status.name == "Done" else i.fields.status.name) + '</span><br/>\n'


###
email = ""
api_token = ""
assignee_code = ""
exclude_track = True
###

standup = "<html>"
log = logging.getLogger(__name__)
jira = connect_jira(log, "https://fnba.atlassian.net/", email, api_token)

issues_in_proj = jira.search_issues("assignee = " + assignee_code + " AND statusCategory != Done AND project = SD AND status != Backlog")

if(exclude_track):
	for i in issues_in_proj:
		if(i.fields.status.name != "Track"):
			standup+= write_task(i)
else:
	for i in issues_in_proj:
		standup+= write_task(i)

issues_in_proj = jira.search_issues("project = SD AND assignee = " + assignee_code + " AND updateddate >= -2d AND status = DONE AND status != Backlog")

for i in issues_in_proj:
	if(i.fields.status.name != "Track"):
		standup+= write_task(i)

standup = standup[0:len(standup) -1]
standup+= "</html>"
print(standup)
klembord.set_with_rich_text('html', standup)
print("Your standup has been copied to your clipboard")

