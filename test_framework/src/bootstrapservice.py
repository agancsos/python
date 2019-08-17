#!/bin/python
import os;
import sys;
import re;

class Bootstraper:
	classes = { };

	@staticmethod	
	def load_path(path):
		for child in os.listdir(path):
			script = "";
			if os.path.isdir("{0}/{1}".format(path, child)):
				if "{0}/{1}".format(path, child) not in sys.path:
					sys.path.insert(0, "{0}/{1}".format(path, child));
					Bootstraper.load_path("{0}/{1}".format(path, child));
			else:
				if child[-2:] == "py" and child[0] != ".":
					try:
						with open("{0}/{1}".format(path, child), "r") as reader:
							script = reader.read();
						m = re.search(r"(class\W*)(.+)(\(TestCase\))", script, flags=re.MULTILINE|re.DOTALL);
						if m is not None:
							Bootstraper.classes[m.group(2)] = getattr(__import__(child[:-3]), m.group(2));
						pass;
					except Exception as e:
						print(e);
						continue;
					pass;
				pass;
			pass;
		pass;

	@staticmethod
	def bootstrap(base="./"):
		sys.path.append(base);
		Bootstraper.load_path(base);
		pass;
	pass;
