#!/bin/python
import random

class MYCLASS:
 id=\"\";
 title=\"\";
 text=\"\";

 def __init__(self):
  self.id=int(random.random()*999999);
  self.title=\"DEFAULT\";
  self.text=\"DEFAULT\";

 def pad(self,string,length,char):
  i=len(string);
  final=\"\";
  while i <= length:
   final+=char;
   i+=1;
  return string + final;

 def printReg(self):
  print self.pad(str(self.id),20,\" \") , self.pad(self.title,20,\" \") , self.pad(self.text,40,\" \");

def sort(list):
 n=len(list);
 swapped_flag=1;
 while swapped_flag!=0: 
  swapped_flag=0;
  i=1;
  while i < n-1:
   if list[i-1].id > list[i].id:
    temp=list[i-1];
    list[i-1]=list[i];
    list[i]=temp; 
    swapped_flag=1;
   n=n-1; 
 return list;

##int main
temp_class=MYCLASS();
class_array=[];
i=0;
while i < 10:
 class_array.append(MYCLASS());
 i+=1;

print \"Before: \";
print temp_class.pad(\"ID\",20,\" \") , temp_class.pad(\"TITLE\",20,\" \") , temp_class.pad(\"TEXT\",40,\" \");
print temp_class.pad(\"=\",80,\"=\");
for objects in class_array:
 objects.printReg();
print temp_class.pad(\"=\",80,\"=\");

class_array=sorted(class_array,key=lambda key:key.id);

print \"After: \";
print temp_class.pad(\"ID\",20,\" \") , temp_class.pad(\"TITLE\",20,\" \") , temp_class.pad(\"TEXT\",40,\" \");
print temp_class.pad(\"=\",80,\"=\");
for objects in class_array:
 objects.printReg();
print temp_class.pad(\"=\",80,\"=\");

