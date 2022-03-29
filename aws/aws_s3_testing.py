#!/usr/bin/env python3
###############################################################################
# Name        : aws_s3_testing.py                                             #
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
		self.service           = params["-s"] if "-s" in params.keys() else "s3";
		self.region            = params["-r"] if "-r" in params.keys() else "us-east-1";
		self.client            = boto3.client(self.service, self.region);
	def invoke(self):
		buckets = self.client.list_buckets();
		for bucket in buckets["Buckets"]:
			children = self.client.list_objects(Bucket=bucket["Name"])["Contents"];
			bucket_size = sum(child["Size"] for child in children);
			if (bucket_size / 1024) > 1023: self.logger.warning("! {0}: {1}mb".format(bucket["Name"], bucket_size / 1024));
			else: self.logger.info("{0}: {1}mb".format(bucket["Name"], bucket_size / 1024));
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = AWSService(params);
	session.invoke();

