#!/usr/bin/env python3
###############################################################################
# Name		: memcompare.py												                              #
# Author	  : Abel Gancsos												                            #
# Version	 : v. 1.0.0.0													                              #
# Description : Compares 2 gdb dumps for memory leaks.						            #  
###############################################################################
import os, sys, subprocess;

class OffsetEntry:
	address=None;progbits=None;
	def __init__(self, addr, pbits): self.address = addr; self.progbits = pbits;

class CoreDump:
	path=None;entries=None;
	def __init__(self, path=""):
		self.path = path;
		self.entries = dict();
		assert self.path != "" and os.path.exists(self.path), "Path of core cannot be empty...";
		self.extract_entries();
	def extract_entries(self):
		try:
			raw_elf = subprocess.run(["hexdump", self.path], stdout=subprocess.PIPE).stdout.decode("utf-8").split("\n");
			for line in raw_elf:
				comps = line.split(" ");
				if (len(comps) ==1): continue;
				entry = OffsetEntry(comps[0], ";".join(comps[1:]).split(";"));
				self.entries[comps[0]] = entry;
		except Exception: print("hexdump not installed on system....");
	def find_entry(self, addr): return self.entries[addr] if addr in self.entries.keys() else None;
	pass;

"""
Insctructions:
1. Generate a core dump before via gcore -o <name> <pid>
2. Run the payload
3. Generate a second dump
"""
class MemoryComparer:
	dump11=None;dump2=None;ignore_missing=None;ignore_data=None;
	def __init__(self, params=dict()):
		self.dump1 = CoreDump(params["--c1"]) if "--c1" in params.keys() else None;
		self.dump2 = CoreDump(params["--c2"]) if "--c2" in params.keys() else None;
		self.ignore_missing = True if "--ignore" in params.keys() and int(params["--ignore"]) > 0 else False;
		self.ignore_data = True if "--ignore-data" in params.keys() and int(params["--ignore-data"]) > 0 else False;
		self.entries = dict();
	def invoke(self):
		assert self.dump1 != None, "Core dump1 not set...";
		assert self.dump2 != None, "Core dump2 not set...";
		for entry in self.dump2.entries.keys():
			dump1_entry = self.dump1.find_entry(entry);
			dump2_entry = self.dump2.find_entry(entry);
			if (dump1_entry == None):
				if not self.ignore_missing: print("Entry not found ({0})".format(entry));
				continue;
			if (dump2_entry.size - dump1_entry.size < 1): continue;
			if (dump2_entry.progbits != dump1_entry.progbits):
				if (self.ignore_data):
					print("{0}; {1}; {2}".format(entry, dump2_entry.size - dump1_entry.size, dump2_entry.progbits));
				else:
					data = "";
					for c in dump2_entry.progbits:
						data = "{0}{1}".format(data, chr(int(str(int(c, 16)).encode("unicode_escape").decode("ascii"))));
					line_with_data = "{0};{1}".format(entry, data);
					try: print(line_with_data);
					except: print("{0}; {1}; {2}".format(entry, dump2_entry.size - dump1_entry.size, dump2_entry.progbits));
		pass;
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = MemoryComparer(params);
	session.invoke();
	pass;
