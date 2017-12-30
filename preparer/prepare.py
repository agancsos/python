###############################################################################
## Name        : prepare											    	  #
## Author      : Abel Gancsos												  #
## Date        : December 30, 2017 											  #
## Version     : v. 1.0.0													  #
## Description :                 											  #
###############################################################################

#!/bin/python
import os;
import sys;

"""
	This class helps prepare directories for videos
"""
class PREPARER:
	max_seasons = "1";
	season_value = "1";
	disk_count = "3";
	silent = True;

	'''
		This is the common constructor
		@param ms Value to be set for max seasons
		@param sv Value to be set for the initial season
		@param dc Value to be set for the disk count
		@param s Value to be set for the silent option
	'''
	def __init__(self,ms,sv,dc,s):
		self.max_seasons = ms;
		self.season_value = sv;
		self.disk_count = dc;
		self.silent = s;

	'''
		This method prepares the directories
	'''
	def prepare(self):
		## Dump configuration
		if not self.silent:
			print("Preparing directory...");
			print("Max Seasons  : {0}".format(self.max_seasons));
			print("Start Seasons: {0}".format(self.season_value));
			print("Disk Count   : {0}".format( self.disk_count));
		try:
			for season_index in range(int(self.season_value),int(self.season_value) + int(self.max_seasons)):
				if not self.silent:
					print("Creating season {0}".format(season_index));
				if not os.path.exists("./SEASON_{0}".format(season_index)):
					os.mkdir("./SEASON_{0}".format(season_index));
				if not self.silent:
					print("Preparing disks for season {0}".format(season_index));
				for disk_index in range(int(self.disk_count)):
					if not self.silent:
						print("Creating disk {0} for season {1}".format(disk_index + 1,season_index));
					if not os.path.exists("./SEASON_{0}/DISK_{1}".format(season_index,disk_index + 1)):
						os.mkdir("./SEASON_{0}/DISK_{1}".format(season_index,disk_index + 1));
					pass;
				pass;
			pass;
		except Exception as e:
			print e;
			pass;

'''
	Main entry point from the command-line
'''
if __name__ == "__main__":

	max = "1";
	value = "1";
	disks = "3";
	silent = False;

	## Loop through command-line parameters
	if(len(sys.argv) > 1):
		for arg_index in range(len(sys.argv)):
			if(sys.argv[arg_index] == "-max"):
				max = sys.argv[arg_index + 1];
			elif(sys.argv[arg_index] == "-season"):
				value = sys.argv[arg_index + 1];
			elif(sys.argv[arg_index] == "-disks"):
				disks = sys.argv[arg_index + 1];
			elif(sys.argv[arg_index] == "-silent"):
				silent = True;
			pass;
		pass;
	session = PREPARER(max,value,disks,silent);
	session.prepare();
	pass;
