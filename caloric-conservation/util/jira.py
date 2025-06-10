
from jira.client import JIRA

def connect_jira(log, jira_server, jira_user, api_token):
    try:
        log.info("Connecting to JIRA: %s" % jira_server)
        jira_options = {'server': jira_server}
        jira = JIRA(options=jira_options, basic_auth=(jira_user, api_token))
        return jira
    except Exception(e): 
        log.error("Failed to connect to JIRA: %s" % e)
        return None
