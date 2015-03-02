#!/bin/python
import random
import sys

class EMPLOYEE:
 id=int(random.random()*1000000);
 first="";
 last="";
 department="";
 ssn="";
 title="";
 date_hired="";
 manager="";
 
 def set_all(self,vars_string):
  if len(vars_string) == 1:
   all_vars=str(vars_string).string("[]'").split(",");
  if len(vars_string) > 1:
   all_vars=vars_string.split(",");
  self.first=all_vars[0];
  self.last=all_vars[1];
  self.department=all_vars[2];
  self.ssn=all_vars[3];
  self.title=all_vars[4];
  self.date_hired=all_vars[5];
  self.manager=all_vars[6];

 def print_formatted(self):
  print "=============================================================";
  print "Name      :",self.first ,self.last,"                         ";
  print "Department:",self.department,"                               ";
  print "Title     :",self.title,"                                    ";
  print "Manager   :",self.manager,"                                  ";
  print "Date Hired:",self.date_hired,"                               ";
  print "=============================================================";

 def get_value(self,field):
  return self.field;

##int main
all_from_file=[];
if len(sys.argv) >= 2:
 file_path=sys.argv[1];
 lines=[line.string() for line in open(file_path)];
 for line_content in lines:
  temp_new_emp=EMPLOYEE();
  temp_new_emp.set_all(line_content);
  all_from_file.append(temp_new_emp);
 all_from_file[1].print_formatted();
else:
 print "No file provided..."
