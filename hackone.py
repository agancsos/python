#!/usr/bin/env python3
###############################################################################
# Name         : hackerone.py                                                 #
# Author       : Abel Gancsos                                                 #
# Version      : v. 1.0.0.0                                                   #
# Description  : Helps build out Hacker1 reports without a REST API.          #
###############################################################################
import os, sys, requests_html;

class HackerOner:
	base_endpoint=None;mode=None;headers=None;sleep=None;
	def __init__(self, params=dict()):
		self.base_endpoint = params["--end"] if "--end" in params.keys() else "https://hackerone.com";
		self.mode = params["--mode"] if "--mode" in params.keys() else "companies";
		self.sleep = int(params["--sleep"]) if "--sleep" in params.keys() else 1;
		self.headers = { \
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36', \
			"Upgrade-Insecure-Requests": "1"
		};
		pass;
	def invoke(self):
		assert self.base_endpoint != "", "Endpoint cannot be empty...";
		assert self.mode != "", "Mode cannot be empty...";
		session = requests_html.HTMLSession(verify=False);

		## Lists companies that use Hacker1 for pentesting
		if (self.mode == "companies"):
			rsp = session.get("{0}/programs/search?query=bounties:yes&sort=name:ascending&limit=1000".format(self.base_endpoint), headers=self.headers);
			if (rsp.status_code == 200):
				for c in rsp.json()["results"]: print(c["name"]);

		## Lists Pentesters (Hackers) by ranking with their reputation score
		elif (self.mode == "hackers"):
			rsp = session.get("{0}/leaderboard/reputation".format(self.base_endpoint), headers=self.headers, allow_redirects=False);
			rsp.html.render(sleep=self.sleep);
			hs = rsp.html.find("img");
			stats = rsp.html.find("td");
			rank = 1;
			for h in hs:
				if ("class" in h.attrs.keys() and "daisy-avatar" in h.attrs["class"]): 
					if ("alt" in h.attrs.keys()): 
						print("{0} ({1})".format(h.attrs["alt"], stats[rank * 4 - 3].text));
						rank += 1;
		else: print("Mode is not currently supported ({0})".format(self.mode));
	pass;

if (__name__ == "__main__"):
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = HackerOner(params);
	session.invoke();
	pass;

