from __future__ import print_function
import os
import sys
import subprocess

protocol = raw_input('Enter the protocol: ')
destinationPort = raw_input('Enter the Destination Port: ')

containerName = raw_input('Enter name of container: ')
command ='sudo docker exec '+str(containerName)+' conntrack -D -p '+str(protocol)+' --dport '+str(destinationPort)

os.system(command)

exit(0)



