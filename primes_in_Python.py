#!/bin/python
import sys

def search_in_prime(x,primes):
 i=0;
 final=0;
 count=0;
 while i < len(primes):
  check= int(x) % primes[i];
  if check == 0 and primes[i] != 1:
   count+=1;
  i+=1;
 return count;

def gen_primes(max_primes):
 final_primes=[];
 i=3;
 final_primes.append(1);
 while len(final_primes) <= int(max_primes):
  if i % 2 != 0 and search_in_prime(i,final_primes) == 0:
   final_primes.append(i);
  i+=1;
 return final_primes;

if len(sys.argv) > 1:
 my_test_primes=gen_primes(sys.argv[1]);
 i=0;
 print \"==================================================\";
 while i < int(sys.argv[1]):
  print my_test_primes[i];
  i+=1;
 print \"==================================================\";
else:
 print \"I do not know how high you want me to go...\";
