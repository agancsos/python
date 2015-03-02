#!/bin/python
import sys

def fib_seq(max_fib):
 fibs=[];
 fibs.append(0);
 fibs.append(1);
 i=2;
 while i <= int(max_fib):
  fibs.append(int(fibs[i-1] + fibs[i-2]));
  i+=1;
 return fibs;

if len(sys.argv) > 1:
 if int(sys.argv[1]) > 1:
  my_fibs=fib_seq(sys.argv[1]);
  i=0;
  print \"==========================================\";
  while i < int(sys.argv[1]):
   print my_fibs[i];
   i+=1;
  print \"==========================================\";
 else:
  print \"Please enter a value greater than 1.  Thank you...\";
else:
 print \"I do not know what number to go up to...\";

