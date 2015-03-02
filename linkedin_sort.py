#!/bin/python

class linkedinSort:
 project_name="";
 project_month="";
 project_year=0;
 
 def month_to_int(self):
  month=self.project_month;
  if month == "January":
   return 1;
  if month == "February":
   return 2;
  if month == "March":
   return 3;
  if month == "April":
   return 4;
  if month == "May":
   return 5;
  if month == "June":
   return 6;
  if month == "July":
   return 7;
  if month == "August":
   return 8;
  if month == "September":
   return 9;
  if month == "October":
   return 10;
  if month == "November":
   return 12;
  if month == "December":
   return 12;
  return 0;

 def set_from_other(self,other):
  self.project_name=other.project_name;
  self.project_month=other.project_month;
  self.project_year=other.project_year;

 def print_dates(self):
  for date in self.project_dates:
   date_components=date.split(' ');
   print self.month_to_int(date_components[0]);

 def pad_string(self,string,length):
  final_string="";
  i=0;
  while i<len(string):
   final_string=final_string+string[i];
   i+=1;
  if(len(final_string)<length):
   i=len(final_string);
   while(i<=length):
    final_string=final_string+'_';
    i+=1;
  return final_string;  
   
 def set_dates(self,name,month,year):
  self.project_name=name;
  self.project_month=month;
  self.project_year=year;

 def linkedSort(self):
  return self;

 def sortDates(self,dates_array):
  for sorting in dates_array:
   for sorting2 in dates_array:
    if(sorting.project_year<sorting2.project_year):
     temp_linkedin=linkedinSort();
     temp_linkedin.set_from_other(sorting);
     sorting.set_from_other(sorting2);
     sorting2.set_from_other(temp_linkedin);
    if(sorting.project_year==sorting2.project_year):
     if(sorting.month_to_int()<sorting2.month_to_int()):
      temp_linkedin=linkedinSort();
      temp_linkedin.set_from_other(sorting);
      sorting.set_from_other(sorting2);
      sorting2.set_from_other(temp_linkedin)

     
##int main
to_be_sorted=[];
project_dates={'Sample1 November 2010','PaperWorks October 2012','ResumeBuuilder October 2013','Resume_Sampler September 2013',
               'iNCREPYT_Alpha August 2013','LangSim November 2013','iNCREPTY_LT_Alpha August 2013','DOY April 2013',
               'JokeBook January 2013','HIRED January 2014','JokeBook2 January 2014','Pic2Text January 2014','BlackBook January 2014',
               'LangSim_LT February 2014','MovieBook February 2014','Geode October 2012','Star_wars_Roll-Ups  ','Students.py October 2013'};
i=0;
for dates in project_dates:
 test_linkedin=linkedinSort();
 temp_comp=dates.split(' ');
 temp_name=temp_comp[0];
 temp_name=linkedinSort().pad_string(temp_name,20);
 temp_month=temp_comp[1];
 temp_year=temp_comp[2];
 test_linkedin.set_dates(temp_name.replace('_',' '),temp_month,temp_year);
 to_be_sorted.insert(i,test_linkedin);
 i+=1;

linkedinSort().sortDates(to_be_sorted);
for project in to_be_sorted:
 print project.project_name,'\t\t',project.pad_string(project.project_month,10).replace('_',' '),'\t\t',project.project_year;

