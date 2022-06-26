#!/usr/bin/env python3
###############################################################################
# Name        : aws_ebs_tools.py                                              #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description :                                                               #
###############################################################################
import boto3, os, sys, logging;

class AWSService:
	params=None;client=None;debug=None;force=None;logger=None;service=None;region=None;operation=None;volume_name=None;
	def __init__(self, params=dict()):
		logging.basicConfig(format="%(asctime)s %(levelname)s  %(message)s", level="INFO");
		self.logger            = logging.getLogger(__name__);
		self.params            = params;
		self.ignored_instances = params["--ignored"].split(",") if "--ignored" in params.keys() else list();
		self.service           = params["-s"] if "-s" in params.keys() else "ec2";
		self.region            = params["-r"] if "-r" in params.keys() else "us-east-1";
		self.client            = boto3.client(self.service, self.region);
		self.operation         = params["--op"] if "--op" in params.keys() else "disable-dot";
		self.volume_name       = params["-n"].split(",") if "-n" in params.keys() else ["*"];
		self.debug             = False if "--debug" in params.keys() and int(params["--debug"]) < 1 else True;
	def invoke(self):
		if self.operation == "disable-dot":
			volumes = self.client.describe_volumes()["Volumes"];
			for volume in volumes:
				if volume["VolumeId"] not in self.volume_name and "*" not in self.volume_name: continue;
				self.logger.info("Performing {0} on {1}".format(self.operation, volume["VolumeId"]));
				if not self.debug:
					for attach in volume["Attachments"]:
						self.client.modify_volume_attribute("blockDeviceMapping", ["{0}=0".format(attach["Device"]));
		else:
			raise Exception("Invalid operation ({0})".formaat(self.operation));
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = AWSService(params);
	session.invoke();

