#!/usr/bin/env python3
###############################################################################
# Name        : test_role_deletion                                            #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Test creation and deletion of an IAM Role.                    #
###############################################################################
import os, sys, boto3, logging, random, json, time;
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");
log = logging.getLogger(__name__);

def aws_session(arn, session_name="trm-session", ttl=60):
	client  = boto3.client("sts");
	rsp     = client.assume_role(RoleArn=arn, RoleSessionName=session_name, DurationSeconds=(ttl * 60));
	session = boto3.Session(aws_access_key_id=rsp["Credentials"]["AccessKeyId"],
		aws_secret_access_key=rsp["Credentials"]["SecretAccessKey"],
		aws_session_token=rsp["Credentials"]["SessionToken"]);
	return session;

if __name__ == "__main__": 
	params               = {};
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	account              = params.get("--acct", None);
	role_name            = params.get("--role", None);
	assert account != None, "Account cannot be empty...";
	assert role_name != None, "Role name cannot be empty...";
	session1             = aws_session("arn:aws:iam::{0}:role/{1}".format(account, role_name));
	client1              = session1.client("iam");
	role_name2           = "test_role_{0}".format(random.randint(10000, 99999));
	identity_1           = boto3.client("sts").get_caller_identity();
	log.info("Creating new IAM Role: {0}".format(role_name2));
	client1.create_role(RoleName=role_name2, AssumeRolePolicyDocument=json.dumps({
		"Version": "2012-10-17",
		"Statement": [
		{
			"Effect": "Allow",
			"Principal": {
				"AWS": [
					"arn:aws:iam::{0}:role/{1}".format(account, role_name),
					identity_1["Arn"]
				]
			},
			"Action": "sts:AssumeRole"
		}
	]}));
	time.sleep(10);
	role2 = client1.get_role(RoleName=role_name2);
	log.info("Performing smoke test on new role with {0} seconds...".format(role2["Role"]["MaxSessionDuration"]));
	session2 = aws_session("arn:aws:iam::{0}:role/{1}".format(account, role_name2), ttl=int(role2["Role"]["MaxSessionDuration"] / 60));

	log.info("Updating IAM Role session duration...");
	client1.update_role(RoleName=role_name2, MaxSessionDuration=43200);
	time.sleep(10);

	log.info("Performing smoke test on new role with {0} seconds...".format(role2["Role"]["MaxSessionDuration"]));
	session2 = aws_session("arn:aws:iam::{0}:role/{1}".format(account, role_name2), ttl=int(role2["Role"]["MaxSessionDuration"] / 60));

	log.info("Deleting IAM Role...");
	client1.delete_role(RoleName=role_name2);
	time.sleep(10);

	log.info("Attempt to assume IAM Role after delettion...");
	try:
		session3 = aws_session("arn:aws:iam::{0}:role/{1}".format(account, role_name2), ttl=int(role2["Role"]["MaxSessionDuration"] / 60));
	except Exception as ex:
		log.info(ex);
		try:
			log.info("Attempt to reuse 12 hour session")
			client2 = session2.client("s3");
		except Exception as ex2:
			log.info(ex2);
