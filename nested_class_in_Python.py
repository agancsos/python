#!/bin/python
import random
import sys

class PERSON:
 id=(random.random()*9999999999);
 first=\"\";
 last=\"\";
 gender=\"\";
 age=\"\";
 street=\"\";
 city=\"\";
 state=\"\";
 zip=\"\";
 status=\"\";

 def set_field(self,field,value):
  if field == \"first\":
   self.first=value;
  elif field == \"last\":
   self.last=value;
  elif field == \"gender\":
   self.gender=values;
  elif field == \"age\":
   self.age=value;
  elif field == \"street\":
   self.street=value;
  elif field == \"city\":
   self.city=value;
  elif field == \"state\":
   self.state=value;
  elif field == \"zip\":
   self.zip=value;
  elif field == \"status\":
   self.status=value;
  else:
   all_values=value.split(,);
   self.first=all_values[0];
   self.last=all_values[1];
   self.gender=all_values[2];
   self.age=all_values[3];
   self.street=all_values[4];
   self.city=all_values[5];
   self.state=all_values[6];
   self.zip=all_values[7];
   self.status=all_values[8];

 class STUDENT:
  person_id=\"\";

  majors=\"\";
  minors=\"\";
  gpa=\"\";
  status=\"\";
  degree=\"\";
  institute=\"\";
  def set_field(self,field,value):
   if field == \"person_id\":
    self.person_id=value;
   elif field == \"majors\":
    self.majors=value;
   elif field == \"minors\":
    self.minors=values;
   elif field == \"gpa\":
    self.gpa=value;
   elif field == \"status\":
    self.status=value;
   elif field == \"degree\":
    self.degree=value;
   elif field == \"institute\":
    self.institute=value;
   else:
    all_values=value.split(,);
    self.person_id=all_values[0];
    self.majors=all_values[1];
    self.minors=all_values[2];
    self.gpa=all_values[3];
    self.status=all_values[4];
    self.degree=all_values[5];
    self.institute=all_values[6];

 class EMPLOYEE:
  person_id=\"\";
  title=\"\";
  departments=\"\";
  status=\"\";
  supervisor_id=\"\";
  def set_field(self,field,value):
   if field == \"person_id\":
    self.person_id=value;
   elif field == \"title\":
    self.title=value;
   elif field == \"departments\":
    self.departments=values;
   elif field == \"status\":
    self.status=value;
   elif field == \"supervisor_id\":
    self.supervisor_id=value;

   else:
    all_values=value.split(,);
    self.person_id=all_values[0];
    self.title=all_values[1];
    self.departments=all_values[2];
    self.status=all_values[3];
    self.supervisor_id=all_values[4];

def print_test_data(person):
 print \"======================================================\";
 print \"Name    :\",person.first,\" \",person.last;
 print \"SSN     :\",person.id;
 print \"School  :\",person.STUDENT.institute;
 print \"======================================================\";

##int main
test_person=PERSON();
test_person.set_field(\"first\",\"Abel\");
test_person.STUDENT.institute=\"William Paterson University\";
test_person.STUDENT.person_id=test_person.id;
test_person.STUDENT.majors=\"Computer Science\";
test_person.STUDENT.degree=\"BS\";
print_test_data(test_person);

