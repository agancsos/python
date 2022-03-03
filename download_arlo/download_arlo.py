#!/usr/bin/env python3
###############################################################################
# Name        : download_arlo.py                                              #
# Version     : v. 1.0.0.0                                                    #
# Author      : Abel Gancsos                                                  #
# Description : Downloads recordings from Arlo for archiving.                 #
###############################################################################
import base64, os, sys, requests_html, subprocess, shutil, time;
class Downloader:
	base_endpoint=None;target_path=None;start_date=None;end_date=None;debug=None;username=None;password=None;token=None;headers=None;session=None;mfa_id=None;userid=None;factor_code=None;
	def __init__(self, params=dict()):
		self.start_date    = params['--start'] if '--start' in params.keys()                   else "";
		self.end_date      = params['--end']   if '--end'   in params.keys()                   else "";
		self.base_endpoint = params['-b']      if '-b'      in params.keys()                   else "https://myapi.arlo.com/hmsweb";
		self.target_path   = params['-t']      if '-t'      in params.keys()                   else "";
		self.password      = str(base64.b64encode(params['-p'].encode("utf-8")), "utf-8") if '-p' in params.keys() else "";
		self.username      = params['-u']      if '-u'      in params.keys()                   else "";
		self.debug         = True if "--debug" in params.keys() and int(params['--debug']) > 0 else False;
		self.session       = requests_html.HTMLSession(verify=True);
		self.headers       = { \
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36', "dnt":"1", \
			"authority":"ocapi-app.arlo.com", "Upgrade-Insecure-Requests": "1", "Referer":"https://my.arlo.com/", "source":"arloCamWeb",\
			 "Origin":"https://my.arlo.com", "Host":"ocapi-app.arlo.com", "Auth-Version":"2"};
	def auth(self):
		endpoint = "https://ocapi-app.arlo.com/api/auth";
		rsp = self.session.post(endpoint, json={"email":self.username, "password":self.password, "EnvSource":"prod", "language":"en"}, headers=self.headers);
		self.token = rsp.json()["data"]["token"];
		self.userid = rsp.json()["data"]["userId"];
		self.headers["Authorization"] = str(base64.b64encode(self.token.encode("utf-8")), "utf-8");
		rsp = self.session.get(endpoint.replace("auth", "getFactors") + "?data%20={0}".format(rsp.json()["data"]["authenticated"]), headers=self.headers);
		self.mfa_id = next(x for x in rsp.json()["data"]["items"] if x["factorType"] == "EMAIL")["factorId"];
		rsp = self.session.post(endpoint.replace("auth", "startAuth"), json={"factorId":self.mfa_id}, headers=self.headers);
		self.factor_code = rsp.json()["data"]["factorAuthCode"];
		mfa_code = input("MFA Code: ");
		rsp = self.session.post(endpoint.replace("auth", "finishAuth"), json={"factorAuthCode":self.factor_code, "otp":"{0}".format(mfa_code)}, headers=self.headers);
		self.token = rsp.json()["data"]["token"];
		self.headers["Authorization"] = str(base64.b64encode(self.token.encode("utf-8")), "utf-8");
		rsp = self.session.get(endpoint.replace("auth", "validateAccessToken?data={0}".format(int(time.time()))), headers=self.headers);
		self.headers["Authorization"] = self.token;
		self.headers["Host"] = "myapi.arlo.com";
		rsp = self.session.get("https://myapi.arlo.com/hmsweb/users/session/v3?time={0}".format(int(time.time())), headers=self.headers);
	def list_recordings(self, device): print(device["deviceName"]);
	def list_devices(self):
		endpoint = "{0}/v2/users/devices".format(self.base_endpoint);
		rsp = self.session.get(endpoint, headers=self.headers, allow_redirects=False);
		return rsp.json()["data"];
	def download(self, recording): return False;
	def remove_recording(self, recording): return False;
	def invoke(self):
		assert self.base_endpoint != "", "Base endpoint cannot be empty...";
		assert self.username      != "", "Username cannot be empty...";
		assert self.password      != "", "Password cannot be empty...";
		self.auth();
		if self.token != None:
			for device in self.list_devices():
				for recording in self.list_recordings(device):
					if self.download(recording):
						self.remove_recording(recording);
	pass;

if __name__ == "__main__":
	params = dict();
	for x in range(1, len(sys.argv[1:]), 2) : params[sys.argv[x]] = sys.argv[x + 1];
	session = Downloader(params);
	session.invoke();
	pass;

