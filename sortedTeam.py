#!/bin/python

def pad(string,mylen,char):
 i=len(string);
 final="";
 while i<=mylen:
  final+=char;
  i+=1;
 return string+final;

team=[{'name':'Rob','title':'SR Analyst'},{'name':'Usha','title':'SR Analyst'},{'name':'Tom','title':'SR Analyst'},{'name':'t','title':'Lead'}];

team=sorted(team,key=lambda k:k['title']);
for object in team:
 print pad(object['name'],20," ")," ",pad(object['title'],20," ");
