
def get_version(client):
	return client.raw_request("cgi-bin/debug/version_info");
def get_syslog(client, max_lines=5):
	return client.raw_post_request("cgi-bin/tasks/syslog", params={
		"msgcount": max_lines,
		"send": "Send"});
def get_cpu_config(client):
	return client.raw_request("cgi-bin/configure/cpu");
def get_general_registers(client):
	return client.raw_request("cgi-bin/registers/general");
def get_control_registers(client):
	return client.raw_request("cgi-bin/registers/control");
def list_devices(client):
	return client.raw_request("cgi-bin/debug/device/list");

