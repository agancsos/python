#!/usr/bin/env python3
###############################################################################
# Name        : aws_helpers.py                                                #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helpers to maintain an AWS environment.                       #
###############################################################################
import os, sys, requests_html, datetime, base64, hmac, hashlib, urllib.parse;

class AWSHelpers:
	base_endpoint=None;username=None;password=None;client=None;debug=None;
	def __init__(self, params=dict()):
		self.base_endpoint     = params["-b"] if "-b" in params.keys() else "https://ec2.us-east-2.amazonaws.com";
		self.username          = params["-u"] if "-u" in params.keys() else "";
		self.password          = params["-p"] if "-p" in params.keys() else "";
		self.client            = requests_html.HTMLSession(verify=True);
		self.debug = True if "--debug" in params.keys() and int(params["--debug"]) > 0 else False;
		if not self.debug:
			assert self.base_endpoint != "", "Base endpoint cannot be empty...";
			assert self.username      != "", "Username cannot be empty...";
			assert self.password      != "", "Password cannot be empty...";
	def sign(self, key, msg): return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
	def generate_signature(self, service, timestamp, region="us-east-2"):
		return self.sign(self.sign(self.sign(self.sign("AWS4{0}".format(self.password).encode("utf-8"), timestamp.strftime("%Y%m%d")), region), service), "aws4_request");
	def invoke_req(self, method, service, region, action, args=None):
		timestamp = datetime.datetime.utcnow();
		a = urllib.parse.urlparse("{0}/?Action={1}{2}&Version=2016-11-15".format(self.base_endpoint, action, "&{0}".format(args) if args != None else ""));
		ca_uri = a.path; ca_query = a.query;
		if method == "GET": payload = hashlib.sha256(('').encode("utf-8")).hexdigest();
		ca_headers = "host:{0}\nx-amz-date:{1}\n".format(a.hostname, timestamp.strftime("%Y%m%dT%H%M%SZ"));
		ca_request = "{0}\n{1}\n{2}\n{3}\nhost;x-amz-date\n{4}".format(method, ca_uri, ca_query, ca_headers, payload);
		scope = "{0}/{1}/{2}/aws4_request".format(timestamp.strftime("%Y%m%d"), region, service);
		ca_string = "AWS4-HMAC-SHA256\n{0}\n{1}\n{2}".format(timestamp.strftime("%Y%m%dT%H%M%SZ"), scope, hashlib.sha256(ca_request.encode("utf-8")).hexdigest());
		signing_key = self.generate_signature(service, timestamp, region);
		signature = hmac.new(signing_key, ca_string.encode("utf-8"), hashlib.sha256).hexdigest();
		headers = {
			"X-AMZ-DATE":timestamp.strftime("%Y%m%dT%H%M%SZ"),
			"Authorization":"AWS4-HMAC-SHA256 Credential={0}/{1}, SignedHeaders=host;x-amz-date, Signature={2}".format(self.username, scope, signature)};
		if method == "GET": return self.client.get("{0}/?Action={1}{2}&Version=2016-11-15".format(self.base_endpoint, action, "&{0}".format(args) if args != None else ""), headers=headers);
	def log(self, msg, level=3):
		if level == 1: print("\033[31;1m{0} ERR   {1}\033[0m".format(datetime.datetime.now(), msg));
		elif level == 2: print("\033[35;1m{0} WARN  {1}\033[0m".format(datetime.datetime.now(), msg));
		elif level == 3: print("\033[33;1m{0} INFO  {1}\033[0m".format(datetime.datetime.now(), msg)); 
		elif level == 4: print("\033[34;1m{0} VERB  {1}\033[0m".format(datetime.datetime.now(), msg));
		else: print("{0} DEBUG {1}".format(datetime.datetime.now(), msg));
	def ec2_get_instances(self):
		rsp = self.invoke_req("GET", "ec2", "us-east-2", "DescribeHosts", None);
		print(rsp.content.decode("utf-8"));
		return [];
	def ec2_stop_instance(self, instance, remove=False):
		if self.debug: return;
	def ec2_create_instance(self, image, name):
		if self.debug: return;
	def ec2_eod_instances(self):
		for instance in self.ec2_get_instances():
			if self.debug: self.log("{0};{1}".format(instance["instanceId"], instance["state"]), 5);
			if not self.debug and instance["state"] != "stopped": ec2_stop_instance(instance["instanceId"]);
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session       = AWSHelpers(params);
	operation     = params["-o"] if "-o" in params.keys() else "test";
	assert operation != "", "Operation cannot be empty...";

	## Invoke handlers
	try:
		if operation == "test": pass;
		elif operation == "eod": session.ec2_eod_instances();
		elif operation == "list-ec2":
			for instance in session.ec2_get_instances(): session.log("{0};{1}".format(instance["instanceId"], instance["state"]), 3);
		elif operation == "stop-ec2":
			assert params["--id"] != "", "Instance id cannot be empty...";
			session.ec2_stop_instance(params["--id"], True if "--remove" in params.keys() and int(params["--remove"]) > 0 else False);
		elif operation == "create-ec2":
			assert "--name" in params.keys() and params["--name"] != "", "Instance name cannot be empty...";
			assert "--image" in params.keys() and params["--image"] != "", "Image name cannot be empty...";
			session.ec2_create_instance(params["--image"], params["--name"]);
		else: raise Exception("Unsupported operation ({0})".format(operation));
		print("\033[32;1mDone!\033[m");
	except Exception as ex: print("\033[31;1mException occurred: '{0}'\033[0m".format(ex));
	
