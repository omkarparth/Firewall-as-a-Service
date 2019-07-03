#!/usr/bin/python
import uuid 

with open('./scripts/connectivitymat.txt') as f:
  node_list = f.readline().strip().split()

node_num = len(node_list)

unique_id=uuid.uuid4()

open('./scripts/vars_file.yaml', 'w').close() #Clear Previous data
open('./scripts/node_name.txt', 'w').close()
file=open('./scripts/vars_file.yaml','a')
file.write("container_names:\n")

file1=open('./scripts/node_name.txt','a')

for node_name in node_list:
  file.write("  - "+node_name+str(unique_id)+"\n")
  file1.write(node_name+str(unique_id)+"\t")

file.write("  - TR"+str(unique_id)+"\n")
file.write("  - PGW1"+str(unique_id)+"\n")
file.write("  - PGW2"+str(unique_id)+"\n")




