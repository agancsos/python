#!/usr/bin/env python3
###############################################################################
# Name        : git_sync.py                                                   #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helps sync Git repositories cross systems.                    #
###############################################################################
import os, sys, json, logging, yaml, paramiko, base64, socket;
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");
log = logging.getLogger(__name__);

if __name__ == "__main__":
	params               = {};
	for i in range(0, len(sys.argv) - 1):
		params[sys.argv[i]] = sys.argv[i + 1];
	inventory_file       = params.get("-f", "{0}/inventory.yml".format(os.path.dirname(os.path.abspath(__file__))));
	assert os.path.exists(inventory_file), "Inventory file cannot be empty and must exist...";
	ext                  = os.path.splitext(inventory_file)[1];
	hosts                = params.get("-h", "").split(",");
	ttl                  = int(params.get("--ttl", 20));
	inventory            = {};
	failed               = False;
	if any(x == "" for x in hosts): hosts.remove("");
	if ext.lower() == ".json":
		with open(inventory_file, "r") as fh: inventory = json.loads(fh.read());
	elif ext.lower() == ".yml" or ext.lower() == ".yaml":
		with open(inventory_file, "r") as fh: inventory = yaml.load(fh.read());
	else:
		raise Exception("Unsupported inventory file ({0})".format(inventory_file));
	for host in hosts:
		try:
			assert host in inventory["hosts"].keys(), "Host not found in inventory...";
			s = socket.socket();
			s.settimeout(ttl);
			s.connect((host, 22));
			s.close();
			ssh = paramiko.client.SSHClient();
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy());
			ssh.connect(host, username=inventory["hosts"][host]["username"], password=base64.b64decode(inventory["hosts"][host]["pat"].encode()).decode().split(":")[1]);
			_stdin, _stdout, _stderr = ssh.exec_command("find . -name git -maxdepth 3 -type d", timeout=ttl);
			git_base = _stdout.read().decode().strip();
			assert git_base != "", "Failed to find git base directory...";
			_stdin, _stdout, _stderr = ssh.exec_command("ls {0}".format(git_base), timeout=ttl);
			repos = _stdout.read().decode().strip().split("\n");
			for repo in repos:
				_stdin, _stdout, _stderr = ssh.exec_command("git -C '{0}/{1}' pull".format(git_base, repo), timeout=ttl);
				assert _stderr.read().decode().strip() == "", "Failed to pull git ({0})".format(repo);
			ssh.close();
		except Exception as ex:
			failed = True;
			log.warning("\033[33m{0}\033[m".format(ex));
	if not failed:
		log.info("\033[32mSuccess!\033[m");

