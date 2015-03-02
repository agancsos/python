#!/bin/python
import sys

def help():
 print \"HELP MENU:\";
 print \"python converter.py [b||d] [d|b] value\";
 exit();

def dec_to_bin(dec):
 final=\"\";
 temp_final=\"\";
 while int(dec/2)>=0:
  if(int(dec%2)>0):
   temp_final=temp_final+\"1\"
  else:
   temp_final=temp_final+\"0\"
  dec=int(dec/2)
  if(dec/2==0):
   temp_final=temp_final + str(dec%2);
   i=len(temp_final)-1;
   while i>=0:
    final=final+temp_final[i];
    i=i-1;
   return final

def bin_to_dec(bin):
 final=\"\";
 temp_final=\"\";
 i=0;
 while 1<100000:
  if(str(dec_to_bin(int(i)))==bin):
   return i;
  i=i+1;
 return -1;

if len(sys.argv) ==2 and sys.argv[1]==\"help\":
 help(); 
if len(sys.argv) > 3:
 parm1=sys.argv[1];
 parm2=sys.argv[2];
 parm3=sys.argv[3];
 if parm1==\"d\" and parm2==\"b\":
  print dec_to_bin(int(parm3));
 if parm2==\"b\" and parm2==\"d\":
  print bin_to_dec(parm3);
if len(sys.argv) > 2 and len(sys.argv)<4:
 parm1=sys.argv[1];
 parm2=sys.argv[2];
 if parm1==\"b\":
  print bin_to_dec(str(parm2));
 if parm1==\"d\":
  print dec_to_bin(int(parm2));
if len(sys.argv) >1 and len(sys.argv)<3:
 print \"This functionality has been depricated...\";
if len(sys.argv) ==1 :
 print \"Please provide a value to convert...\";

