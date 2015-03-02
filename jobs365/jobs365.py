#!/bin/python
import sys
import os
import random
import sqlite3 as lite

db_file_path="jobs365.db";
handler=lite.connect(db_file_path);

def right_pad(mstr,mlen,mpad):
 final="";
 i=len(mstr);
 if i<mlen:
  while i < mlen:
   final=final+mpad;
   i+=1;
 else:
  return substr(0,mlen,mstr); 
 return mstr+final;

def menu():
 print right_pad("",80,"=");
 print "Welcome to Jobs365";
 print "Details:";
 print "Name    : jobs365.py";
 print "Author  : Abel Gancsos";
 print "Dev ENV : Mac OS X Mavericks";
 print "QA ENV  : Mac OS X Yosemite";
 print "Language: Python + SQLite";
 print right_pad("",80,"-");
 print "\nDescription:";
 print "This application is meant to help with searching";
 print "for a new job by collecting data based on user";
 print "input.  User navigates application by using the";
 print "following flags:";
 print right_pad("",80,"-");
 print "-q:  Query database";
 print "-rc: Run crawler (Disclaimer: will run a LONG time...)";
 print "-ap: Add interested position title";
 print "      *Must follow this format: '{TITLE_NAME}'";
 print "-ao: Add interested organization";
 print "      *Must follow this format: '{NAME},{CITY},{STATE},{CEO},{COO},{CIO},{CTO}'";
 print "      *Note: Not all fields are needed, but you do need all commas";
 print "-av: Manually add an open posiition";
 print "      *Must follow this format: '{TITLE},{ORG},{REF},{APPLIED:1/0},{CALLBACK:1/0},{OFFER:1/0},{ACCEPTED:1/0}'";
 print "      *Note: Not all fields are needed, but you do need all commas";
 print "-uv: Manually update open position";
 print "      *Must follow this format: '{TITLE},{ORG},{REF},{APPLIED:1/0},{CALLBACK:1/0},{OFFER:1/0},{ACCEPTED:1/0}'";
 print "      *Must also set the -id flag";
 print "-nh: No headers";
 print "-do: Delete organization (Provide organization name)";
 print "-dp: Delete interested position (Provide positiion name)";
 print right_pad("",80,"-");
 print right_pad("",80,"=");

class JOBS:
 session_id=None;
 interested_jobs=None;
 interested_orgs=None;
 interested_pos=None;
 headers=1;
 id=0;

 def __init__(self,headers):
  self.session_id=right_pad(str(random.randint(0,2000)),10,"0");
  if(headers=="0"):
   self.headers=0;
 def headers(self):
  print "BLAH";
 def query(self,sql):
  if self.headers==1:
   self.headers();
  os.system("sqlite3 -header -column \""+db_file_path+"\" \""+sql+"\"");
 def run(self):
  if self.headers==1:
   self.headers();
 def add_title(self,title):
  os.system("sqlite3 \""+db_file_path+"\" \"insert into interested_titles (title_name) values ('"+title+"')\"");
 def add_org(self,org):
   os.system("sqlite3 \""+db_file_path+"\" \"insert into interested_organizations (organization_name,organization_city,organization_state,organization_ceo,organicastion_coo,organization_cio,organization_cto) values values ('"+replace(",","','",org)+")\"");
 def add_vac(self,org):
  os.system("sqlite3 \""+db_file_path+"\" \"insert into vacs (vac_title,vac_organization,vac_ref,applied,call_back,offer,accepted) values ('"+replace(",","','",org)+")\"");
 def del_pos(self,pos):
  os.system("sqlite3 \""+db_file_path+"\" \"delete from interested_titles where title_name='"+pos+"'\"");
 def del_org(self,org):
  os.system("sqlite3 \""+db_file_path+"\" \"delete from interested_organizations where organization_name='"+org+"'\"");
 def update_vac(self,vac,id):
  print "TEMP";
##int main()
headers="1";
if len(sys.argv) < 2:
 menu();
else:
 i=0;
 while i < len(sys.argv):
  if sys.argv[i] == "-nh":
   headers="0";
  i+=1;
 session=JOBS(headers);
 i=0;
 while i < len(sys.argv):
  if sys.argv[i]=="-id":
   id=sys.argv[i+1];
  if sys.argv[i]=="-q":
   session.query(sys.argv[i+1]);
  if sys.argv[i]=="-rc":
   session.run();
  if sys.argv[i]=="-ap":
   session.add_title(sys.argv[i+1]);
  if sys.argv[i]=="-ao":
   session.add_org(sys.argv[i+1]);
  if sys.argv[i]=="-av":
   session.add_vac(sys.argv[i+1]);
  if sys.argv[i]=="-dp":
   session.del_pos(sys.argv[i+1]);
  if sys.argv[i]=="-do":
   session.del_org(sys.argv[i+1]);
  if sys.argv[i]=="-uv":
   session.update_vac(sys.argv[i+1]);
  i+=1;
#################################################################

