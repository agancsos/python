def my_random(length):
 import datetime;
 final_str=\"\";
 now=str(datetime.datetime.now());
 final_str=now[len(now)-length:len(now)-length+length];
 return final_str;

for i in xrange(10):
 print my_random(3);
