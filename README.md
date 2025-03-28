# caloric-conservation
you don't even have to standup anymore

## Setup
- install python https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe
- run `pip install jira`
- run `pip install logging`
- run `pip install klembord`

## Jira
- Navigate to https://id.atlassian.com/manage-profile/security/api-tokens
- Click Create API token. Copy API Token.
- Navigate to https://fnba.atlassian.net/issues/?jql=assignee%20%3D%206357078cb7b39379d71f38ea
	- This will bring you to a Jira filter that displays SD tasks where I (Hans) am listed as the assignee. In the input box at the top of the page, delete my name, enter your own and click on your name from the dropdown that appears. 
	- Put your cursor inside of the input, and press `ctrl + a, ctrl + c`. This will copy your assignee code. Paste it elsewhere, and copy only the assignee code.

## Python
- Open `standup.py`
- Set email as your fnba email (`firstName.lastName@fnba.com`)
- set api_token to your newly created api token
- set assignee_code to the assignee code that you copied above.
- Optionally, toggle exclude_track to `false` if you would like to include Tracked tasks in your standup.

## Run
- Finally, run the file from Powershell  `python standup.py`
- Optionally, right click on the .py file in your file explorer, and click `create shortcut` to create a clickable image to place on your desktop.
- Your standup will be copied to your clipboard automatically.
