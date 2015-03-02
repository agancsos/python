#!/bin/python
class MEMBER:
 name="";
 title="";
 
 def __init__(self):
  name="DEFAULT";
  title="DEFAULT";

def pad(string,mylen,char):
 i=len(string);
 final="";
 while i<=mylen:
  final+=char;
  i+=1;
 return string+final;

team=[];
rob=MEMBER();
rob.name="Rob";
rob.title="Sr. Analyst";
t=MEMBER();
t.name="T";
t.title="Lead";
usha=MEMBER();
usha.name="Usha";
usha.title="Sr. Analyst";
tom=MEMBER();
tom.name="Tom";
tom.title="Sr. Analyst";
team.insert(0,rob);
team.insert(1,usha);
team.insert(2,tom);
team.insert(3,t);

team=sorted(team,key=lambda k:k.title);
for object in team:
 print pad(object.name,20," ")," ",pad(object.title,20," ");
