#!/bin/python
class student:
  name="";
  age=""
  major="";
  school="";

  def print_school(self):
   print self.school;
  
  def print_format(self):
   print "Full Name: ",(self.name);
   print "School: ",(self.school);
   print "Major: ",(self.major);
   print "Age: ",(self.age);

my_student1=student();
my_student2=student();
my_student1.name="Abel Gancsos";
my_student1.age=25;
my_student1.major="Computer Science";
my_student1.school="William Paterson University";

my_student1.print_format();
