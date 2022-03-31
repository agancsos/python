#!/usr/bin/env python3
###############################################################################
# Name        : aws_budgets_tools.py                                          #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helps find budgets.                                           #
###############################################################################
import boto3, os, sys, logging, datetime;

class AWSService:
	params=None;client=None;debug=None;force=None;logger=None;service=None;region=None;filter_key=None;filter_value=None;report=None;
	def __init__(self, params=dict()):
		logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");
		self.logger            = logging.getLogger(__name__);
		self.params            = params;
		self.service           = params["-s"] if "-s" in params.keys() else "budgets";
		self.filter_key        = params["--filter-key"] if "--filter-key" in params.keys() else "BudgetType";
		self.filter_value      = params["--filter-value"] if "--filter-value" in params.keys() else "COST";
		self.region            = params["-r"] if "-r" in params.keys() else "us-east-1";
		self.report            = params["--report"].lower() if "--report" in params.keys() else "filter";
		self.client            = boto3.client(self.service, self.region);
	def invoke(self):
		assert self.report != "", "Report name cannot be blank...";
		account_id = boto3.client("sts").get_caller_identity()["Account"];
		if self.report == "filter":
			budgets = self.client.describe_budgets(AccountId=account_id);
			for budget in budgets["Budgets"]:
				if budget[self.filter_key] == self.filter_value: self.logger.info(budget);
		elif self.report == "bill-by-service":
			self.client = boto3.client("ce");
			end_date   = datetime.datetime.utcnow().strftime("%Y-%m-%d");
			start_date = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime("%Y-%m-%d");
			billing = self.client.get_cost_and_usage(TimePeriod={"Start":start_date, "End":end_date},
				GroupBy=[{"Type":"DIMENSION","Key":"SERVICE"}],
				Granularity="MONTHLY",
				Metrics=["BLENDED_COST", "UNBLENDED_COST", "USAGE_QUANTITY"]);
			if len(billing["ResultsByTime"]) < 1: self.logger.info("No data to display...");
			else:
				for cost in billing["ResultsByTime"][0]["Groups"]:
					self.logger.info("{0}; ${1}; ${2}; {3}".format(cost["Keys"][0], cost["Metrics"]["BlendedCost"]["Amount"], cost["Metrics"]["UnblendedCost"]["Amount"], cost["Metrics"]["UsageQuantity"]["Amount"]));
		else: raise Exception("Invalid report ({0})".format(self.report));
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = AWSService(params);
	session.invoke();

