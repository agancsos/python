#!/bin/python
import datetime

class employee:
 first=\"\";
 last=\"\";
 department=\"\";
 start_date=\"\";
 end_date=\"\";

 def set_all(self,first,last,depart,start,end):
  self.first=first;
  self.last=last;
  self.department=depart;
  self.start_date=start;
  self.end_date=end;

 def date_diff(self,date1,date2):
  datetime1=datetime.datetime.strptime(date1,%Y-%m-%d);
  datetime2=datetime.datetime.strptime(date2,%Y-%m-%d);
  return datetime2-datetime1;

test_employee=employee();
test_employee.set_all(\"Abel\",\"Gancsos\",\"QA-Unix\",\"2013-07-24\",\"2013-12-31\");
now=str(datetime.datetime.now());
now_date=now[0:10];
print test_employee.date_diff(now_date,test_employee.end_date);
