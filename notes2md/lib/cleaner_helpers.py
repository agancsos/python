#!/usr/bin/env python3
import os, sys, zlib, re;

class CleanerHelpers:
	def parse_table(row, col_count=2):
		rst = "";
		raw_lines = row.split("\n");
		col_count = raw_lines.index(next(x for x in raw_lines if x == ""));
		if col_count == len(raw_lines) - 1:
			col_count = 2;
		col_i = 0;
		row_i = 0;
		for comp in raw_lines:
			if col_i == col_count:
				rst += "|\n";
				if row_i == 0:
					rst += "|";
					for i in range(0, col_count): rst += "-|";
					rst += "\n";
				col_i = 0;
				row_i += 1;
			if comp.strip() != "" and row_i < len(raw_lines):
				rst += "|{0}".format(comp.strip());
			col_i += 1;
		return rst.replace("|\n|\n", "|\n");

	def clean_data(raw, attachments=[], increase_indents=False):
		cleaned_raw = re.sub(r"[^\x00-\x7f]",r"", str(zlib.decompress(raw["zdata"], 32)).replace("\\n", "\n"));
		cleaned_raw = cleaned_raw.replace("b'", "");
		cleaned_raw = cleaned_raw.replace(r"\xef\xbf\xbc", "<TABLE>");
		cleaned_raw = re.sub(r"(\\x[0-9-a-z]{2})*", r"", cleaned_raw, re.MULTILINE);
		cleaned_raw = re.sub(r"\\x[^']*", r"", cleaned_raw, re.MULTILINE).replace("'", "");
		if increase_indents:
			cleaned_raw = re.sub("#", "##", cleaned_raw, re.MULTILINE);
		if "<TABLE>" in cleaned_raw:
			table_i = 0;
			for t in [x["zsummary"] for x in attachments if x["ztypeuti"] == "com.apple.notes.table"]:
				cleaned_raw = cleaned_raw.replace("<TABLE>", CleanerHelpers.parse_table(t), 1);
			table_i += 1;
		return cleaned_raw.lstrip();

if __name__ == "__main__":
	pass;
