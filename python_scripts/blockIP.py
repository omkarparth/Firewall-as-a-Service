from __future__ import print_function
import sys
import subprocess
import os


ipAddressToBlock = raw_input('Enter the ip adress to be blocked: ')

containerName = raw_input('Enter name of container: ')

command = 'sudo docker exec '+str(containerName)+' iptables -I INPUT 1 -s '+str(ipAddressToBlock)+' -j DROP'

os.system(command)


exit(0)
