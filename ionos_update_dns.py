#!/usr/bin/env python3
###############################################################################
# Name       : ionos_update_dns.py                                            #
# Author     : Abel Gancsos                                                   #
# Version    : v. 1.0.0.0                                                     #
# Description: Helps update IONOS DNS entries.                                #
###############################################################################
import os, sys, logging, requests, json;
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");
log = logging.getLogger(__name__);
from urllib3.exceptions import InsecureRequestWarning;
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning);

if __name__ == "__main__":
	params               = {};
	for i in range(0, len(sys.argv) - 1):
		params[sys.argv[i]] = sys.argv[i + 1];
	config_file          = params.get("-f", "{0}/.ionos.json".format(os.environ["HOME"]));
	zone_name            = params.get("-z", "");
	dryrun               = False if "--dry" in params.keys() and int(params["--dry"]) < 1 else True;
	target_ip            = params.get("--ip", "");
	excluded_zones       = params.get("--exclude", "").split(",");
	if any(x == "" for x in excluded_zones): excluded_zones.remove("");
	assert os.path.exists(config_file), "\033[31Configuration file must exist...\033[m";
	config               = {};
	with open(config_file, "r") as fh: config = json.loads(fh.read());
	api_key              = "{0}.{1}".format(config["publicPrefix"], config["secret"]);
	zones                = requests.get("https://api.hosting.ionos.com/dns/v1/zones", verify=False, headers={ "X-API-KEY": api_key }).json();
	if not any(x["name"] == zone_name for x in zones):
		log.warning("\033[33mNo zones with name '{0}'\033[m".format(zone_name));
		exit(1);
	zone                 = next(x for x in zones if x["name"] == zone_name);
	zone                 = requests.get("https://api.hosting.ionos.com/dns/v1/zones/{0}?suffix={1}&recordType=A".format(zone["id"], zone_name), verify=False, headers={ "X-API-KEY": api_key }).json();
	to_update_list       = [];
	for record in zone["records"]:
		if "ftp" in record["name"] or ("www" in record["name"] and record["name"] != "www.{0}".format(zone_name)): continue;
		if record["name"] in excluded_zones: continue;
		if record["content"] != target_ip:
			record["content"] = target_ip;
			to_update_list.append(record);
	if len(to_update_list) > 0:
		log.info("Updating zones: {0}".format(json.dumps(to_update_list, indent=4)));
		if not dryrun:
			rsp = requests.patch("https://api.hosting.ionos.com/dns/v1/zones/{0}".format(zone["id"]),
				verify=False, headers={
					"X-API-KEY": api_key
			}, data=json.dumps(to_update_list)).json();
			assert rsp.status_code == 200, "\033[31mFailed to update DNS entries...\033[m";

