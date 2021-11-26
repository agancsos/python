#!/usr/bin/env python3
###############################################################################
# Name        : zork.py                                                       #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Run Google Dork queries based on dork files.                  #
###############################################################################
import os, sys, requests_html, time;
class Zork:
	operation=None;probe_path=None;loot_path=None;jitter_rate_seconds=None;domain=None;working_path=None;debug=None;req_headers=None;
	def __init__(self, params=dict()):
		self.working_path = os.path.realpath(os.path.dirname(__file__));
		self.req_headers = { "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36" };
		self.operation = params["--op"] if "--op" in params.keys() else "probe";
		self.probe_path = params["-p"] if "-p" in params.keys() else "{0}/dorks".format(self.working_path);
		self.loot_path = params["--loot"] if "--loot" in params.keys() else "{0}/loot".format(self.working_path);
		self.jitter_rate_seconds = int(params["-j"]) if "-j" in params.keys() else 5;
		self.domain = params["--domain"] if "--domain" in params.keys() else "";
		self.debug = True if "--debug" in params.keys() and int(params["--debug"]) > 0 else False;
	def encode_query(self, query):
		return query.replace("+", "%2B").replace(" ", "+").replace(":", "%3A");
	def probe(self, path):
		if (os.path.isdir(path)):
			for x in os.listdir(path): self.probe("{0}/{1}".format(path, x));
		else:
			session = requests_html.HTMLSession(verify=False);
			comps = path.replace("./", "").split(".");
			if len(comps) > 0 and comps[1] in ("dork"):
				with open(path, "r") as fh:
					dork = fh.readline();
					row = 1;
					while (dork != ""):
						query = self.encode_query("{0} site:{1}".format(dork, self.domain) if self.domain != "" else dork);
						rsp = session.get("https://www.google.com/search?q={0}".format(query), headers=self.req_headers);
						rsp.html.render(sleep=30);
						with open("{0}/{1}_{2}.dork.result".format(self.loot_path, comps[0], row), "w+") as fh2:
							fh2.write("query: {0}\n".format(query));
							raw_content = "{0}".format(rsp.html);
							m = rsp.html.find("a");
							if (m != None):
								for e in m: 
									if ("href" in e.attrs.keys() and "http" in e.attrs["href"]): fh2.write("* {0}".format(e.attrs["href"]));
						dork = fh.readline();
						row += 1;
						time.sleep(self.jitter_rate_seconds);
	def invoke(self):
		assert self.operation != "", "Operation cannot be empty...";
		if (self.operation == "update"): pass;
		elif (self.operation == "probe"):
			assert self.probe_path != "" and os.path.exists(self.probe_path), "Probe path cannot be empty...";
			if not os.path.exists("{0}/dorks".format(self.loot_path)): os.mkdir("{0}/dorks".format(self.loot_path));
			self.probe(self.probe_path);
		else: print("Operation ({0}) not currently supported...".format(self.operation));
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = Zork(params);
	session.invoke();

