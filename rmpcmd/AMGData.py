###############################################################################
# Name       : AMGData                                                        #
# Author     : Abel Gancsos                                                   #
# Version    : v. 1.0.0                                                       #
# Description:                                                                #
###############################################################################
import sys;
import os;
import sqlite3;

"""
	This class is a simple wrapper for the SQLite database.
"""
class AMGData:
	file_path = "";
	db_handler = None;
	db_cursor = None;

	"""
		This method initializes a new isntance of the class.
	"""	
	def __init__(self,path):
		self.file_path = path;
		pass;

	"""
		This method opens the SQLite database.
	"""
	def connect(self):
		if(os.path.exists(self.file_path)):
			self.db_handler = sqlite3.connect(self.file_path);
			self.db_cursor = self.db_handler.cursor();
		else:
			print("File does not exist...");
		pass;

	"""
		This method runs a query against the database.
	"""
	def run_query(self,query):
		self.connect();
		try:
			self.db_cursor.execute(query);
			self.db_handler.commit();
		except e:
			pass;
		self.db_handler.close();
		return False;

	"""
		This method looks up the database via the provided query.
	"""
	def query(self,query):
		self.connect();
		final_results = list();
		self.db_cursor.execute(query);
		for table_row in self.db_cursor.fetchall():
			final_results.append(table_row);
			pass;
		self.db_handler.close();
		return final_results;
	pass;
