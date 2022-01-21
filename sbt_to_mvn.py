#!/usr/bin/env python3
###############################################################################
# Name        : sbt_to_mvn.py                                                 #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Generates Maven dependencies from SBT.                        #
###############################################################################
import os, sys, re;

class SbtConverter:
	input_file=None;output_file=None;debug=None;
	def __init__(self, params=dict()):
		self.input_file = params["-i"] if "-i" in params.keys() else "";
		self.output_file = params["-o"] if "-o" in params.keys() else "";
		self.debug = True if "--debug" in params.keys() and int(params["--debug"]) > 0 else False;
		self.init_value = 0;
	def invoke(self):
		assert self.input_file != "" and os.path.exists(self.input_file), "SBT definition file must exist...";
		result = "<dependencies>";
		raw = "";
		with open(self.input_file, "r") as fh: raw = fh.read();
		ms = re.findall("libraryDependencies \+\+= Seq\([^\)]*", raw, re.MULTILINE);
		if ms != None:
			for m in ms[0].split("\n"):
				if "%" in m:
					comps = m.replace("\"", "").replace(",", "").strip().split("%");
					result += "\n\t<dependency>\n\t\t<groupId>{0}</groupId>\n\t\t<artifactId>{1}</artifactId>\n\t\t<version>{2}</version>".format(comps[0].strip(), comps[1].strip(), comps[2].strip());
					if len(comps) > 3: result += "\n\t\t<scope>{0}</scope>".format(comps[3].strip());
					result += "\n\t</dependency>";
			result += "\n</dependencies>";
			if self.debug or self.output_file == "": print(result);
			else:
				with open(self.output_file, "w") as fh: fh.write(result);
		else: print("Did not find any dependencies...");
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = SbtConverter(params);
	session.invoke();

