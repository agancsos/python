#!/usr/bin/env python3
###############################################################################
# Name        : jenkins_remote.py                                             #
# Version     : v. 1.0.0.0                                                    #
# Author      : Abel Gancsos                                                  #
# Description : Practice with Jenkins API.                                    #
###############################################################################
import json, os, sys, requests_html;
from requests.auth import HTTPBasicAuth;
class JenkinsSession:
    base_endpoint=None;username=None;pam=None;session=None;credential=None;
    def __init__(self, params=dict()):
        raw_config         = None;
        if not os.path.exists("{0}/.jenkins.json".format(os.environ["HOME"])):
            with open("{0}/.jenkins.json".format(os.environ["HOME"]), "w") as fh: fh.write('{"username":"", "pam":"", "baseEndpoint":""}');
        with open("{0}/.jenkins.json".format(os.environ["HOME"]), "r") as fh: raw_config = fh.read();
        config             = json.loads(raw_config);
        self.base_endpoint = params["-b"] if "-b" in params.keys() else config["baseEndpoint"];
        self.username      = params["-u"] if "-u" in params.keys() else config["username"];
        self.password      = params["-p"] if "-p" in params.keys() else config["pam"];
        self.session       = requests_html.HTMLSession();
        self.credential    = HTTPBasicAuth(self.username, self.password);
    def trigger_job(self, name, delay_seconds=0):
        rsp = self.session.post("{0}/job/{1}/build?delay={2}sec".format(self.base_endpoint, name, delay_seconds), auth=self.credential, allow_redirects=True);
        return str(rsp.content, "utf-8");
    def get_job_log(self, name, build=None):
        rsp = None;
        if build == None: rsp = self.session.get("{0}/job/{1}/lastBuild/consoleText".format(self.base_endpoint, name), auth=self.credential, allow_redirects=False);
        else: rsp = self.session.get("{0}/job/{1}/{2}/consoleText".format(self.base_endpoint, name, build), auth=self.credential, allow_redirects=False);
        return str(rsp.content, "utf-8");
    def get_last_build(self, name):
        rsp = self.session.get("{0}/job/{1}/lastBuild/api/json".format(self.base_endpoint, name), auth=self.credential, allow_redirects=False);
        return rsp.json();
    def delete_job_run(self, name, build=None):
        rsp = None;
        if build == None: build = self.get_last_build(name)["id"];
        rsp = self.session.post("{0}/job/{1}/{2}/doDelete".format(self.base_endpoint, name, build), auth=self.credential, allow_redirects=False);
        return rsp.status_code == 200;
    def list_jobs(self, path=None, recursive=False):
        result = [];
        rsp = self.session.get("{0}/api/json".format(self.base_endpoint), auth=self.credential, allow_redirects=False);
        for job in rsp.json()["jobs"]:
            if ".folder." in job["_class"]:
                if recursive:
                    temp = self.list_jobs(job["url"], recursive);
                    for j in temp: result.append(j);
            else: result.append(job);
        return result;
    pass;

if __name__ == "__main__":
    params = dict();
    for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
    session   = JenkinsSession(params);
    operation = params["-o"] if "-o" in params.keys() else "trigger";
    job_name  = params["-n"] if "-n" in params.keys() else "";
    build_num = params["--build"] if "--build" in params.keys() else None;

    if operation == "trigger" : print(session.trigger_job("Test1"));
    elif operation == "log"   : print(session.get_job_log("Test1", build_num));
    elif operation == "delete": print(session.delete_job_run("Test1", build_num));
    elif operation == "list"  : print(session.list_jobs());

