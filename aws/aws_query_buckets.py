#!/usr/bin/env python3
###############################################################################
# Name        : aws_query_buckets.py                                          #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description :                                                               #
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
	bucket_name                = params["--bucket"] if "--bucket" in params.keys() else "";
	object_key                 = params["--key"] if "--key" in params.keys() else "";
	query                      = params["--query"] if "--query" in params.keys() else "select * from s3object"
	record_delim               = params["--rdelim"] if "--rdelim" in params.keys() else "\n";
	field_delim                = params["--fdelim"] if "--fdelim" in params.keys() else ";";
	session                    = boto3.Session();
	if role != "":
		assert account != "", "Account cannot be empty...";
		session                    = aws_session("arn:aws:iam::{0}:role/{1}".format(account, role));
	try:
		items                      = [];
		client                     = session.client("s3", region, config=Config(read_timeout=timeout, connect_timeout=timeout));
		input_serial = {}; output_serial = {};
		if ".csv" in object_key:
				input_serial = {"CSV": {"RecordDelimiter": record_delim, "FieldDelimiter": field_delim}};
				output_serial = input_serial;
		else:
				input_serial = {"JSON": {"Type": "DOCUMENT"}};
				output_serial = {"JSON": {"RecordDelimiter": record_delim}};
		rsp                        = client.select_object_content(Bucket=bucket_name,
            Key=object_key,
            Expression=query,
            ExpressionType="SQL",
            InputSerialization=input_serial,
            OutputSerialization=output_serial);
		payload = next(x for x in rsp["Payload"]);
		records = json.loads(payload["Records"]["Payload"]);
		for k, v in records.items(): logger.info("{0}: {1}".format(k, v));
	except Exception as ex: logger.error(ex);

