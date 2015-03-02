#!/bin/python
import sys;
import random;
import os;

class branch:
 value=0;
 l=None;
 r=None;
 
 def __init__(self,value):
  self.value=value;
  self.l=None;
  self.r=None;

class tree:
 
 def add_node(self,root,value):
  if root==None:
   return branch(value);
  else:
   if value%3==0 and value%2!=0:
    root.l=self.add_node(root.l,value);
   else:
    root.r=self.add_node(root.r,value);
   return root;

 def pad(self,mstring,mlen,mchar):
  final="";
  i=len(mstring);
  while i<mlen:
   final=final+mchar;
   i+=1;
  return final+mstring;

 def size(self,root):
  self.total+=1;
  if root.l!=None:
   self.size(root.l)
  if root.r!=None:
   self.size(root.r);
  return self.total;

 def __init__(self,name,max):
  self.id=self.pad(str(random.randint(0,99999)),10,"0");
  self.name=name;
  self.root=None;
  self.root_value=0;
  self.total=0;
  self.visibles=0;
  self.roots=[];
  self.max=max;

 def print_tree(self,root):
  if root==None:
   pass;
  else:
   print root.value;
   self.print_tree(root.l);
   self.print_tree(root.r);

 def visible_branches(self,root):
  ##Go through tree and count
  if root!=None:
   if root.value>=self.root_value:
    self.visibles+=1;
   self.visible_branches(root.l);
   self.visible_branches(root.r);
  return self.visibles-1;

##int main
my_tree=tree("Binary Tree",10);
print my_tree.pad("",80,"=");
print "ID:"+my_tree.id;
print "Name: "+my_tree.name;
root=branch(random.randint(1,20));
my_tree.root_value=root.value;
i=0;
while i<my_tree.max:
 my_tree.add_node(root,random.randint(1,20));
 i+=1;
my_tree.print_tree(root);
print my_tree.pad("",80,"=");
print "Visible Branches: "+str(my_tree.visible_branches(root));
##################################
