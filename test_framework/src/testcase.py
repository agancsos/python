#!/bin/python
import random;

## Abstract class representing the object to be tested
class TestCase:
	id		  = random.randint(1, 999999999);
	name		= "";
	description = "";
	
	def __init__(self):
		pass;
	
	def invoke(self):
		raise NotImplementedError; 
	pass;

