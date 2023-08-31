###############################################################################
# Name       : battery_profiler.py                                            #
# Author     : Abel Gancsos                                                   #
# Version    : v. 1.0.0.0                                                     #
# Description: Helps determine battery life.                                  #
###############################################################################
import datetime, os, sys, subprocess, platform, logging;
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");
log = logging.getLogger(__name__);

def get_last_startup(platform):
	rst = "";
	if "macOS" in platform or "Linux" in platform:
		rst = subprocess.run(["bash", "-c", "last reboot"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode();
		rst = rst.split("\n")[0].split("~")[1].strip();
		rst = datetime.datetime.strptime("{0} {1}".format(rst, datetime.datetime.now().year), "%a %b %d %H:%M %Y");
	else:
		rst = subprocess.run(["powershell", "-c", "Get-WinEvent -FilterHashtable @{logname='System';'id'=6005}|Select TimeCreated"],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode();
		rst = rst.split("\n")[3].strip();
		rst = datetime.datetime.strptime(rst, "%m/%d/%Y %I:%M:%S %p");
	return rst;

def get_last_shutdown(platform):
	rst = "";
	if "macOS" in platform or "Linux" in platform:
		rst = subprocess.run(["bash", "-c", "last shutdown"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode();
		rst = rst.split("\n")[0].split("~")[1].strip();
		rst = datetime.datetime.strptime("{0} {1}".format(rst, datetime.datetime.now().year), "%a %b %d %H:%M %Y");
	else:
		rst = subprocess.run(["powershell", "-c", "Get-WinEvent -FilterHashtable @{logname='System';'id'=1074}|Select TimeCreated"],
			stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode();
		rst = rst.split("\n")[3].strip();
		rst = datetime.datetime.strptime(rst.split(".")[0], "%m/%d/%Y %I:%M:%S %p");
	return rst;

if __name__ == "__main__":
	params               = {};
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	boot_time     = get_last_startup(platform.platform());
	shutdown_time = get_last_shutdown(platform.platform());
	log.info("\033[35mLast Startup : {0}\033[m".format(boot_time));
	log.info("\033[35mLast Shutdown: {0}\033[m".format(shutdown_time));
	duration   = (shutdown_time - boot_time).total_seconds() / 60 / 60;
	t_duration = ((datetime.datetime.now() - boot_time).total_seconds() / 60 / 60 / 24 / 7);
	log.info("\033[36mLifetime     : {0:0.2f} hours\033[m".format(duration));
	# Ideally, on a PC (mac or Windows), you really should reboot once a week to clear the buffers, but after 2 weeks, you're asking for trouble.
	if duration == 0.0 and t_duration > 2:
		log.info("\033[42m{0:0.2f} weeks, impressive! You can reboot now...\033[m".format(t_duration));

