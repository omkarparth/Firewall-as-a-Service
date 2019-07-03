from __future__ import print_function
import sys
import subprocess
import os



containerName = raw_input('Enter name of container: ')
ipAddressToLogAndDrop = raw_input('Enter IP address to log and drop: ')

ruleA = 'sudo docker exec '+str(containerName)+' iptables -N LOG_AND_DROP'
ruleB = 'sudo docker exec '+str(containerName)+' iptables -A LOG_AND_DROP -j LOG --log-prefix \"iptables dropped\"'
ruleC = 'sudo docker exec '+str(containerName)+' iptables -A LOG_AND_DROP -j DROP'

os.system(ruleA)
os.system(ruleB)
os.system(ruleC)

command = 'sudo docker exec '+str(containerName)+' iptables -I INPUT 1 -s '+str(ipAddressToLogAndDrop)+'  -j LOG_AND_DROP'

os.system(command)

exit(0)

