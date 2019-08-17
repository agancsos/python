#!/bin/python
import os;
import sys;
from datetime import datetime;
import re;
import random;
from bootstrapservice import *;

## Acts as the main Test Suite engine 
class TestSuite:
	success_test_runs = list();
	failure_test_runs = list();
	test_runs = list();
	
	def __init__(self):
		pass;
	
	## Adds a Test Run for each Test Case
	def initialize(self):
		for test_class in Bootstraper.classes.itervalues():
			class_object = test_class();
			self.test_runs.append(class_object);
			pass;
		pass;
	
	## Runs all Tests Cases in the loaded Test Suite
	def run(self):
		self.initialize();
		for test_run in self.test_runs:
			try:
				test_run.invoke();
				self.success_test_runs.append(test_run);
			except Exception as e:
				print(e);
				self.failure_test_runs.append(test_run);
			pass;
		print("Test Coverage: " + str(len(self.success_test_runs)/(len(self.success_test_runs) + len(self.failure_test_runs)) * 100) + "%");
		pass;
	pass;
