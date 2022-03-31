#!/usr/bin/env python3
###############################################################################
# Name        : aws_cloudwatch_filter.py                                      #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helps find CloudWatch alarms.                                 #
###############################################################################
import boto3, os, sys, logging;

class AWSService:
	params=None;client=None;debug=None;force=None;logger=None;service=None;region=None;filter_key=None;filter_value=None;
	def __init__(self, params=dict()):
		logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");
		self.logger            = logging.getLogger(__name__);
		self.params            = params;
		self.service           = params["-s"] if "-s" in params.keys() else "cloudwatch";
		self.filter_key        = params["--filter-key"] if "--filter-key" in params.keys() else "AlarmType";
		self.filter_value      = params["--filter-value"] if "--filter-value" in params.keys() else "*";
		self.region            = params["-r"] if "-r" in params.keys() else "us-east-1";
		self.client            = boto3.client(self.service, self.region);
	def invoke(self):
		alarms = self.client.describe_alarm_history();
		if len(alarms["AlarmHistoryItems"]) == 0: self.logger.info("No data to display...");
		else:
			for alarm in alarms["AlarmHistoryItems"]:
				if self.filter_value == "*" or self.filter_value in alarm[self.filter_key]: self.logger.info(alarm);
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = AWSService(params);
	session.invoke();

