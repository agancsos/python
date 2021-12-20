###############################################################################
# Name        : gmail_scanner.py                                              #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0.0                                                    #
# Description : Cleans spam from GMAIL.                                       # 
###############################################################################
import os, sys, threading, time, datetime, json;
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

class ScanRecord:
	title=None;message=None;flagged_words=None;
	def __init__(self, title, message, words): self.title = title; self.message = message; self.flagged_words = words;
class ScanSet:
	w_records=None;s_records=None;
	def __init__(self): self.w_records = []; self.s_records = [];
	pass;
class GmailScanner:
	user_file=None;g_service=None;threads=None;debug=None;interval_seconds=None;scopes=None;credentials=None;service=None;
	w_keywords=None;s_keywords=None;output_format=None;credentials_file=None;purge=None;
	def __init__(self, params=dict()):
		## It's suggested to set the following for the OAUTHLIB_RELAX_TOKEN_SCOPE environment variable. export OAUTHLIB_RELAX_TOKEN_SCOPE="https://www.googleapis.com/auth/gmail.modify https://mail.google.com"
		self.scopes = ["https://www.googleapis.com/auth/gmail.modify", "https://mail.google.com"];
		if "-f" in params.keys(): self.read_config(params["-f"]);
		self.output_format = params["-o"].upper() if "-o" in params.keys() else "LIST";
		self.purge = True if "--purge" in params.keys() and int(params["--purge"]) > 0 else False;
		self.user_file = params["-u"] if "-u" in params.keys() else self.user_file;
		self.service = True if "-d" in params.keys() and int(params["-d"]) > 0 else False;
		self.debug = True if "--debug" in params.keys() and int(params["--debug"]) > 0 else self.debug;
		self.interval_seconds = int(params["-t"]) if "-t" in params.keys() else 30;
		self.threads=list();
	def read_config(self, path):
		raw="";
		with open(path, "r") as fh: raw = fh.read(); 
		raw_config = json.loads(raw);
		self.user_file = raw_config["userFile"]; self.credentials_file = raw_config["credentialsFile"];
		self.debug = True if int(raw_config["debugMode"]) > 0 else False;
		self.w_keywords = raw_config["warningKeywords"]; self.s_keywords = raw_config["severeKeywords"];
		self.interval_seconds = int(raw_config["intervalSeconds"]);
	def scan(self):
		result = ScanSet();
		self.g_service = build("gmail", "v1", credentials=self.credentials);
		rsp = self.g_service.users().messages().list(userId="me").execute();
		for x in rsp["messages"]: 
			rsp2 = self.g_service.users().messages().get(userId="me", id=x["id"], format="full").execute();
			temp_subject = "NOT FOUND";
			for y in rsp2["payload"]["headers"]:
				if y["name"] == "Subject": temp_subject = y["value"]; break;
			if any(y in x["snippet"] for y in self.s_keywords): 
				result.s_records.append(ScanRecord(temp_subject, x, []));
			if not any(y.message["id"] == x["id"] for y in result.s_records) and any(y in x["snippet"] for y in self.w_keywords):
				result.w_records.append(ScanRecord(temp_subject, x, []));
		if self.purge:
			for x in result.s_records: self.g_service.users().messages().delete(userId="me", id=x.message["id"]).execute();
		return result;
	def build_html(self, raw):
		rsp = "<html><head><meta name='author' content='Abel Gancsos'/><meta name='auto-purge' content='{0}'/><title>GMailScanner Report {1}</title>".format(self.purge, datetime.datetime.today());
		rsp += "<style>* {margin:0;padding:0;border:0;} html {width:100%; height:100%;} table { width: 100%; border-collapse:collapse;} th,td { background-color: black; color: white; \
			text-align:left; vertical-align:top; border:2px solid white; } th { height: 40px; font-size: 16pt; } center { font-size: 8pt; }</style></head><body><table>";
		rsp += "<tr><th>Title</th><th>Flagged Words</th></tr>";
		for x in raw.s_records: rsp += "<tr style='background-color:rgb(50, 0, 0);'><td>{0}</td><td>{1}</td></tr>".format(x.title, ",".join(x.flagged_words));
		for x in raw.w_records: rsp += "<tr style='background-color:rgb(204,204,0);'><td>{0}</td><td>{1}</td></tr>".format(x.title, ",".join(x.flagged_words));
		rsp += "</table><center>&copy; {0} Abel Gancsos <br/>All Rights Reserved</center></body></html".format(datetime.datetime.today().year);
		return rsp;
	def invoke_service(self):
		while True:
			t = threading.Thread(target=self.scan);
			self.threads.append(t);
			t.start();
			for t in self.threads: t.join();
			time.sleep(self.interval_seconds);
	def invoke(self):
		if os.path.exists(self.user_file): self.credentials = Credentials.from_authorized_user_file(self.user_file, self.scopes);
		if not self.credentials or not self.credentials.valid:
			if self.credentials and self.credentials.expired and self.credentials.refresh_token: self.credentials.refresh(Request());
			else:
				flow2 = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.scopes); 
				flow2.run_local_server();
				self.credentials = flow2.credentials;
				with open(self.user_file, "w") as fh: fh.write(self.credentials.to_json());
		if self.service: self.invoke_service();
		else:
			assert self.output_format != "", "Output format cannot be empty...";
			assert self.output_format in ["JSON", "HTML", "LIST"], "Unsupported output format...";
			rsp = self.scan();
			if self.output_format == "JSON": print(json.dumps(rsp));
			elif self.output_format == "HTML": print(self.build_html(rsp));
			elif self.output_format == "LIST":
				for x in rsp.w_records: print("{0}\tWARNING".format(x.title));
				for x in rsp.s_records: print("{0}\tSEVERE".format(x.title));
	pass;

if __name__ == "__main__":
	params = dict();
	for i in range(0, len(sys.argv) - 1): params[sys.argv[i]] = sys.argv[i + 1];
	session = GmailScanner(params);
	session.invoke();

