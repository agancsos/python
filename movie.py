#!/bin/python
import sys
import os
import random
import urllib2


def right_pad(mstr,mlen,mpad):
 final="";
 if len(mstr) > mlen:
  return mstr[0:len];
 else:
  i=len(mstr);
  while i < mlen:
   final=final + mpad;
   i+=1;
  return mstr + final;

def left_pad(mstr,mlen,mpad):
 final="";
 if len(mstr) > mlen:
  return mstr[0:len];
 else:
  i=len(mstr);
  while i < mlen:
   final=final + mpad;
   i+=1;
  return final + mstr;

class MOVIES:
 id=None;
 movies=0;
 list=None;

 def __init__(self):
  self.id=left_pad(str(random.randint(0,9999)),10,"0");
  self.movies=0;
  self.list=self.extract_list();

 def extract_list(self):
  handler=urllib2.urlopen("http://api.computerfoxdesign.com/movie_api.php");
  lines=handler.read().split("\nEND RECORD");
  return lines;

 def create_db(self):
  sql="create table if not exists movies (movie_name character not null,gancsos_flag integer,movie_year";
  sql=sql+" integer not null,row integer,genre character,rating float,primary key(movie_name,movie_year))";
  os.system("sqlite3 \"movies.db\" \""+sql+"\"");

 def run(self):
  self.create_db();
  i=0;
  while i < len(self.list) - 1:
   os.system("sqlite3 \"movies.db\" \"insert into movies values ('"+self.list[i].replace('::',"','")+"')\"");
   i+=1;

session=MOVIES();
print session.id;
session.run();
