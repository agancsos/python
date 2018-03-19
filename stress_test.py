###############################################################################
# Name        : stress_test                                                   #
# Author      : Abel Gancsos                                                  #
# Version     : v. 1.0.0                                                      #
# Create Date : 03/18/2018                                                    #
###############################################################################

#!/bin/python
import os;
import sys;
import time;
import threading;

"""
	This class helps to generate a load on the current system
"""
class AMGStress:

	max_threads   = 500;
	sleep_seconds = 30;
	results = list();
	max_index = 50000000;

	'''
		This is the constructor
	'''
	def __init__(self):
		pass;

	'''
		This is the public entry point to the class
	'''
	def run(self):
		threads = list();

		'''
			CPU test
		'''
		for thread_index in range(0,self.max_threads):
			new_thread = threading.Thread(target=self.runnable,name=("Thread " + str(thread_index)));
			new_thread.start();
			threads.append(new_thread);

		for thread_cursor in threads:
			thread_cursor.join();
		pass;
	
	'''
		This method performs read operations in each thread
	'''
	def runnable(self):
		print("Current Thread: " + str(threading.currentThread().name));
		for temp_cursor in range(1,self.max_index):
			for array_index in range(0,len(self.results)):
				self.results.add(1 + temp_cursor * self.results[array_index]);
			pass;
		pass;
	pass;

"""
	This is the main script block used to setup the load test environment
"""
if __name__ == "__main__":
	session = AMGStress();
	if(len(sys.argv) > 1):
		for arg_cursor in range(0,len(sys.argv)):
			if(sys.args[arg_cursor] == "-threads"):
				session.max_threads = sys.argv[arg_cursor + 1];
			pass;
	session.run();
	pass;
