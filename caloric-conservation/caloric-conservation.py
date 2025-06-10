import logging
import klembord
import requests
import sys

from objects.Dialog import Dialog
from util.jira import connect_jira
from util.color_dict import color_dict
from util.plaid import plaid

from PyQt5.QtWidgets import (
    QDialog, QApplication
)

from cred import email, api_token, assignee_code, server, exclude_track, url

def write_task(i):
	return '<b><a href="' + server + 'browse/' + i.key +'">' + i.key + '</a></b> ' + i.fields.summary + ' : <span style="color: ' + color_dict[i.fields.status.name.lower()] + '">' + ("<u><b><i>" + i.fields.status.name + "</i></b></u>" if i.fields.status.name == "Done" else i.fields.status.name) + '</span><br/>\n'

standup = "<html>"
log = logging.getLogger(__name__)
jira = connect_jira(log, server, email, api_token)

issues_in_proj = jira.search_issues("assignee = " + assignee_code + " AND statusCategory != Done AND project = SD AND status != Backlog")

if(exclude_track):
	for i in issues_in_proj:
		if(i.fields.status.name != "Track"):
			standup+= write_task(i)
else:
	for i in issues_in_proj:
		standup+= write_task(i)

issues_in_proj = jira.search_issues('project = SD AND assignee = ' + assignee_code + ' AND updateddate >= -2d AND status CHANGED TO "Done" AFTER -2d AND status != Backlog')

for i in issues_in_proj:
	if(i.fields.status.name != "Track"):
		standup+= write_task(i)

standup = standup[0:len(standup) -6]
standup+= "</html>"

print(standup)

# Run GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = Dialog(standup)
    if dialog.exec_() == QDialog.Accepted:
        html_edit, include_plaid, plaid_text, add_info_text, copy_to_clipboard, post_in_teams = dialog.get_data()
        
        print(html_edit)
        
        standup = f"{html_edit}{("<br/><br/>" + plaid + ' ' + plaid_text) if (include_plaid and plaid_text != "") else ""}{("<br/><br/>" + add_info_text) if (add_info_text != "") else ""}"
                            
        if(copy_to_clipboard):
            klembord.set_with_rich_text('html', standup)
        
        if(post_in_teams):    
            data_json = {'standup': standup}
            response_json = requests.post(url, json=data_json)
            print(response_json)        
    sys.exit()


