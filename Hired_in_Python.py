#!/bin/python
import sys

def search_array(char,array):
 i=0;
 final=0;
 while i<len(array):
  if array[i]==char:
   final+=1;
  i+=1;
 return final;

def anagrams(firsts,seconds):
 if len(firsts)==len(seconds):
  i=0;
  while i<len(firsts):
   current1=firsts[i];
   current2=seconds[i];
   count_letters=0;
   if len(current1)==len(current2):
    j=0;
    while j<len(current1):
     check_char=current1[j];
     count_letters+=search_array(check_char,current2);
     j+=1;
   if count_letters==len(current1):
    print \"1\";
   else:
    print \"0\"; 
   i+=1; 
 else:
  print \"Not equal number of matches\";

def braces(expressions):
 i=0;
 while i<len(expressions):
  current_exp=expressions[i];
  check1a=search_array(\"{\",current_exp);
  check1b=search_array(\"}\",current_exp);
  check1=(check1a==check1b);

  check2a=search_array(\"(\",current_exp);
  check2b=search_array(\")\",current_exp);
  check2=(check2a==check2b);

  check3a=search_array(\"{\",current_exp);
  check3b=search_array(\"}\",current_exp);
  check3=(check3a==check3b);
  if check1 and check2 and check3:
   print \"1\";
  else:
   print \"0\";
  i+=1;

if len(sys.argv)==1:
 option=\"anagrams\";
else:
 option=sys.argv[1];

if option==\"anagrams\":
 anagrams([\"cat\",\"hat\",\"bob\",\"dog\"],[\"tac\",\"aht\",\"bodb\",\"god\"]);
else:
 braces([\"()()()\"]);
