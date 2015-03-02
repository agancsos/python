#!/bin/python
import os
import random
import sys
from os import walk
from os import listdir
from os.path import isfile,isdir, join

db_file_path="./index.db";

def right_pad(mstr,mlen,mchar):
 final="";
 i=len(mstr);
 if(len(mstr)<mlen):
  while(i<mlen):
   final=final+mchar;
   i+=1;
  return mstr+final;
 return substring(0,mlen,mstr)

def menu():
 print right_pad("",80,"=");
 print "Name    : index.py";
 print "Author  : Abel Gancsos";
 print "Version : 1.0.0";
 print "Dev ENV : Mac OS X 10.9";
 print "Test ENV: Mac OS X 10.9";
 print right_pad("",80,"-");
 print "Description:";
 print "This command-line application helps index an application";
 print "repository.  You can also manage the statuses and check for";
 print "new applications that were not added.";
 print right_pad("",80,"-");
 print "Flags:";
 print "-s: Create index database";
 print "  *If database is already created, commands are skipped.";
 print "-r: Refresh index database with new data";
 print "-d: Directory for repo root";
 print "-h: Print headers for session";
 print "-u: Update status for -p Project in -g group to -v Status";
 print "  *Please set -p -g  and -v prior to -u";
 print "-q: Query database";
 print right_pad("",80,"=");

class INDEX:
 id=None;
 dir=None;
 headers=0;
 root="./";
 project=None;
 value=None;
 group=None;

 def __init__(self,dir,headers):
  self.id=right_pad(str(random.randint(0000,999999)),10,"0");
  self.dir=dir;
  self.headers=headers;
 
 def create(self):
  sql="create table if not exists projects(project_name character not null,project_lang character default '',";
  sql=sql+"project_group character default '',project_status not null default 'Active',project_description character default '',";
  sql=sql+"last_updated_date timestamp not null default current_timestamp,primary key(project_name,project_lang,project_group))";
  os.system("sqlite3 \""+db_file_path+"\" \""+sql+"\"");
 def refresh(self):
   groups=[f for f in listdir(self.dir) if isdir(join(self.dir,f)) ]
   i=0;
   while(i<len(groups)):
    print groups[i];
    langs=[f for f in listdir(self.dir+"/"+groups[i]) if isdir(join(self.dir+"/"+groups[i],f)) ]
    j=0;
    while(j<len(langs)):
     print " "+langs[j];
     projs=[f for f in listdir(self.dir+"/"+groups[i]+"/"+"/"+langs[j]) if isdir(join(self.dir+"/"+groups[i]+"/"+langs[j],f)) or isfile(join(self.dir+"/"+groups[i]+"/"+langs[j],f)) ]
     k=0;
     while(k<len(projs)):
      if(projs[k].replace(".app","")!=projs[k]):
       k+=1;
      print "  "+projs[k];
      sql="select* from projects where project_group='"+groups[i]+"' and project_lang='"+langs[j]+"' and project_name='"+projs[k]+"'";
      os.system("sqlite3 \""+db_file_path+"\" \""+sql+"\" > temp.dat");
      file_handler=open("temp.dat","r");
      rows=file_handler.read().split("\n");
      if(len(rows)<2):
       sql="insert into projects (project_name,project_group,project_lang) values ('"+projs[k]+"','"+groups[i]+"','"+langs[j]+"')";
       os.system("sqlite3 \""+db_file_path+"\" \""+sql+"\"");
      k+=1;
     j+=1;
    i+=1;
 def update(self,project,group,value):
  os.sys("sqlite3 \""+db_file_path+"\" \"update "+db_file_path+" set project_status='"+value+" where project_name='"+project+"' and project_group='"+group+"'\"");
 def query(self,sql):
  if self.headers==1:
   self.headers();
  os.system("sqlite3 -header -column \""+db_file_path+"\" \""+sql+"\"");
headers=0;
root="./";

if(len(sys.argv)>1):
 i=0;
 while(i<len(sys.argv)):
  if(sys.argv[i]=="-h"):
   headers=1;
  if(sys.argv[i]=="-d"):
   root=sys.argv[i+1];
  session=INDEX(root,headers);
  if(sys.argv[i]=="-s"):
   session.create();
  if(sys.argv[i]=="-r"):
   session.refresh();
  if(sys.argv[i]=="-q"):
   session.query(sys.argv[i+1]);
  if(sys.argv[i]=="-p"):
   project=sys.argv[i+1];
  if(sys.argv[i]=="-v"):
   value=sys.argv[i+1];
  if(sys.argv[i]=="-g"):
   group=sys.argv[i+1];
  if(sys.argv[i]=="-u"):
   session.update(project,group,value);
  i+=1;
else:
 menu();
