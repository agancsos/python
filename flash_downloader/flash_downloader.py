###############################################################################
# Name        : flash_downloader                                              #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0                                                      #
# Description : This script is meant to help download videos from the web     #
###############################################################################
#!/bin/python
import os;
import sys;
import re;
import urllib2;

class Link:
	source = "";
	pattern = "setVideoUrlHigh\(\'([^\']+)\'";
	
	def __init__(self, src=""):
		self.source = src;
		pass;
	def find_url(self):
		try:
			raw_html = urllib2.urlopen(self.source).read();
			matches = re.search(self.pattern, raw_html);
			if matches is not None:
				return matches.group(1);
			else:
				print("No download link found...");
		except Exception as e:
			print(e);
		return None;
		pass;
	def download(self, target=""):
		if(os.path.exists(target)):
			url = self.find_url();
			if url is not None:
				comps = url.split("/");
				video_name = comps[len(comps) - 1];
				cmd = "curl {0} -o {1}/{2}".format(self.find_url(), target, video_name);
				os.system(cmd);
			pass;
		else:
			print("Path does not exist ({0})".format(target));
		pass;
	pass;

class Downloader:
	links = list();
	target_path = "./";
	
	def __init__(self, links=list()):
		self.links = links;
		pass;
	def add_link(self, url):
		self.links.append(Link(url));
		pass;
	def download(self):
		for link in self.links:
			link.download(self.target_path);
			pass;
		pass;
	pass;

if __name__== "__main__":
	links = list();
	broker = Downloader(links);

	if(len(sys.argv) > 0):
		for param_i in range(0, len(sys.argv)):
			if(sys.argv[param_i] == "-t"):
				broker.target_path = sys.argv[param_i + 1];
			elif(sys.argv[param_i] == "-l"):
				broker.add_link(sys.argv[param_i + 1]);
			pass;
	broker.download();
	pass;
