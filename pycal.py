#!/bin/python
import sys;
import random;
import os;

def menu():
 print "Welcome to PyCal";
 print "===========================================================";
 print "Author     : Abel Gancsos";
 print "Version    : 1.0.1";
 print "Description: This application will generate an ASCII";
 print "             calendar for the user-given calendar, month,";
 print "             and year. It can also list the days of the";
 print "             month in a text table form.";
 print "Purpose    : The purpose of this application was to write";
 print "             an applicaiton using date algorithms using";
 print "             two custom Python classes.";
 print "===========================================================";
 print "\n===========================================================";
 print "Usage:"
 print "python pycal.py [-h|-help|-n|-y|-m";
 print "Flags:";
 print "-h|-help: help";
 print "-n: name of the calendar";
 print "-m: full month name";
 print "-y: YYYY";
 print "-d: display (text|ASCII|both->default)";
 print "--no-headers: don't print the headers";
 print "===========================================================";
 print "\n===========================================================";
 print "Notes:"
 print "+YOU MUST PROVIDE AT LEAST ONE FLAG!!!!!!!!!!!!!!!!!!!!!!!!";
 print "+At this time the ASCII representation only prints the first";
 print " day and days that match the 7 day sequence.";
 print "===========================================================";

class day:
 days_str="Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday";
 days=days_str.split(",");
 
 def get_doy(self,month):
  final=0;
  if month=="January":
   final+=self.num_value;
  if month=="February":
   final=final+31+self.num_value;
  if month=="March":
   final=final+31+28+self.num_value;
  if month=="April":
   final=final+31+28+31+self.num_value;
  if month=="May":
   final=final+31+28+31+30+self.num_value;
  if month=="June":
   final=final+31+28+31+30+31+self.num_value;
  if month=="July":
   final=final+31+28+31+30+31+30+self.num_value;
  if month=="August":
   final=final+31+28+31+30+31+30+31+self.num_value;
  if month=="September":
   final=final+31+28+31+30+31+30+31+31+self.num_value;
  if month=="October":
   final=final+31+28+31+30+31+30+31+31+30+self.num_value;
  if month=="November":
   final=final+30+28+31+30+31+30+31+31+30+31+self.num_value;
  if month=="December":
   final=final+30+28+31+30+31+30+31+31+30+31+30+self.num_value;
  return final;

 def left_pad(self,mstring,mlen,mchar):
  final="";
  i=len(mstring);
  while i<mlen:
   final+=mchar;
   i+=1;
  return final+mstring;

 def right_pad(self,mstring,mlen,mchar):
  final="";
  i=len(mstring);
  while i<mlen:
   final+=mchar;
   i+=1;
  return mstring+final;

 def get_dow(self,num_value,month,year):
  monthTable=0;
  leap=0;
  if(year%4==0):
   leap=1;
  if(month==1):
   if(leap==1):
    monthTable=-1;
   else:
    monthTable=2;
  if(month==2):
   if(leap==1):
    monthTable=2;
   else:
    monthTable=3;
  if(month==3):
   monthTable=3;
  if(month==4):
   monthTable=6;
  if(month==5):
   monthTable=1;
  if(month==6):
   monthTable=4;
  if(month==7):
   monthTable=6;
  if(month==8):
   monthTable=2;
  if(month==9):
   monthTable=5;
  if(month==10):
   monthTable=0;
  if(month==11):
   monthTable=3;
  if(month==12):
   monthTable=5;

  div_str="";
  div_str+=str(year)[2];
  div_str+=str(year)[3];
  yr=int(float(div_str));
  final=num_value+monthTable+yr+(yr/4)+self.get_century(year);
  return self.days[final%7];

 def get_century(self,year):
  div_str="";
  div_str+=str(year)[0];
  div_str+=str(year)[1];
  yr=int(float(div_str));
  if yr%4==0:
   return 6;
  else:
   final=0;
   i=4;
   while yr%4!=0:
    i/=2;
    yr+=1;
   return final;
  return 0;

 def __init__(self,num_value):
  self.id=self.left_pad(str(random.randint(1,9999)),8,"0");
  self.num_value=num_value;
  self.str_value=self.days[self.num_value/7-1];
  self.doy=self.get_doy(self.num_value);

class calendar:
 def __init__(self,name,month,year):
  self.id=day(1).left_pad(str(random.randint(1,9999)),8,"0");
  self.name=name;
  self.month=month;
  self.year=year;
  self.num_of_days=self.get_num_days();
  if self.year%4==0:
   self.leap_year=1;
  else:
   self.leap_year=0;

 def get_num_days(self):
  if self.month=="January":
   return 31;
  if self.month=="February":
   return 28;
  if self.month=="March":
   return 31;
  if self.month=="April":
   return 30;
  if self.month=="May":
   return 31;
  if self.month=="June":
   return 30;
  if self.month=="July":
   return 31;
  if self.month=="August":
   return 31;
  if self.month=="September":
   return 30;
  if self.month=="October":
   return 31;
  if self.month=="November":
   return 30;
  if self.month=="December":
   return 31;
  else:
   return 0;
 
 def num_month(self,month):
  if self.month=="January":
   return 1;
  if self.month=="February":
   return 2;
  if self.month=="March":
   return 3;
  if self.month=="April":
   return 4;
  if self.month=="May":
   return 5;
  if self.month=="June":
   return 6;
  if self.month=="July":
   return 7;
  if self.month=="August":
   return 8;
  if self.month=="September":
   return 9;
  if self.month=="October":
   return 10;
  if self.month=="November":
   return 11;
  if self.month=="December":
   return 12;
  else:
   return 0;

 def print_header(self):
  print day(1).right_pad("",80,"=");
  print "ID: "+self.id;
  print "Name: "+self.name;
  print "Month: "+self.month;
  print "Year: "+str(self.year);
  print "Leap Year: "+str(self.leap_year);
  print "Number of Days: "+str(self.num_of_days);
  print day(1).right_pad("",80,"=");

 def print_text_calendar(self):
  print day(1).right_pad("",80,"=");
  print "|"+day(1).right_pad("Day",10," ")+"|"+day(1).right_pad("DOW",10," ")+"|"+day(1).right_pad("DOY",10," ")+"|";
  print day(1).right_pad("",80,"=");
  i=1;
  while i<=self.num_of_days:
   current_day=day(i);
   print current_day.right_pad(str(i),12," ")+current_day.right_pad(current_day.get_dow(i,self.num_month(self.month),self.year),12," ")+str(current_day.get_doy(self.month));
   i+=1;
  print day(1).right_pad("",80,"=");

 def print_calendar(self):
  print day(1).right_pad("",80,"=");
  sys.stdout.write("|");
  for full_day in day(1).days:
   sys.stdout.write(day(1).right_pad(full_day,10," ")+"|");
  print;
  print day(1).right_pad("",80,"=");
  i=1;
  day_index=1;
  while i<=self.num_of_days:
   current_day=day(day_index%7);
   j=0;
   days=current_day.days;
   sys.stdout.write("|");
   while j<len(days):
    if current_day.get_dow(day_index/7,self.num_month(self.month),self.year)==days[j-1]:
     sys.stdout.write(current_day.right_pad(str(i),10," ")+"|");
    else:
     sys.stdout.write(current_day.right_pad("",10," ")+"|");
    j+=1;
   print; 
   i+=7;
   day_index+=1;
  print day(1).right_pad("",80,"=");


##int main
name="Default Name";
month="January";
year=2014;
display="both";
headers=1;
if len(sys.argv) > 1:
 if sys.argv[1]=="-h" or sys.argv[1]=="-help":
  menu();
 else:
  i=1;
  while i<len(sys.argv):
   if sys.argv[i]=="-n":
    name=sys.argv[i+1];
   if sys.argv[i]=="-m":
    month=sys.argv[i+1];
   if sys.argv[i]=="-y":
    year=int(sys.argv[i+1]);
   if sys.argv[i]=="-d":
    display=sys.argv[i+1];
   if sys.argv[i]=="--no-headers":
    headers=0;
   i+=1;
  my_cal=calendar(name,month,year);
  if headers==1:
   my_cal.print_header();

  if display=="text":
   my_cal.print_text_calendar();

  if display=="ASCII":
   my_cal.print_calendar();

  if display=="both":
   my_cal.print_text_calendar();
   my_cal.print_calendar();
else:
 menu();
###################################################
