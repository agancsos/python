#!/bin/python
import random;
import os;
import sys;
sys.path.insert(0, "../src");
from status import *;

## Test engine that runs the Test Case to validate a feature
class TestRun:
	id		   = random.randint(1, 999999999);
	test_case	= None;
	status	   = Status.NONE;
	exit_code	= 0;
	created_time = None;
	end_time = None;
	
	def __init__(self, test=None):
		self.test_case = test;
		pass;

	## Performs the steps needed to run the Test Case
	def run(self):
		self.status = Status.EXECUTING;
		self.create_time = datetime.now();
		try:
			self.test_case.invoke();
			self.status = Status.SUCCEEDED;
		except Exception:
			self.status = Status.FAILED;
		self.end_time = datetime.now();
		pass;
	pass;
