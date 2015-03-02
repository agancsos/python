#!/bin/python

deff team={};
 team['Lead']="t";
 team['SR Analyst']="Rob";
 team['SR Analyst']="Usha";
 team['SR Analyst']="Tom";

for title,person in team.iteritems():
  print person,",",title
