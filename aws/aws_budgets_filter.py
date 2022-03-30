#!/usr/bin/env python3
###############################################################################
# Name        : aws_budgets_filter.py                                         #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helps find budgets.                                           #
###############################################################################
import boto3, os, sys, logging;

class AWSService:
    params=None;client=None;debug=None;force=None;logger=None;service=None;region=None;filter_key=None;filter_value=None;
    def __init__(self, params=dict()):
        logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");
        self.logger            = logging.getLogger(__name__);
        self.params            = params;
        self.service           = params["-s"] if "-s" in params.keys() else "budgets";
        self.filter_key        = params["--filter-key"] if "--filter-key" in params.keys() else "BudgetType";
        self.filter_value      = params["--filter-value"] if "--filter-value" in params.keys() else "COST";
        self.region            = params["-r"] if "-r" in params.keys() else "us-east-1";
        self.client            = boto3.client(self.service, self.region);
    def invoke(self):
        account_id = boto3.client("sts").get_caller_identity()["Account"];
        budgets = self.client.describe_budgets(AccountId=account_id);
        for budget in budgets["Budgets"]:
            if budget[self.filter_key] == self.filter_value: self.logger.info(budget);
    pass;

if __name__ == "__main__":
    params = dict();
    for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
    session = AWSService(params);
    session.invoke();
    
