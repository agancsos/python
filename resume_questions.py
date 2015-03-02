#!/bin/python
import sys

##Globals
deck="AH","AS","AD","AC","KH","KS","KD","KC","JH","JS","JD","JC","QH","QS","QD","QC","10H","10S","10D","10C","9H","9S","9D","9C","8H","8S","8D","8C","7H","7S","7D","7C","6H","6S","6D","6C","5H","5S","5D","5C","4H","4S","4D","4C","3H","3S","3D","3C","2H","2S","2D","2C";
#########################
def print_menu():
 menu_options=[];
 menu_options['Exit']=0;
 menu_options['Q1']=1;
 menu_options['Q2']=2;
 menu_options['Q3']=3;

 for func,key in menu_options.iteritems():
  print func,"=",key;

 opt=input("Enter menu option: ");
 if opt == 0 or opt == "Exit":
  sys.exit(1);
 elif opt == 1 or opt == "Q1":
  get_values(input("Enter list of numbers seperated by comma (,): "));
 elif opt == 2 or opt == "Q2":
  non_repeat_string(input("Enter text to scan: "));
 elif opt == 3 or opt == "Q3":
  shuffle_deck(deck);

def count_list_items(item,list):
 final=0;
 for temp_item in list:
  if temp_item==item:
   final=final+1;
 return final;

def get_values(value_str):
 repeated_values=[];
 index=0;
 list_items=value_str;
 for list_item in list_items:
  if count_list_items(list_item,list_items) > 1:
   if count_list_items(list_item,repeated_values)<1:
    repeated_values.append(list_item);
    index=index+1;
 print_values(repeated_values);

def print_values(list):
  i=0;
  for item in list:
   if item != ",":
    sys.stdout.write(str(item));
    sys.stdout.write(str(" "));

def my_random(length):
 import datetime;
 final_str="";
 now=str(datetime.datetime.now());
 final_str=now[len(now)-length:len(now)-length+length];
 return final_str;

def shuffle_deck(deck):
 sys.stdout.write(str("Current: "));
 print_values(deck);
 sys.stdout.write(str("
    New: "));
 ##Shuffle deck
 deck2=[];
 i=0;
 while len(deck2)!=52:
  rand_index=my_random(2);
  test_value=deck[int(rand_index)%52];
  if count_list_items(test_value,deck2)==0:
   deck2.append(test_value);
  i=i+1;
 print_values(deck2);

def non_repeat_string(user_str):
 non_repeats=[];
 index=0;
 for list_item in user_str:
  if count_list_items(list_item,user_str)==1:
   if count_list_items(list_item,non_repeats)<1:
    non_repeats.append(list_item);
    index=index+1;
 print_values(non_repeats);

cmd_prompt=sys.argv;
cmd_prompt.pop(0);
if len(cmd_prompt)>0:
 flag_index=0;
 for flag in cmd_prompt:
  if flag=="1" or flag=="Q1":
   get_values(cmd_prompt[flag_index+1]);
   print "
";
  elif flag=="2" or flag=="Q2":
   non_repeat_string(str(cmd_prompt[flag_index+1]));
   print "
";
  elif flag=="3" or flag=="Q3":
   shuffle_deck(deck);
   print "
";
   print "This works better within the application...";
   print "
";
 flag_index=flag_index+1;
else:
 while 0==0:
  print_menu();
  print "
"; 

