def search_array(char,array):
 i=0;
 final=0;
 while i<len(array):
  if array[i]==char:
   final+=1;
  i+=1;
 return final;
