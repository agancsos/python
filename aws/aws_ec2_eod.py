#!/usr/bin/env python3
###############################################################################
# Name        : aws_ec2_eod.py                                                #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description :                                                               #
###############################################################################
import boto3, os, sys, logging;

class AWSService:
	params=None;client=None;debug=None;force=None;logger=None;service=None;region=None;
	def __init__(self, params=dict()):
		logging.basicConfig(format="%(asctime)s %(levelname)s  %(message)s", level="INFO");
		self.logger            = logging.getLogger(__name__);
		self.params            = params;
		self.ignored_instances = params["--ignored"].split(",") if "--ignored" in params.keys() else list();
		self.service           = params["-s"] if "-s" in params.keys() else "ec2";
		self.region            = params["-r"] if "-r" in params.keys() else "us-east-1";
		self.client            = boto3.client(self.service, self.region);
	def invoke(self):
		instances = self.client.describe_hosts();
		for instance in instances["Hosts"]:
			if instance["State"] != "Terminated" and instance["Name"] not in self.ignored_instances:
				print(instance["InstanceId"]);
				if not self.debug: self.client.terminate_instance(instance["InstanceId"]);
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = AWSService(params);
	session.invoke();

