from __future__ import print_function
import sys
import subprocess
#import paramiko
import json
from pprint import pprint
import os


data = json.load(open('iptable_json.json'))

commandsToExecuteOnContainers=[]
commandsToExecuteOnPGW=[]
commandsToExecuteOnPrivateNetowrks=[]



for data in data["containerRules"]:

    command = 'sudo docker exec --privileged '+str(data["containerName"])+' iptables -t '+str(data["table"])+' -I '+str(data["chainToAdd"])+' '+str(data["lineNumberToAdd"])+' '

    if data["protocol"]:
        command+='-p '+str(data["protocol"])+' '

    if data["source"]:
        command+='-s '+str(data["source"])+' '

    if data["destination"]:
        command+='-d '+str(data["destination"])+' '

    if data["sourcePort"]:
        command+='--sport '+str(data["sourcePort"])+' '

    if data["destinationPort"]:
        command+='--dport '+str(data["destinationPort"])+' '

    if data["action"]:
        command+='-j '+str(data["action"])

    commandsToExecuteOnContainers.append(command)




for data in data["publicRules"]:

    command1 = 'sudo docker exec --privileged pgw1 iptables -t '+str(data["table"])+' -I '+str(data["chainToAdd"])+' '+str(data["lineNumberToAdd"])+' '
    command2 = 'sudo docker exec --privileged pgw2 iptables -t '+str(data["table"])+' -I '+str(data["chainToAdd"])+' '+str(data["lineNumberToAdd"])+' '

    if data["protocol"]:
        command1+='-p '+str(data["protocol"])+' '
        command2+='-p '+str(data["protocol"])+' '


    if data["source"]:
        command1+='-s '+str(data["source"])+' '
        command2+='-s '+str(data["source"])+' '

    if data["destination"]:
        command1+='-d '+str(data["destination"])+' '
        command2+='-d '+str(data["destination"])+' '


    if data["sourcePort"]:
        command1+='--sport '+str(data["sourcePort"])+' '
        command2+='--sport '+str(data["sourcePort"])+' '

    if data["destinationPort"]:
        command1+='--dport '+str(data["destinationPort"])+' '
        command2+='--dport '+str(data["destinationPort"])+' '

    if data["action"]:
        command1+='-j '+str(data["action"])
        command2+='-j '+str(data["action"])

    commandsToExecuteOnPGW.append(command1)
    commandsToExecuteOnPGW.append(command2)





for data in data["privateRules"]:

    command = 'sudo docker exec --privileged '+str(data["networkName"])+' iptables -t '+str(data["table"])+' -I '+str(data["chainToAdd"])+' '+str(data["lineNumberToAdd"])+' '

    if data["protocol"]:
        command+='-p '+str(data["protocol"])+' '

    if data["source"]:
        command+='-s '+str(data["source"])+' '

    if data["destination"]:
        command+='-d '+str(data["destination"])+' '

    if data["sourcePort"]:
        command+='--sport '+str(data["sourcePort"])+' '

    if data["destinationPort"]:
        command+='--dport '+str(data["destinationPort"])+' '

    if data["action"]:
        command+='-j '+str(data["action"])

    commandsToExecuteOnContainers.append(command)



for command in commandsToExecuteOnContainers:
    os.system(command)

for command in commandsToExecuteOnPGW:
    os.system(command)

for command in commandsToExecuteOnPrivateNetowrks:
    os.system(command)



# username = raw_input('Enter username: ')
# password = raw_input('Enter Password: ')
# port = raw_input('Enter port (ex, 22): ')



# try:
#     client = paramiko.SSHClient()
#     client.load_system_host_keys()
#     client.set_missing_host_key_policy(paramiko.WarningPolicy())
    
#     client.connect(hostname, port=int(port), username=str(username), password=str(password))

#     stdin, stdout, stderr = client.exec_command(command)

# finally:
#     print('Specified firewall rule has been added')
#     client.close()

exit(0)
