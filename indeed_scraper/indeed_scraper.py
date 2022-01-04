#!/usr/bin/env python3
###############################################################################
# Name        : indeed_crawler.py                                             #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helps find open roles based on Indeed data.                   #
###############################################################################
import os, sys, requests_html, json, scrapy, threading, urllib;
import xml.etree.ElementTree as ett;
class IndeedEntry:
	title=None;location=None;company=None;details=None;
	def __init__(self, raw):
		try:
			obj = ett.fromstring(raw);
			self.title = obj.find('.//h2/span[@title]').text;
			self.company = obj.find('.//*[@class="companyName"]').text if obj.find('.//*[@class="companyName"]/a') == None else obj.find('.//*[@data-tn-element="companyName"]').text;
			self.location = obj.find('.//div[@class="companyLocation"]').text if obj.find('.//div[@class="companyLocation"]').text != None else "Remote";
			self.details = obj.find('.//div[@class="job-snippet"]');
		except Exception: pass;
	def __str__(self): return "{0}; {1}; {2}".format(self.company, self.title, self.location);
class IndeedScraper:
	base_endpoint=None;dorking_path=None;threads=None;req_headers=None;cache=None;companies_only=False;limit=None;
	def __init__(self, params=dict()):
		self.limit = int(params["-l"]) if "-l" in params.keys() and int(params["-l"]) > -1 else 50;
		self.req_headers = { "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36" };
		self.base_endpoint = params["-b"] if "-b" in params.keys() else "https://www.indeed.com/jobs?start=0&limit={0}&".format(self.limit);
		self.dorking_path = params["-p"] if "-p" in params.keys() else ".";
		self.companies_only = True if "-c" in params.keys() and int(params["-c"]) > 0 else False;
		self.threads = list();
		self.cache = set();
	def build_endpoint(self, raw): return "{0}q={1}&l={2}&explvl={3}".format(self.base_endpoint, urllib.parse.quote(raw["keywords"]), raw["location"], raw["experience"]);
	def crawl(self, endpoint):
		session = requests_html.HTMLSession(verify=False);
		rsp = session.get(endpoint, headers=self.req_headers);	
		m = scrapy.http.HtmlResponse(url=rsp.url, body=rsp.text, encoding='utf8').xpath('//div[@class="job_seen_beacon"]');
		if m != None:
			for e in m:
				ex = IndeedEntry(e.get());
				if not any(x.__str__().strip() in ex.__str__().strip() for x in self.cache) and ((self.companies_only and not any(x.company == ex.company for x in self.cache)) or not self.companies_only):
					self.cache.add(ex);
	def walk_tree(self, path):
		if os.path.isdir(path):
			children = os.listdir(path);
			for child in children: 
				t = threading.Thread(target=self.walk_tree, args=("{0}/{1}".format(path, child).replace("\\", "/"),));
				self.threads.append(t);
				t.start();
		else:
			raw_entries=None;
			with open(path, "r") as fh: raw_entries = fh.read().split("\n");
			for entry in raw_entries:
				if entry == "": continue;
				try:
					json_entry = json.loads(entry);
					t = threading.Thread(target=self.crawl, args=(self.build_endpoint(json_entry), ));
					self.threads.append(t);
					t.start();
				except Exception: pass;
		for t in self.threads: 
			try: t.join();
			except Exception: pass;
	def invoke(self):
		assert self.base_endpoint != "", "Base endpoint cannot be empty...";
		assert self.dorking_path != "", "Dorking path cannot be empty...";
		self.walk_tree(self.dorking_path);
		for e in self.cache: print(e);
		pass;
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = IndeedScraper(params);
	session.invoke();

