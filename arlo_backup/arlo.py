#!/bin/python
import os;
import sys;
from datetime import datetime;
from datetime import timedelta;
import requests;
 
class ArloCameraService:
	base_endpoint_url = "";
	target_path = "";
	delete = False; 
	username = "";
	password = "";
	token = "";

	def __init__(self):
		self.base_endpoint_url = "https://arlo.netgear.com/hmsweb/";
	def day_folder(self):
		yesterday = datetime.now() + timedelta(days=-1);
		return "{0}/{1}/{2}/{1}{2}{3}".format(self.target_path,
			yesterday.year,
			str(yesterday.month).rjust(2,"0"),
			str(yesterday.day).rjust(2,"0"));
	def login(self):
		url = "{0}/login/v2".format(self.base_endpoint_url);
		request = {"email":self.username,"password":self.password};
		response = requests.post(url, json=request);
		if(response.status_code != 200):
			raise ApplicationError("Request failed...");
		self.token = response.json()['data']['token'];
		return True;
	def get_recordings(self):
		recordings = list();
		url = "{0}/users/library/".format(self.base_endpoint_url);
		yesterday = datetime.now() + timedelta(days=-1);
		request = {
			"dateFrom":"{0}{1}{2}".format(yesterday.year,str(yesterday.month).rjust(2,"0"),str(yesterday.day).rjust(2,"0")), 
			"dateTo":"{0}{1}{2}".format(yesterday.year,str(yesterday.month).rjust(2,"0"),str(yesterday.day).rjust(2,"0"))
		};
		response = requests.post(url, headers={'Content-Type':'application/json', 'Authorization': self.token}, json=request);
		if(response.status_code != 200):
			raise ApplicationError("Request failed...");
		recordings = response.json()['data'];
		return recordings;
	def delete(self, recording):
		pass;
	def backup(self):
		self.target_path = self.target_path;
		print(self.day_folder())
		if(self.login()):
			if(os.path.exists(self.target_path)):
				print("Backing up...");
				if(not os.path.exists(self.day_folder())):
					os.makedirs(self.day_folder());
				## List recordings on Arlo cloud
				recordings = self.get_recordings();
				for recording in recordings:
					print("Downloading: {0}".format(recording.name));
					## Download to target
					os.system("curl {0} -o {1}/{2}.mp4".format(recording.presignedContentUrl,self.day_folder(), recording.name));  
					## Delete from cloud
					if(self.delete):
						self.delete(recording);
			else:
				raise Exception("Target path does not exist....");
		else:
			print("Failed to login....");
	pass;

if __name__ == "__main__":
	session = ArloCameraService();
	if(len(sys.argv) > 0):
		for param_i in range(0, len(sys.argv)):
			if(sys.argv[param_i] == "-url"):
				session.base_endpoint_url = sys.argv[param_i + 1];
			elif(sys.argv[param_i] == "-user"):
				session.username = sys.argv[param_i + 1];
			elif(sys.argv[param_i] == "-pass"):
				session.password = sys.argv[param_i + 1];
			elif(sys.argv[param_i] == "-p"):
				session.target_path = sys.argv[param_i + 1];
			elif(sys.argv[param_i] == "-del"):
				session.delete = True;
	session.backup();
	pass;
