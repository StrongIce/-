from jira import JIRA


jira_login = "login"
jira_api_key = "token"
server = {'server': 'http://jira.contoso.com/'} 
jira = JIRA(options=server, basic_auth=(jira_login, jira_api_key))


def open_tickets(jira):        
    tickets_list = list()
    search = jira.search_issues("status IN ('Открыт')", maxResults=900)
    for ticket in search:
        tickets_list.append(str(ticket))
    return tickets_list

tickets_list = open_tickets(jira)
print(tickets_list)

for ticket in tickets_list:
    print(ticket)
    jira.assign_issue(ticket, assignee = 'admin_a')
    jira.transition_issue(ticket,'761')



