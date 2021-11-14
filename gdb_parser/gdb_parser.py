#!/usr/bin/env python3
###############################################################################
# Name        : gdb_parser.py                                                 #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Parses a GDB trace for pointer allocations.                   #
###############################################################################
import os, sys, re;

class GDBEntry:
    address=None;freed=None;call_stack=None;
    def __init__(self, a, f, s): self.address = a; self.freed = f; self.call_stack = s;
    pass;

class GDBParser:
    trace_path=None;entries=None;verbose=None;
    def __init__(self, params=dict()):
        self.trace_path = params["-f"] if "-f" in params.keys() else "";
        self.verbose = True if "-v" in params.keys() and int(params["-v"]) > 0 else False;
        assert self.trace_path != "" and os.path.exists(self.trace_path), "Trace path cannot be empty and must exist...";
        self.entries = dict();
        self.parse_entries();
    def parse_entries(self):
        with open(self.trace_path, "r") as fh:
            line = fh.readline();
            while (line != ">>>END<<<"):
                if (line == ""): line = fh.readline(); continue;
                if (self.verbose): print(">>> {0}".format(line));
                m = re.search("(\w+) in ", line);
                if (m != None):
                    entry = m.group(1);
                    if m.group(1) not in self.entries.keys(): self.entries[entry] = GDBEntry(entry, False, "");
                m = re.search("(\w+) in (free|fclose)", line);
                if (m != None):
                    entry = m.group(1);
                    if entry in self.entries.keys(): self.entries[entry].freed = True;
                line = fh.readline();
    def invoke(self):
        for e in self.entries: print("{0} => {1}".format(self.entries[e].address, self.entries[e].freed));
    pass;

if __name__ == "__main__":
    params = dict();
    for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
    session = GDBParser(params);
    session.invoke();
    pass;
