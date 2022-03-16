#!/usr/bin/env python3
###############################################################################
# Name        : extract_aws_services.py                                       #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Extracts a list of AWS services.                              #
###############################################################################
import re, requests_html, sys;

class ServiceExtractor:
    base_endpoint=None;client=None;
    def __init__(self, params=dict()):
        self.base_endpoint = params["-b"] if "-b" in params.keys() else "https://docs.aws.amazon.com/general/latest/gr/aws-service-information.html";
        self.client        = requests_html.HTMLSession(verify=True);
    def invoke(self):
        assert self.base_endpoint != "", "Base endpoint cannot be empty...";
        rsp = self.client.get(self.base_endpoint);
        ms  = re.findall("\<li\>.+?\</a\>?", rsp.content.decode("utf-8"));
        for m in ms: print(m.split("\">")[1].replace("</a>", ""));
    pass;

if __name__ == "__main__":
    params = dict();
    for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
    session = ServiceExtractor(params);
    session.invoke();
    
