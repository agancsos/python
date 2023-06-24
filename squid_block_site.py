#!/usr/bin/env python3
###############################################################################
# Name        : squid_block_site.py                                           #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helps block sites using a Squid proxy server.                 #
###############################################################################
import os, sys, logging, paramiko, json, base64, requests;
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");
log = logging.getLogger(__name__);

class SquidHelpers:
	def __run_ssh_command__(session, cmd):
		stdin, rst, _stderr = session.exec_command(cmd);
		return rst.read().decode();
	def list_blocked_sites(session, site="", proxy="", proxy_username="", proxy_pat=""):
		if site == "":
			return SquidHelpers.__run_ssh_command__(session, "cat /etc/squid/blocked_sites.txt");
		else:
			return SquidHelpers.__run_ssh_command__(session, "cat /etc/squid/blocked_sites.txt|grep {0}".format(site));
	def block_site(session, site, proxy="", proxy_username="", proxy_pat=""):
		assert site != "", "Site cannot be empty...";
		return SquidHelpers.__run_ssh_command__(session, "echo '{0}' >> /etc/squid/blocked_sites.txt; service squid restart".format(site));
	def ping_site(session, site, proxy, proxy_username, proxy_pat):
		proxy = proxy.replace("https://", "").replace("http://", "");
		assert site != "", "Site cannot be empty...";
		assert proxy != "", "Proxy endpoint cannot be empty...";
		return requests.get(site, verify=False, proxies={
			"http": "http://{0}:{1}@{2}".format(proxy_username, proxy_pat, proxy),
			"https": "http://{0}:{1}@{2}".format(proxy_username, proxy_pat, proxy)
		}).status_code;

if __name__ == "__main__":
	params               = {};
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	squid_server         = params.get("--server", "");
	operation            = params.get("--op", "list_blocked_sites").replace("-", "_");
	site                 = params.get("--site", "");
	proxy_server         = params.get("--proxy", "");
	config_file          = params.get("-f", "{0}/.squid.json".format(os.environ["HOME"]));
	assert os.path.exists(config_file), "Configuration file does not exists ({0})".format(config_file);
	config               = {};
	with open(config_file, "r") as fh: config = json.loads(fh.read());
	try:
		session = paramiko.client.SSHClient()
		session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		session.connect(squid_server, username=config.get("username", ""), password=base64.b64decode(config.get("pat", "").encode()).decode());
		log.info("\033[36m{0}\033[m".format(getattr(SquidHelpers, operation)(session,
			site, proxy_server, config.get("proxyUsername", ""), base64.b64decode(config.get("proxyPAT", "").encode()).decode())));
		session.close();
	except Exception as ex:
		log.warning("\33[33m{0}\033[m".format(ex));

