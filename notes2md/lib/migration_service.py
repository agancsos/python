#!/usr/bin/env python3
import os, sys, logging, zlib, re;
from . import db_service;
from . import cleaner_helpers;
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level="INFO");
logger = logging.getLogger(__name__);

class AppleNote:
	def __init__(self, pk=0, title="", path="", md_content="", link=""):
		self.title     = title;
		self.full_path = path;
		self.content   = md_content;
		self.link      = link;
		self.z_pk      = pk;

class MigrationService:
	def __init__(self, path):
		self.dbs       = db_service.DBService(path);
		self.note_objs = [];
	def extract_full_path(self, identifier):
		rst    = "";
		rsp    = self.dbs.service_query("select ztitle2, zparent from ZICCLOUDSYNCINGOBJECT where z_pk = '{0}'".format(identifier));
		for folder_row in rsp:
			rst += folder_row["ztitle2"];
			if folder_row["zparent"] != None:
				rst = "{0}/{1}".format(self.extract_full_path(folder_row["zparent"]), rst);
		return rst;
	def migrate(self, note_name, dry=True, increase_indents=False, remove_title=False, base_output=""):
		notes = self.dbs.service_query("select zidentifier, ztitle1, zfolder, z_pk from ZICCLOUDSYNCINGOBJECT where ztitle1 is not null");
		for note in notes:
			if note_name == "" or note_name in note["ztitle1"]:
				folder = self.dbs.service_query("select ztitle2 from ZICCLOUDSYNCINGOBJECT where z_pk = '{0}'".format(note["zfolder"]))[0];
				note_obj           = AppleNote(title=note["ztitle1"]);
				note_obj.link      = "notes://showNote?identifier={0}".format(note["zidentifier"])
				note_obj.full_path = self.extract_full_path(note["zfolder"]);
				note_obj.z_pk      = note["z_pk"];
				logger.info("\033[35mExtracting: {0}/{1} ({2})\033[m".format(note_obj.full_path, note_obj.title, note_obj.z_pk));
				data = self.dbs.service_query("select zdata from ZICNOTEDATA where znote = '{0}'".format(note["z_pk"]))[0];
				attachments = self.dbs.service_query("select ZTYPEUTI, ZSUMMARY from ZICCLOUDSYNCINGOBJECT where znote = '{0}'".format(note["z_pk"]));
				note_obj.content   = cleaner_helpers.CleanerHelpers.clean_data(data, attachments, increase_indents);
				if remove_title: note_obj.content = note_obj.content.replace("{0}\n".format(note_obj.title), "").lstrip();
				note_obj.full_path = self.extract_full_path(note["zfolder"]);
				self.note_objs.append(note_obj);
				if not dry and base_output != "":
					os.makedirs("{0}/{1}".format(base_output, note_obj.full_path), exist_ok=True);
					with open("{0}/{1}/{2}.md".format(base_output, note_obj.full_path, note_obj.title), "w") as fh:
						fh.write(note_obj.content);
				else:
					print(note_obj.content);

if __name__ == "__main__":
	pass;
