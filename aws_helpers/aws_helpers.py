#!/usr/bin/env python3
###############################################################################
# Name        : aws_helpers.py                                                #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helpers to maintain an AWS environment.                       #
###############################################################################
import os, sys;
from aws_ec2_client import *;

class AWSHelpers:
	operation=None;service=None;client=None;params=None;
	def __init__(self, params=dict()):
		self.params        = params;
		self.operation     = params["-o"] if "-o" in params.keys() else "test";
		self.service       = params["-s"] if "-s" in params.keys() else "ec2";
		assert self.operation != "", "Operation cannot be empty...";
		assert self.service   != "", "Service cannot be empty...";
		if self.service == "ec2": self.client = AWSEC2Client(params);
		else: raise Exception("Invalid service ({0})".format(self.service));
	def invoke(self):
		try:
			if self.operation == "test": pass;
			elif self.operation == "eod": self.client.ec2_eod_instances();
			elif self.operation == "list-ec2":
				for instance in self.client.ec2_get_instances(): 
					self.client.log("{0};{1}".format(instance["instanceId"], instance["state"]), 3);
			elif self.operation == "stop-ec2":
				assert self.params["--id"] != "", "Instance id cannot be empty...";
				self.client.ec2_stop_instance(self.params["--id"],
					True if "--remove" in self.params.keys() and int(self.params["--remove"]) > 0 else False);
			elif self.operation == "create-ec2":
				assert "--name" in self.params.keys() and self.params["--name"] != "", "Instance name cannot be empty...";
				assert "--image" in self.params.keys() and self.params["--image"] != "", "Image name cannot be empty...";
				self.client.ec2_create_instance(self.params["--image"], self.params["--name"]);
			else: raise Exception("Unsupported operation ({0})".format(self.operation));
			print("\033[32;1mDone!\033[m");
		except Exception as ex: print("\033[31;1mException occurred: '{0}'\033[0m".format(ex));

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session       = AWSHelpers(params);
	session.invoke();

