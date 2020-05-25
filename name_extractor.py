###############################################################################
# Name       : Name Extractor                                                 #
# Author     : Abel Gancsos                                                   #
# Version    : v. 1.0.0                                                       #
# Description: Generates a list of possible values given a specific pattern   #
###############################################################################
#!/usr/bin/python
import os;
import sys;
import random;

class NameExtractor:
	mask = "*";
	def __init__(self):
		pass;
	def invoke(self, pattern):
		results = list();
		letters = "ABCDEFGHIJKLMNOPQRSTUVWXWZ";
		combinations =  pow(pattern.count(self.mask), len(letters));
		for i in xrange(0, combinations):
			result = "";
			for j in range(0, len(pattern)):
				if (pattern[j] != self.mask):
					result += pattern[j];
				else:
					result += letters[random.randrange(0, len(letters) - 1)];
			if result not in results:
				print(result);
				results.append(result);
		return results;
	pass;

if __name__ == "__main__":
	session = NameExtractor();
	pattern = "";

	for param_i in range(0, len(sys.argv)):
		if (sys.argv[param_i] == "--pattern"):
			pattern = sys.argv[param_i + 1];
		elif (sys.argv[param_i] == "--mask"):
			session.mask = sys.argv[param_i + 1];

	session.invoke(pattern);
	pass;
