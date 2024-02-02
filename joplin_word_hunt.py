#!/usr/bin/env python3
###############################################################################
# Name       : joplin_word_hunt.py                                            #
# Author     : Abel Gancsos                                                   #
# Version    : v. 1.0.0.0                                                     #
# Description: Helps find Joplin notes based on keywords and REGEX patterns.  #
###############################################################################
import os, sys, re, requests, json;

def retrieve_notes(base_endpoint, token):
	rst      = [];
	has_more = True;
	page     = 1;
	while has_more:
		rsp = requests.get("{0}/notes?token={1}&page={2}".format(base_endpoint, token, page));
		assert rsp.status_code == 200, "\033[31mFailed to retrieve notes...\033[m";
		rsp      = rsp.json();
		has_more = rsp["has_more"];
		page += 1;
		for item in rsp["items"]:
			rsp2 = requests.get("{0}/notes/{1}?token={2}&fields=body".format(base_endpoint, item["id"], token));
			item["body"] = rsp2.json()["body"];
			rst.append(item);
	return rst;

if __name__ == "__main__":
	params               = {};
	keywords             = [];
	for i in range(0, len(sys.argv) - 1):
		if sys.argv[i] == "-k": keywords.append(sys.argv[i + 1]);
		params[sys.argv[i]] = sys.argv[i + 1];
	base_endpoint        = params.get("-b", "http://localhost:41184");
	api_token            = params.get("--token", "");
	assert base_endpoint != "", "\033[31mBase endpoint cannot be empty...\033[m";
	assert api_token != "", "\033[31mToken must be provided...\033[m";
	notes                = retrieve_notes(base_endpoint, api_token);
	for note in notes:
		if all(len(re.findall(x, note["body"])) > 0 for x in keywords):
			print(note["title"]);
