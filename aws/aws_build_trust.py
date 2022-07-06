#!/usr/bin/env python3
###############################################################################
# Name        : aws_build_trust.py                                            #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helps build AWS Trust Relationships between IAM Roles.        #
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
	source_role                = params["--source-role"] if "--source-role" in params.keys() else ""; # ARN
	target_role                = params["--target-role"] if "--target-role" in params.keys() else ""; # ARN
	role_tags                  = json.loads(params["--tags"]) if "--tags" in params.keys() else [];
	if role != "":
		assert account != "", "Account cannot be empty...";
		session                    = aws_session("arn:aws:iam::{0}:role/{1}".format(account, role));
	try:
		assert source_role != "", "Source Role cannot be empty...";
		assert target_role != "", "Target Role cannot be empty...";
		client          = session.client("iam",  region, config=Config(read_timeout=timeout, connect_timeout=timeout));
		all_roles       = client.list_roles()["Roles"];
		if not any(x["Arn"] != target_role for x in all_roles):
			logger.info("Target Role ({0}) does not exist in account.  Creating...".format(target_role));
			client.create_role(RoleName=target_role,
				AssumeRolePolicyDocument="{0}".format({
					"Version": "2012-10-17",
					"Statement": [ {
						"Effect": "Allow",
						"Prinicpal": {
							"AWS": [source_role]
						},
						"Action": "sts:AssumeRole"	
					]},
					"MaxSessionDuration": 43200
				}),
				Tags=tags);
		else:
			logger.info("Found Target Role ({0}).  Scanning for Trust Relationships...".format(target_role));
			role = next(x for x in all_roles if x["Arn"] == target_role);
			for statement in role["AssumeRolePolicyDocument"]["Statement"]:
				if "AWS" not in statement["Principal"].keys(): continue;
				if isinstance(statement["Principal"]["AWS"], list):
					if not any(x == source_role for x in statement["Principal"]["AWS"]):
						statement["Principal"]["AWS"].append(source_role);
						break;
					else:
						logger.info("Trust Relationship between {0} and {1} already exists...".format(source_role, target_role));
						break;
				else:
					if statement["Principal"]["AWS"] == source_role:
						logger.info("Trust Relationship between {0} and {1} already exists...".format(source_role, target_role));
						break;
					else:
						temp_roles = [];
						temp_roles.append(statement["Principal"]["AWS"]);
						temp_roles.append(source_role);
						statement["Principal"]["AWS"] = temp_roles;
						break;
		if not debug:
			pass;
		else: logger.info(role["AssumeRolePolicyDocument"]);
	except Exception as ex: logger.error(ex);

