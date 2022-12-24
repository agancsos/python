#!/usr/bin/env python3
###############################################################################
# Name        : hunter.py                                                     #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Helps to find and report scam/spam callers.                   #
###############################################################################
import os, sys, logging, requests, json, re;
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");
log = logging.getLogger(__file__);

class HunterHelpers:
	BASE_LOOKUP_URL    = "https://www.reversephonelookup.com/number";
	BASE_REPORT_URL    = "https://api.ftc.gov/v0/dnc-complaints?api_key=DEMO_KEY";
	def extract_owner_info(number):
		client   = requests.Session();
		rsp      = client.get("{0}{1}/".format(HunterHelpers.BASE_LOOKUP_URL, number), headers={
			"User-Agent": "PostmanRuntime/7.26.8"
		}, allow_redirects=False);
		rsp      = client.get("{0}/{1}/".format(HunterHelpers.BASE_LOOKUP_URL, number), headers={
			"User-Agent": "PostmanRuntime/7.26.8",
			"Cookie": "PHPSESSID={0}".format(client.cookies["PHPSESSID"])
		});
		rst      = {
			"number": number,
			"owner": "NA",
			"provider": "NA",
			"isVOIP": False,
			"needsReport": False
		};
		raw_info = None;
		ms       = re.findall("\<li\>.*\</li\>", rsp.content.decode());
		if len(ms) == 0: return rst;
			rst["provider"]    =  ms[5].split("<strong>")[1].replace("</strong></li>", "");
			rst["isVOIP"]      =  True if "voip" in ms[4].split("<strong>")[1].replace("</strong></li>", "").lower() else False;
			rst["needsReport"] =  rst["isVOIP"];
		};
		return rst;
	def report_number(owner_info):
		client = requests.Session();
		return client.post(HunterHelpers.BASE_REPORT_URL, headers={
			"User-Agent": "PostmanRuntime/7.26.8"
		}, json={
			"company-phone-number": str(owner_info["number"]),
			"created-date": "",
			"violation-date": "",
			"consumer-city": "",
			"consumer-state": "NJ",
			"consumer-area-code": "973",
			"subject": "Dropped call or no message",
			"recorded-message-or-robocall": "Y"
		});

if __name__ == "__main__":
	params               = {};
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	input_path = params["-f"] if "-f" in params.keys() else None;
	numbers    = params["--numbers"].split(",") if "--numbers" in params.keys() else [];
	if input_path and os.path.exists(input_path):
		log.info("\033[36mReading numbers file '{0}'\033[m".format(input_path));
		with open(input_path, "r") as fh: numbers = fh.readlines();
	for number in numbers:
		number = number.strip().replace("-", "").replace("(", "").replace(")", "").replace(" ", "");
		log.info("\033[36mScanning number: {0}\033[m".format(number));
		info = HunterHelpers.extract_owner_info(number);
		if info["needsReport"]:
			log.info("\033[31mNumber flagged.  Reporting....\033[m");
			HunterHelpers.report_number(info);

