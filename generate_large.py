#!/bin/python

import os;
import sys;
import sqlite3;

"""
	This class helps generate large SQLite databases
"""
class Generator:
	file_path = "";
	max_records = 0;
	max_columns = 0;
	db_handler  = None;
	db_cursor   = None;

	'''
		This is the default constructor
	'''
	def __init__(self):
		pass;

	'''
		This method creates the tables for the large database
	'''
	def create_tables(self):
		sql = "create table if not exists testing(id integer not null primary key autoincrement";
		if(self.max_columns > 0):
			for columns_index in xrange(1,int(self.max_columns),1):
				sql += ",";
				sql += ("field_" + str(columns_index) + " character default ''");
				pass;
			pass;
		sql += ")";
		self.db_cursor.execute(sql);
		self.db_handler.commit();
		pass;

	'''
		This method fills the data in the test database
	'''
	def fill_data(self):
		for row_index in xrange(1,int(self.max_records),1):
			self.db_cursor.execute("insert into testing default values");
			self.db_handler.commit();
			pass;
		pass;

	'''
		This method opens the SQLite database file and sets the cursor
	'''
	def connect(self):
		self.db_handler = sqlite3.connect(self.file_path);
		self.db_cursor = self.db_handler.cursor();
		pass;

	'''
		This method is the entry point for the class from the main block
	'''
	def run(self):
		try:
			self.connect();
			self.create_tables();
			self.fill_data();
			self.db_handler.close();
		except:
			pass;
		pass;

	pass;

"""
	This is the entry point to the script from the command-line
"""
if __name__ == "__main__":
	session = Generator();

	'''
		Sets the class attributes from the command-line
	'''
	if(len(sys.argv) > 1):
		for cmd_index in range(len(sys.argv)):
			if(sys.argv[cmd_index] == "-f"):
				session.file_path = sys.argv[cmd_index + 1];
			elif(sys.argv[cmd_index] == "-r"):
				session.max_records = sys.argv[cmd_index + 1];
			elif(sys.argv[cmd_index] == "-c"):
				session.max_columns = sys.argv[cmd_index + 1];
			pass;

		session.run();
		pass;
	else:
		print("You must specify a file path, max record count, and max column count....");
		pass;
	pass;
