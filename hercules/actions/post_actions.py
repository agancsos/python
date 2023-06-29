
def get_syslog(client, cmd=""):
	return client.raw_post_request("cgi-bin/tasks/syslog", params={
		"command": cmd,
		"send": "Send"});

