#!/usr/bin/env python3
###############################################################################
# Name        : aws_client.py                                                 #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helpers to connect to an AWS environment.                     #
###############################################################################
import requests_html, datetime, base64, hmac, hashlib, urllib.parse, logging;

class AWSClient:
	base_endpoint=None;username=None;password=None;client=None;debug=None;force=None;
	def __init__(self, params=dict()):
		logging.basicConfig(format="%(asctime)s %(message)s";
		logger                 = logging.getLogger(__name__);
		self.base_endpoint     = params["-b"] if "-b" in params.keys() else "https://ec2.us-east-2.amazonaws.com";
		self.username          = params["-u"] if "-u" in params.keys() else "";
		self.password          = params["-p"] if "-p" in params.keys() else "";
		self.client            = requests_html.HTMLSession(verify=True);
	def sign(self, key, msg): return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
	def generate_signature(self, service, timestamp, region="us-east-2"):
		return self.sign(self.sign(self.sign(self.sign("AWS4{0}".format(self.password).encode("utf-8"), timestamp.strftime("%Y%m%d")), region), service), "aws4_request");
	def invoke_req(self, method, service, region, action, args=None):
		timestamp = datetime.datetime.utcnow();
		a = urllib.parse.urlparse("{0}/?Action={1}{2}&Version=2016-11-15".format(self.base_endpoint, action, "&{0}".format(args) if args != None else ""));
		ca_uri = a.path; ca_query = a.query;
		if method == "GET": payload = hashlib.sha256(('').encode("utf-8")).hexdigest();
		ca_headers = "host:{0}\nx-amz-date:{1}\n".format(a.hostname, timestamp.strftime("%Y%m%dT%H%M%SZ"));
		ca_request = "{0}\n{1}\n{2}\n{3}\nhost;x-amz-date\n{4}".format(method, ca_uri, ca_query, ca_headers, payload);
		scope = "{0}/{1}/{2}/aws4_request".format(timestamp.strftime("%Y%m%d"), region, service);
		ca_string = "AWS4-HMAC-SHA256\n{0}\n{1}\n{2}".format(timestamp.strftime("%Y%m%dT%H%M%SZ"), scope, hashlib.sha256(ca_request.encode("utf-8")).hexdigest());
		signing_key = self.generate_signature(service, timestamp, region);
		signature = hmac.new(signing_key, ca_string.encode("utf-8"), hashlib.sha256).hexdigest();
		headers = {
			"X-AMZ-DATE":timestamp.strftime("%Y%m%dT%H%M%SZ"),
			"Authorization":"AWS4-HMAC-SHA256 Credential={0}/{1}, SignedHeaders=host;x-amz-date, Signature={2}".format(self.username, scope, signature)};
		if method == "GET": return self.client.get("{0}/?Action={1}{2}&Version=2016-11-15".format(self.base_endpoint, action, "&{0}".format(args) if args != None else ""), headers=headers);
	pass;

