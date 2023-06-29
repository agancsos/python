#!/usr/bin/env python3
###############################################################################
# Name        : hercules_client.py                                            #
# Version     : v. 1.0.0.0                                                    #
# Author      : Abel Gancsos                                                  #
# Description :                                                               #
###############################################################################
import os, sys, json, requests, re;

class HerculesClient:
	def __init__(self, params=dict()):
		self.base_endpoint = params["baseEndpoint"] if "baseEndpoint" in params.keys() else "";
		self.session       = requests.Session();
	def parse_response(self, raw):
		if "<table>" not in raw:
			response_data = re.findall("<PRE>.*</PRE>", raw, re.DOTALL)[0].replace("<PRE>", "").replace("</PRE>", "");
			return {"raw": raw.replace("\n", "\\n"), "data": response_data.replace("\n", "\\n")};
		else:
			tables        = [];
			response_data = re.findall("<table>.*?</table>", raw, re.DOTALL);
			for table in response_data:
				table_data    = [];
				raw_data      = re.findall("<th>.*?</th>", table, re.DOTALL);
				fields        = [x.replace("<th>", "").replace("</th>", "") for x in raw_data];
				raw_data      = re.findall("<tr>.*?</tr>", table, re.DOTALL);
				for lines in raw_data:
					raw_data2 = re.findall("<td>.*?</td>", table, re.DOTALL);
					raw_item  = {};
					for i in range(0, len(fields)):
						raw_item[fields[i]] = raw_data2[i].replace("<td>", "").replace("</td>", "");
					table_data.append(raw_item);
				tables.append(table_data);
			return {"raw": raw.replace("\n", "\\n"), "data": tables};
	def raw_request(self, url, redirects=False):
		if "http" not in url: url = "{0}/{1}".format(self.base_endpoint, url);
		try:
			rsp = self.session.get(url, allow_redirects=redirects);
			return self.parse_response(rsp.content.decode());
		except Exception as ex:
			return {"error": f"{ex}"};
	def raw_post_request(self, url, params, redirects=True):
		if "http" not in url: url = "{0}/{1}".format(self.base_endpoint, url);
		try:
			rsp = self.session.post(url, data=params, allow_redirects=redirects);
			print(rsp.content);
			return self.parse_response(rsp.content.decode());
		except Exception as ex:
			return {"error": f"{ex}"};

def new_hercules_client(base_endpoint=""):
	rst               = HerculesClient();
	rst.base_endpoint = base_endpoint;
	return rst;

