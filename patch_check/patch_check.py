#/usr/bin/env python3
###############################################################################
# Name         : patch_check.py                                               #
# Author       : Abel Gancsos                                                 #
# Version      : v. 1.0.0.0                                                   #
# Description  : Applies patches to remote Linux servers.                     #
###############################################################################
import sys, os, paramiko, time;

class LinuxPatcher:
    ssh_host=None;ssh_username=None;ssh_password=None;debug=None;ssh_client=None;ignore_list=None;no_restart=None;
    def __init__(self, params=dict()):
        self.ssh_host     = params["-h"] if "-h" in params.keys() else "";
        self.ssh_username = params["-u"] if "-u" in params.keys() else "";
        self.ssh_password = params["-p"] if "-p" in params.keys() else "";
        self.ignore_list  = params["-i"].split(",") if "-i" in params.keys() else ["certbot"];
        self.debug        = True if "--debug" in params.keys() and int(params["--debug"]) > 0 else False;
        self.no_restart   = True if "--no-restart" in params.keys() and int(params["--no-restart"]) > 0 else False;
        self.ssh_client   = paramiko.SSHClient();
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy());
    def remote_command(self, cmd):
        result = "";
        stdin,rsp,err = self.ssh_client.exec_command(cmd, timeout=9999);
        while not rsp.channel.exit_status_ready(): time.sleep(3);
        temp = rsp.channel.recv(1024).decode("utf-8");
        while temp != "":
            result += temp;
            temp = rsp.channel.recv(1024).decode("utf-8");
        return result;
    def invoke(self):
        assert self.ssh_host     != "", "Host cannot be empty...";
        assert self.ssh_username != "", "Username cannot be empty...";
        assert self.ssh_password != "", "Password cannot be empty...";
        self.ssh_client.connect(hostname=self.ssh_host, username=self.ssh_username, password=self.ssh_password);
        platform = self.remote_command("cat /etc/os-release | grep -i PRETTY_ | cut -f 2 -d'='").replace('"', "");
        updates = ();
        if "CentOS" in platform or "RHEL" in platform: updates = self.remote_command("yum check-update").split("\n");
        else: raise Exception("Platform not supported ({0})".format(platform));
        for update in updates:
            comps = [i for i in update.strip().split(" ") if i != ""];
            if len(comps) < 3 or comps[0] == "*": continue;
            if comps[2] in ["@base", "epel", "base", "security"] and len([i for i in self.ignore_list if i in comps[0]]) == 0:
                print("\033[1;34mUpdating: '{0};{1}'\033[m".format(comps[0], comps[1]));
                if not self.debug:
                    if "CentOS" in platform or "RHEL" in platform: rsp = self.remote_command("yum upgrade -y {0}".format(comps[0]));
        if not self.no_restart: self.ssh_client.exec_command("shutdown -r +10 'Shutting down in 10 minutes...'");
        self.ssh_client.close();
        print("\033[1;32mDone!\033[m");
    pass;

if __name__ == "__main__":
    params = dict();
    for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
    session = LinuxPatcher(params);
    session.invoke();
