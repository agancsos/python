#!/usr/bin/env python3
import os, sys, logging, sqlite3, zlib, re;

class AppleNote:
	def __init__(self, title="", path="", md_content="", link=""):
		self.title     = title;
		self.full_path = path;
		self.content   = md_content;
		self.link      = link;

class DBService:
	def __init__(self, path):
		assert path != "" and os.path.exists(path), "Notes database must exist and cannot be empty...";
		self.client = sqlite3.connect(path);
	def service_query(self, query):
		cursor = self.client.cursor();
		cursor.execute(query);
		rst    = [];
		cols   = cursor.description
		rows   = cursor.fetchall();
		for row in rows:
			temp = {};
			i = 0;
			for col in cols:
				temp[col[0]] = row[i];
				i += 1;
			rows.append(temp);
		cursor.close();
		return rst;
	def run_service_query(self, query, commit=True):
		cursor = self.client.cursor();
		cursor.execute(query);
		if commit: self.client.commit();
		cursor.close();

class MigrationService:
	def __init__(self, path):
		self.dbs       = DBService(path);
		self.note_objs = [];
	def extract_full_path(self, identifier):
		rst    = "";
		rsp    = self.dbs.service_query("select ztitle2, zparent from ZICCLOUDSYNCINGOBJECT where z_pk = '{0}'".format(identifier));
		for folder_row in rsp:
			rst += folder_row["ztitle2"];
			if folder_row["zparent"] != None:
				rst = "{0}/{1}".format(extract_full_path(client, folder_row["zparent"]), rst);
		return rst;
	def parse_table(self, row, col_count=2):
		rst = "";
		col_i = 0;
		row_i = 0;
		comps = row.split("\n");
		for comp in comps:
			if col_i == col_count:
				rst += "|\n";
				if row_i == 0:
					rst += "|";
					for i in range(0, col_count): rst += "-|";
					rst += "\n";
				col_i = 0;
				row_i += 1;
			if comp.strip() != "" and row_i < len(comps):
				rst += "|{0}".format(comp.strip());
			col_i += 1;
		return rst.replace("|\n|\n", "|\n");

	def clean_data(self, raw, attachments=[], increase_indents=False):
		cleaned_raw = re.sub(r"[^\x00-\x7f]",r"", str(zlib.decompress(raw[0], 32)).replace("com.apple.notes.table", "<TABLE>").replace("\\n", "\n"));
		cleaned_raw = cleaned_raw.replace(r"\xef\xbf\xbc", "<TABLE>");
		cleaned_raw = cleaned_raw.replace(r"\x12\xbe\x01", "");
		for x in r"\x08,\x00,\x12,\xf5,\x08,\x00,\x10,\x00,\x1a,\xee".split(","):
			cleaned_raw = cleaned_raw.replace(x, "");
		cleaned_raw = cleaned_raw.replace(r"b'", "");
		cleaned_raw = cleaned_raw.replace(r"\'", "'");
		cleaned_raw = re.sub(r"\\x04[^']*", "", cleaned_raw, re.MULTILINE);
		cleaned_raw = cleaned_raw.replace("'", "");
		if increase_indents:
			cleaned_raw = re.sub("#", "##", cleaned_raw, re.MULTILINE);
		if "<TABLE>" in cleaned_raw:
			table_i = 0;
			for t in [x[1] for x in attachments if x[0] == "com.apple.notes.table"]:
				cleaned_raw = cleaned_raw.replace("<TABLE>", parse_table(t), 1);
			table_i += 1;
		return cleaned_raw;

if __name__ == "__main__":
	pass;
