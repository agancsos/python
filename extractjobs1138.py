#!/bin/python
import urllib2
import re
import sys
import random
import os

class extractor:
 id="";
 state="";
 base_url="http://www.altiusdirectory.com/Computers/software-companies-list-in-";

 def __init__(self,state):
  self.id=random.randint(0,99999);
  self.id=self.padid();
  self.state=state.lower().replace(" ","")
  self.base_url=self.base_url+self.state+".html";

 def padid(self):
  final="";
  i=len(str(self.id));
  while i < 10:
   final=final+"0";
   i+=1;
  return final+str(self.id);

 def pad(self,mstring,mlen,char):
  final="";
  i=len(mstring);
  while i < mlen:
   final=final+char;
   i+=1;
  return mstring+final;

 def getState2(self):
  if self.state=="newjersey":  return "NJ";
  if self.state=="newyork":  return "NY";
  else:
   return self.state[0]+self.state[1];

 def queryTable(self,company_name):
  sql="select * from companies where company_name='"+company_name+"'";
  key=str(random.randint(0,99999));
  os.system("sqlite3 \"jobser.db\" \""+sql+"\" > jobserextract_"+key+".txt");
  temp_file=open("jobserextract_"+key+".txt","r");
  file_contents=temp_file.read();
  rows=file_contents.split("\n"); 
  os.system("rm jobserextract_"+key+".txt");
  return rows;
  
 def extract_dir(self):
  print self.pad("",100,"=");
  print "Extracting Software companies for:    ";
  print ".....",self.state,".....",self.id;
  print self.base_url;
  print self.pad("",100,"-");

  ##Setup URL handler
  handler=urllib2.urlopen(self.base_url)
  contents=handler.read()
  
  ##Regular expression
  exp="(<p(.*)<\/p>)+";  ##############Key###########
  exp2="((.+),(.+)<br)+"; ############Key2##########
  exp3="(<td bgcolor=\"#ececec\">(.*)</td>)+";
  matches=re.findall(exp,contents);
  matches2=re.findall(exp2,contents);
  matches3=re.findall(exp3,contents);
  print len(matches);
  if len(matches)==1:
   matches=matches3;
  else:
   matches=re.findall(exp,contents);
  if matches:
   i=0;
   for match in matches:
    company_name=match[0].replace("</p>","").replace("<p>","").replace("</strong>","").replace("<strong style=\"color:#BD0706\">","").replace("'","");
    company_name=company_name.replace("<td bgcolor=\"#ececec\">","").replace("</td>","");
    if i < len(matches2):
     all_addr=matches2[i][0].replace("<br","").replace("<p>","").replace("'","");
     addr_comps=all_addr.split(", ");
     if len(addr_comps) > 2:
      city=addr_comps[1];
      state=addr_comps[2];
     if len(addr_comps) == 2:
      city=addr_comps[0];
      state=addr_comps[1];
     else:
      city="";
      state=self.getState2();
    else:
     city="";
     state=self.getState2();
    city=city.replace("            ","");
    print "Name: " + self.pad(company_name,50," ") +" City: " + self.pad(city,20," ") + " State: " + state;
    if len(self.queryTable(company_name))<2:
     os.system("sqlite3 \"jobser.db\" \"insert into companies (company_name,company_city,company_state) values ('"+company_name+"','"+city+"','"+state+"')"+"\"");
    i+=1;
  else:
   print "Sorry, no matches found...";
  print self.pad("",100,"=");

if len(sys.argv) > 1:
 my_extract=extractor(sys.argv[1]);
 my_extract.extract_dir();
else:
 print "Please provide a State...";
