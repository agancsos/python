#!/usr/bin/env python3
###############################################################################
# Name        : aws_update_policy.py                                          #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helps ensure that permissions exist in an AWS IAM Policy.     #
###############################################################################
import os, sys, logging, json, boto3;
sys.path.append(os.path.dirname(__file__));
from aws_helpers import aws_session, get_account;
from botocore.config import Config
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	logger                     = logging.getLogger(__file__)
	account                    = params["--account"] if "--account" in params.keys() else get_account(boto3.Session());
	role                       = params["--role"] if "--role" in params.keys() else "";
	region                     = params["--region"] if "--region" in params.keys() else "us-east-1";
	timeout                    = int(params["--ttl"]) if "--ttl" in params.keys() else 30;
	session                    = boto3.Session();
	debug                      = False if "--debug" in params.keys() and int(params["--debug"]) < 1 else True;
	policy_name                = params["--policy"] if "--policy" in params.keys() else "";
	permissions                = json.loads(params["--perms"]) if "--perm" in params.keys() else {}; # {"<permission>": "<resource>"}
	if role != "":
		assert account != "", "Account cannot be empty...";
		session                    = aws_session("arn:aws:iam::{0}:role/{1}".format(account, role));
	try:
		assert policy_name != "", "Policy name cannot be empty...";
		client          = session.client("iam",  region, config=Config(read_timeout=timeout, connect_timeout=timeout));
		policies        = client.list_policies()["Policies"];
		assert any(x["PolicyName"] == policy_name for x in policies), "Policy ({0}) does not exist...".format(policy_name);
		policy          = next(x for x in policies if x["PolicyName"] == policy_name);
		full_policy     = client.get_policy(PolicyArn=policy["Arn"]);
		policy_versions = client.list_policy_versions(PolicyArn=policy["Arn"])["Versions"];
		latest_version  = next(x for x in policy_versions);
		latest_version  = client.get_policy_version(VersionId=latest_version["VersionId"], PolicyArn=policy["Arn"]);
		statements      = latest_version["PolicyVersion"]["Document"]["Statement"];
		for k, v in permissions.items():
			logger.info("Checking for: {0}; {1}".format(k, v));
			found = False;
			for p in statements:
				if isinstance(p["Action"], list):
					if not any(x == k for x in p["Action"]):
						if p["Resource"] == v:
							found = True;
							logger.info("Adding {0} to actions...".format(k));
							p["Action"].append(k);
				else:
					if p["Action"] != k and v == p["Resource"]:
						found = True;
						temp_actions = [];
						temp_actions.append(p["Action"]);
						temp_actions.append(k);
						p["Action"] = temp_actions;
			if not found:
				logger.info("Permission ({0}) not found for matching resource {1}.  Adding new statement to policy...".format(k, v));
				statements.append({"Effect": "Allow", "Action": [k], "Resource": v});
		if not debug:
			client.update_policy(PolicyId=full_policy["PolicyId"], Content="{0}".format(latest_version["PolicyVersion"]["Document"]));
		else: logger.info(latest_version["PolicyVersion"]["Document"]);
	except Exception as ex: logger.error(ex);

