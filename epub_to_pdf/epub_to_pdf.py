#!/bin/bash env python
import os;
import sys;
import shutil;
import re;
"""
https://snipplr.com/view/70884/convert-epub-to-pdf-in-linux-command-line
Readme:
	# Requires	
		* https://wkhtmltopdf.org/downloads.html
"""
class EpubConvertor:
	source_path = None; target_path = None;
	def __init__(self):
		self.source_path = "";
		self.target_path = "";
		pass;
	def invoke(self):
		self.source_path = os.path.realpath(self.source_path);
		print(self.source_path);
		assert os.path.exists(self.source_path), "Source path doesn't exist...";
		assert os.path.exists(self.target_path), "Target base path doesn't exist...";
		## Find title in package
		raw_file = "";
		with open("{0}/OEBPS/package.opf".format(self.source_path), 'r') as handler:
			raw_file = handler.read();
		m = re.search('(\<dc:title\>)(.*)(\</dc:title\>)', raw_file);
		title = m.group(2);
		os.system('rm -fR "{0}/{1}"'.format(self.target_path, title));
		os.mkdir("{0}/{1}".format(self.target_path, title));
		## Convert HTML files to PDF
		for file in os.listdir("{0}/OEBPS".format(self.source_path)):
			if ".xhtml" in file:
				print("file://{0}/OEBPS/{3}".format(self.source_path, self.target_path, title, file));
				os.system('wkhtmltopdf -q --title "{1}" "file://{0}/OEBPS/{3}" "{1}/{2}/{3}".pdf'.format(self.source_path, self.target_path, title, file));
		## Merge PDF files to single
		os.system('cd "{0}/{1}" && cat *.pdf > "{0}/{1}.pdf"'.format(os.path.realpath(self.target_path), title));
		## Cleanup
		os.system('rm -fR "{0}/{1}"'.format(self.target_path, title));
		pass;
	pass;

if __name__ == "__main__":
	session = EpubConvertor();
	for param_i in range(0, len(sys.argv)):
		if (sys.argv[param_i] == "--epub"):
			session.source_path = sys.argv[param_i + 1];
		elif (sys.argv[param_i] == "--tar"):
			session.target_path = sys.argv[param_i + 1];
		pass;
	session.invoke();
	pass;
