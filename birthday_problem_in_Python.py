#!/bin/python
import sys

class birthday_problem:
 max_people=23;
 def get_probability(self):
  i=1;
  final=1;
  while i < int(self.max_people):
   final=rount(float(final*(1.0-float(float(1)/365.0))),4);
   i+=1;
  return final;
 final_probability=24.0;
 final_value=final_probability * 100.0;
 def refresh(self):
  i=1;
  final=1;
  while i < int(self.max_people):
   final=round(float(final*(1.0-float(float(i)/365.0))),4);
   i+=1;
   self.final_probability=final;
   self.final_value=self.final_probability * 100.0;
 def set(self,user_defined_max):
   self.max_people=user_defined_max;
   self.refresh();

max_people=sys.argv[1];
test_birthday=birthday_problem();
test_birthday.set(max_people);
test_birthday.max_people=int(max_people);
print \"=========================================================================\";
print \"Number of people: \",test_birthday.max_people;
print \"Birhday probability: \",test_birthday.final_probability;
print \"Final Percentage Value: \",test_birthday.final_value,\"%\";
print \"=========================================================================\";
