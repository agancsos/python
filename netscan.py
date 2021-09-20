#!/usr/bin/env python3
###############################################################################
# Name        : netscan.py                                                    #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Scans the network systems for open ports.                     #
###############################################################################
import os, sys, socket, threading, datetime;

class NetInfo:
    ip=None;ports=None;
    def __init__(self, ip, ports=list()):
        self.ip = ip; self.ports = ports
    pass
class NetScanner:
    base_ip=None;verbose=None;wait=None;cache=None;start_time=None;end_time=None;duration=None;
    def __init__(self, params=dict()):
        self.cache = dict();
        self.base_ip = params["-b"] if "-b" in params.keys() else "192.168.3";
        self.verbose = True if "-v" in params.keys() and int(params["-v"]) > 0 else False;
        self.wait = int(params["-w"]) if "-w" in params.keys() else 3;
        pass;
    def scan_ports(self, ip):
        info = NetInfo(ip);
        for port in range(22, 5024):
            rsp = os.system("nc -zw{0} {1} {2} > /dev/null 2>&1".format(self.wait, ip, port));
            if rsp == 0 and port not in info.ports: info.ports.append(port);
        if (self.cache[info.ip] == None): self.cache[info.ip] = info;
        pass;
    def check_ip(self, ip):
        rsp = os.system("ping -c 1 -W {0} {1} > /dev/null 2>&1".format(self.wait, ip));
        if (rsp == 0):
            if (self.verbose): print("Found IP ({0})".format(ip));
            t = threading.Thread(target=self.scan_ports, args=("{0}".format(ip),));
            t.start();
        pass;
    def invoke(self):
        assert self.base_ip != "", "Base ip cannot be empty...";
        self.start_time = datetime.datetime.now();
        for current_ip in range(2, 255):
            full_ip = "{0}.{1}".format(self.base_ip, current_ip);
            if (self.verbose): print("Checking: {0}".format(full_ip));
            t = threading.Thread(target=self.check_ip, args=("{0}".format(full_ip),));
            t.start();
            t.join();
            pass;
        self.end_time = datetime.datetime.now();
        self.duration = abs(self.end_time - self.start_time)
        print("Ports found:");
        for ip in self.cache.keys():
            print("* {0}".format(ip));
            for port in self.cache[ip].ports: print("    * {0}".format(port));
        print("Scan ran for {0} seconds".format(self.duration.seconds));
    pass;

if __name__ == "__main__":
    params = dict();
    for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
    session = NetScanner(params);
    session.invoke();
    pass;
