#!/usr/bin/env python3
###############################################################################
# Name        : extract_amazon_books.py                                       #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description :                                                               #
###############################################################################
import os, sys, logging, re;
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");
if __name__ == "__main__":
	params                    = {};
	for i in range(0, len(sys.argv) - 1): params[sys.aargv[i]] = sys.argv[i + 1];
	logger                    = logging.getLogger(__file__);
	html_extract_path         = params["-p"] if "-p" in params.keys() else "{0}/Downloads/books.html".format(os.environ["HOME"]);
	logger.info(html_extract_path);
	raw_html_content          = "";
	with open(html_extract_path, "r") as fh: raw_html_content = fh.read();
	ms                        = re.findall("\"B[^\.]+/?action=21\"", raw_html_content, re.MULTILINE);
	for m in ms:
		comps = m.split(",");
		if len(comps) == 2:
			logger.info(comps[0].replace('"', ""));

