#!/usr/bin/env python3
import os, sys, logging, sqlite3;

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
			if row == None or not isinstance(row, tuple): continue;
			for col in cols:
				temp[col[0].lower()] = row[i];
				i += 1;
			rst.append(temp);
		cursor.close();
		return rst;
	def run_service_query(self, query, commit=True):
		cursor = self.client.cursor();
		cursor.execute(query);
		if commit: self.client.commit();
		cursor.close();

if __name__ == "__main__":
	pass;
