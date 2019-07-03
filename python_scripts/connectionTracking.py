from __future__ import print_function
import sys
import subprocess
import os



containerName = raw_input('Enter name of container: ')

command = 'sudo docker exec '+str(containerName)+'  conntrack -L'

os.system(command)


exit(0)
