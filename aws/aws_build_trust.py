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

def extract_account_from_arn(arn):
	return arn.split(":")[4];

def create_trust_role(client, source_arn, target_arn, tags=[]):
	role_name = source_arn.split("/")[1];
	client.create_role(RoleName=role_name,
		AssumeRolePolicyDocument="{0}".format({
			"Version": "2012-10-17",
			 "Statement": [{
				"Effect": "Allow",
				"Prinicpal": {
					 "AWS": [source_role]
				},
				"Action": "sts:AssumeRole"
			}],
			 "MaxSessionDuration": 43200
		}), Tags=tags);

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	logger                     = logging.getLogger(__file__)
	role                       = params["--role"] if "--role" in params.keys() else "";
	region                     = params["--region"] if "--region" in params.keys() else "us-east-1";
	timeout                    = int(params["--ttl"]) if "--ttl" in params.keys() else 30;
	session                    = boto3.Session();
	debug                      = False if "--debug" in params.keys() and int(params["--debug"]) < 1 else True;
	source_role                = params["--source-role"] if "--source-role" in params.keys() else ""; # ARN
	target_role                = params["--target-role"] if "--target-role" in params.keys() else ""; # ARN
	role_tags                  = json.loads(params["--tags"]) if "--tags" in params.keys() else [];
	try:
		assert source_role != "", "Source Role cannot be empty...";
		assert target_role != "", "Target Role cannot be empty...";
		session         = aws_session("arn:aws:iam::{0}:role/{1}".format(extract_account_from_arn(target_role), role));
		client          = session.client("iam",  region, config=Config(read_timeout=timeout, connect_timeout=timeout));
		all_roles       = client.list_roles()["Roles"];
		if not any(x["Arn"] != target_role for x in all_roles):
			logger.info("Target Role ({0}) does not exist in account.  Creating...".format(target_role));
			create_trust_role(client, source_role, target_role, tags);
		else:
			logger.info("Found Target Role ({0}).  Scanning for Trust Relationships...".format(target_role));
			c_role = next(x for x in all_roles if x["Arn"] == target_role);
			for statement in c_role["AssumeRolePolicyDocument"]["Statement"]:
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
		if not debug: client.update_assume_role_policy(RoleName=role["RoleName"], PolicyDocument="{0}".format(role["AssumeRolePolicyDocument"]));
		else: logger.info(c_role["AssumeRolePolicyDocument"]);

		## Ensure that source Role has the permissions
		logger.info("Checking sts:AssumeRole permissions for source Role...");
		session         = None;
		session         = aws_session("arn:aws:iam::{0}:role/{1}".format(extract_account_from_arn(source_role), role));
		client          = session.client("iam",  region, config=Config(read_timeout=timeout, connect_timeout=timeout));
		all_policies    = client.list_role_policies(RoleName=source_role.split("/")[1])["PolicyNames"];
		found           = False;
		for p in all_policies:
			f_policy = client.get_role_policy(RoleName=source_role.split("/")[1], PolicyName=p);
			policy   = f_policy["PolicyDocument"];
			logger.info("Scanning Policy: {0}".format(f_policy["PolicyName"]));
			if not any("sts:AssumeRole" in x["Action"] \
				or (isinstance(x["Resource"], list) and target_role in x["Resource"]) \
				or (isinstance(x["Resource"], str) and x["Resource"] == "*") for x in policy["Statement"]):
				continue;
			if any(("*" == x["Resource"] or target_role in x["Resource"]) and "sts:AssumeRole" in x["Action"] for x in policy["Statement"]):
				logger.info("Source Role should already have permissions");
				found = True;
				break;
			statement = next(x for x in policy["Statement"] if "sts:AssumeRole" in x["Action"] or "*" in x["Resource"] or target_role in x["Resource"]);
			found     = True;
			if "sts:AssumeRole" in statement["Action"]:
				statement["Resource"].append(target_role);
				if not debug: client.put_role_policy(RoleName=source_role.split("/")[1], PolicyName=f_policy["PolicyName"], PolicyDocument="{0}".format(policy));
				break;
			else:
				if isinstance(statement["Action"], list): statement["Action"].append("sts:AssumeRole");
				else: statement["Action"] = [statement["Action"], "sts:AssumeRole"];
				if not debug: client.put_role_policy(RoleName=source_role.split("/")[1], PolicyName=f_policy["PolicyName"], PolicyDocument="{0}".format(policy));
				break;
		if not found:
			logger.warning("Sorry, no Policy found with sts:AssumeRole in source Account.  Permissions will need to be added manually..");
		else:
			if debug: logger.info(policy);
	except Exception as ex: logger.error(ex); raise ex;

