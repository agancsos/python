#!/usr/bin/env python3
###############################################################################
# Name        : aws_search_bucket.py                                          #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Finds a specific file in buckets.                             #
###############################################################################
import os, sys, boto3, logging;
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");

class AwsService:
    accounts=None;search=None;logger=None;role_name=None;
    def __init__(self, params=dict()):
        self.logger              = logging.getLogger(__name__);
        self.accounts            = params["--accounts"].split(",") if "--accounts" in params.keys() else [];
        self.search              = params["--search"] if "--search" in params.keys() else "";
        self.role_name           = params["--role"] if "--role" in params.keys() else "";
    def get_assumed_session(self, arn, session_name="aws_runner"):
        client     = boto3.client("sts");
        rsp        = client.assume_role(RoleArn=arn, RoleSessionName=session_name);
        session    = boto3.Session(aws_access_key_id=rsp["Credentials"]["AccessKeyId"],
            aws_secret_access_key=rsp["Credentials"]["SecretAccessKey"], aws_session_token=rsp["Credentials"]["SessionToken"]);
        return session;
    def invoke(self):
        for account in self.accounts:
            session   = self.get_assumed_session("arn:aws:iam::{0}:role/{1}".format(account, self.role_name));
            client    = session.client("s3");
            buckets   = client.list_buckets()["Buckets"];
            for bucket in buckets:
                bucket_objects = client.list_objects(Bucket=bucket["Name"]);
                for item in bucket_objects["Contents"]:
                    if self.search in item["Key"]: self.logger.info("s3://{0}/{1}".format(bucket["Name"], item["Key"]));
    pass;

if __name__ == "__main__":
    params                = dict();
    for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
    session               = AwsService(params);
    session.invoke();

