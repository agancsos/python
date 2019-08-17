#!/bin/python

## Acts as an enum class for the TestCase status
class Status:
	NONE = 0;
	NEW = 1;
	EXECUTING = 2;
	SUCCEEDED = 3;
	FAILED = 4;
   
	def get_name(self, status):
		if status == 0:
			return "None";
		elif status == 1:
			return "New";
		elif status == 2:
			return "Executing";
		elif status == 3:
			return "Succeeded";
		elif status == 4:
			return "Failed";
		pass;
	pass;
