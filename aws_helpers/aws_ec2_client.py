#!/usr/bin/env python3
###############################################################################
# Name        : aws_ec2_client.py                                             #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helpers for AWS EC2 service.          .                       #
###############################################################################
from aws_client import *;

class AWSEC2Client(AWSClient):
	base_endpoint=None;username=None;password=None;debug=None;force=None;
	def __init__(self, params=dict()):
		AWSClient.__init__(self, params);
		self.debug = True if "--debug" in params.keys() and int(params["--debug"]) > 0 else False;
		self.force = True if "--force" in params.keys() and int(params["--force"]) > 0 else False;
		if not self.debug:
			assert self.base_endpoint != "", "Base endpoint cannot be empty...";
			assert self.username      != "", "Username cannot be empty...";
			assert self.password      != "", "Password cannot be empty...";
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
			if instance["state"] != "stopped" or self.force: self.ec2_stop_instance(instance["instanceId"]);
	pass;

