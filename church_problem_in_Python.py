#!/bin/python
import sys

class CHURCH_PROBLEM:
 function_str=\"\";
 max_iter=0;
 def calculate_numerals(self):
  i=0;
  j=0;
  final=int(self.function_str[0]);
  final_str=str(final)+\"0\";
  while (i < int(self.max_iter)):
   while (j< len(self.function_str)-1):
    buffer=self.function_str[j];
    next_char=self.function_str[j+1];
    ##Go through string with buffer
    if buffer is \"+\":
     final+=int(next_char);
     final_str+=str(final);
     final_str+=\"0\";
    elif buffer is \"-\":
     final-=int(next_char);
     final_str+=str(final);
     final_str+=\"0\";
    elif buffer is \"*\":
     final*=int(next_char);
     final_str+=str(final);
     final_str+=\"0\";
    elif buffer is \"/\":
     final/=int(next_char);
     final_str+=str(final);
     final_str+=\"0\";
    j+=1;
   i+=1;
  return final_str;

if(len(sys.argv) > 1):
 user_defined_function=sys.argv[1];
 user_defined_max=sys.argv[2];
 test_church=CHURCH_PROBLEM();
 test_church.function_str=user_defined_function;
 test_church.max_iter=user_defined_max;
 print \"===============================================\";
 print \"Function: \",user_defined_function;
 print \"Iterations: \",user_defined_max;
 print \"Final Church: \",test_church.calculate_numerals();
 print \"===============================================\";
else:
 print \"No information passed...\";

