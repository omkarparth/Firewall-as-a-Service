#!/usr/bin/python

from math import *
import subprocess
import os
import pexpect
import sys
import json

#old_stdout = sys.stdout
#sys.stdout = open(os.devnull, 'w')

with open('/home/bsinha/Downloads/winter2017-finalzip/team12/scripts/node_name.txt') as f:
  connectivity_mat = f.read()

current_octet=1
base_ip=1

## Reading the node names
connectivity_mat_row = connectivity_mat.strip().split("\n")
nodes = connectivity_mat_row[0].strip().split()
node_num = len(nodes)

with open('/home/bsinha/Downloads/winter2017-finalzip/team12/scripts/connectivitymat.txt') as f:
  connectivity_mat = f.read()

connectivity_mat_row = connectivity_mat.strip().split("\n")

## Getting the PIDs of nodes
pids=['pids']
for i in range(0,node_num):
  output = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}' "+nodes[i], stdout=subprocess.PIPE, shell=True)
  (out, err) = output.communicate()
  pids.append(out.strip())
##
print("pids")
print(pids)

open('/home/bsinha/Downloads/winter2017-finalzip/team12/connectivity_map.txt', 'w').close() #Clear Previous data
file =open('/home/bsinha/Downloads/winter2017-finalzip/team12/connectivity_map.txt','a')
file.write("Connections:\n")

uni_uuid = str(nodes[0])[-36:]

print(uni_uuid)

## Creating and Sending the veth links
for i in range(1,(node_num+1)):
        current_node = connectivity_mat_row[i].strip().split()

        for j in range(i,(node_num+1)):
                if current_node[j] == "1":
                        os.system("sudo ip link add vport1 type veth peer name vport2")
                        port1 = "eth"+str(j)
                        port2 = "eth"+str(i)
                        port1_ip = "192.168."+str(current_octet)+"."+str(base_ip)+"/24"
                        port2_ip = "192.168."+str(current_octet)+"."+str(base_ip+1)+"/24"

                        os.system("sudo ip link set dev vport1 netns "+pids[i]+" name "+port1+" up")
                        os.system("sudo ip link set dev vport2 netns "+pids[j]+" name "+port2+" up")
                        os.system("sudo docker exec "+nodes[i-1]+" ip addr add "+port1_ip+" dev "+port1)
                        os.system("sudo docker exec "+nodes[j-1]+" ip addr add "+port2_ip+" dev eth"+str(i))
                        current_octet=current_octet+1
                        file.write(nodes[i-1] +" "+ port1 + " ("+port1_ip+") --- "+nodes[j-1]+" "+port2+ " ("+port2_ip+")\n")
file.close()


## Tunneling VXLAN

with open('/home/bsinha/Downloads/winter2017-finalzip/team12/scripts/vxlanmat.txt') as f:
  connectivity_mat = f.read()

connectivity_mat_row = connectivity_mat.strip().split("\n")

unique_vxlan=0
unique_id=1
current_octet=1
base_ip=1

for i in range(1,(node_num+1)):
        current_node = connectivity_mat_row[i].strip().split()
        for j in range(i,(node_num+1)):
                if current_node[j] == "1":
                        os.system("sudo docker exec "+nodes[i-1]+" ip link add vxlan"+str(unique_vxlan)+" type vxlan id "+str(unique_id)+" group 224.0."+str(current_octet)+"."+str(base_ip)+" dev eth0 dstport 4789")
                        os.system("sudo docker exec "+nodes[i-1]+" ip link set dev vxlan"+str(unique_vxlan)+" up")
                        os.system("sudo docker exec "+nodes[i-1]+" ip addr add  10.0."+str(current_octet)+"."+str(base_ip)+"/24 dev vxlan"+str(unique_vxlan))
                        os.system("sudo docker exec "+nodes[j-1]+" ip link add vxlan"+str(unique_vxlan)+" type vxlan id "+str(unique_id)+" group 224.0."+str(current_octet)+"."+str(base_ip)+" dev eth0 dstport 4789")
                        os.system("sudo docker exec "+nodes[j-1]+" ip link set dev vxlan"+str(unique_vxlan)+" up")
                        os.system("sudo docker exec "+nodes[j-1]+" ip addr add 10.0."+str(current_octet)+"."+str(base_ip+1)+"/24 dev vxlan"+str(unique_vxlan))
                        unique_vxlan=unique_vxlan+1
                        unique_id=unique_id+1
                        current_octet=current_octet+1

file.close()


## Tunneling GRE

with open('/home/bsinha/Downloads/winter2017-finalzip/team12/scripts/gremat.txt') as f:
  connectivity_mat = f.read()

connectivity_mat_row = connectivity_mat.strip().split("\n")


unique_gre=1
current_octet=1
base_ip=1

for i in range(1,(node_num+1)):
        current_node = connectivity_mat_row[i].strip().split()

        for j in range(i,(node_num+1)):
                if current_node[j] == "1":
                        ip_i = os.popen("sudo docker exec "+nodes[i-1]+" ip -4 addr show eth0 | grep -oP \"(?<=inet ).*(?=/)\"").read()
                        ip_i = ip_i.strip()
                        ip_j = os.popen("sudo docker exec "+nodes[j-1]+" ip -4 addr show eth0 | grep -oP \"(?<=inet ).*(?=/)\"").read()
                        ip_j = ip_j.strip()
                        os.system("sudo docker exec --privileged "+nodes[i-1]+" ip tunnel add gre"+str(unique_gre)+" mode gre local "+str(ip_i)+" remote "+str(ip_j)+" ttl 255")
			print("sudo docker exec --privileged "+nodes[i-1]+" ip tunnel add gre"+str(unique_gre)+" mode gre local "+str(ip_i)+" remote "+str(ip_j)+" ttl 255")
                        os.system("sudo docker exec --privileged "+nodes[i-1]+" ip link set dev gre"+str(unique_gre)+" up")
                        os.system("sudo docker exec --privileged "+nodes[i-1]+" ip addr add 10.1."+str(current_octet)+"."+str(base_ip)+"/24 dev gre"+str(unique_gre))
                        os.system("sudo docker exec --privileged "+nodes[j-1]+" ip tunnel add gre"+str(unique_gre)+" mode gre local "+str(ip_j)+" remote "+str(ip_i)+" ttl 255")
			print("sudo docker exec --privileged "+nodes[j-1]+" ip tunnel add gre"+str(unique_gre)+" mode gre local "+str(ip_j)+" remote "+str(ip_i)+" ttl 255")
                        os.system("sudo docker exec --privileged "+nodes[j-1]+" ip link set dev gre"+str(unique_gre)+" up")
                        os.system("sudo docker exec --privileged "+nodes[j-1]+" ip addr add 10.1."+str(current_octet)+"."+str(base_ip+1)+"/24 dev gre"+str(unique_gre))
                        unique_gre=unique_gre+1
                        current_octet=current_octet+1

file.close()


pid=os.fork()
#if pid==0: # new process
os.system("sudo docker exec TR"+str(uni_uuid)+" dockerd &")
    	#exit()
print("sudo docker exec TR"+str(uni_uuid)+" docker network create --driver=bridge --gateway=172.19.0.1 --subnet=172.19.0.0/16 -o \"com.docker.network.bridge.name\"=\"bridge1\" network1")
os.system("sudo docker exec TR"+str(uni_uuid)+" docker network create --driver=bridge --gateway=172.19.0.1 --subnet=172.19.0.0/16 -o \"com.docker.network.bridge.name\"=\"bridge1\" network1")
subnet=21
network_id=0


with open('/home/bsinha/Downloads/winter2017-finalzip/team12/scripts/subnetmat.txt') as f:
  connectivity_mat = f.read()

connectivity_mat_row = connectivity_mat.strip().split("\n")

node_num=len(connectivity_mat_row)

c=1
counter=5
## Creating subnet
for i in range(1,(node_num)):
	current_node = connectivity_mat_row[i].strip().split()
 	num=len(current_node)      
	count=1
        os.system("sudo docker run -itd --privileged  --name=IGW"+str(network_id)+str(uni_uuid)+" tenant_image")
        os.system("sudo docker start IGW"+str(network_id)+str(uni_uuid))
	os.system("sudo docker exec IGW"+str(network_id)+str(uni_uuid)+" iptables -t nat -A POSTROUTING -j MASQUERADE")	
	nodes.append("IGW"+str(network_id)+str(uni_uuid))	
	pid=os.fork()
	if pid==0: # new process
    		os.system("sudo docker exec IGW"+str(network_id)+str(uni_uuid)+" dockerd &")
    		exit()
	#os.system("sudo docker exec IGW"+str(network_id)+" ")
        os.system("sudo docker exec IGW"+str(network_id)+str(uni_uuid)+" docker network create --driver=bridge --gateway=172."+str(subnet)+".0.1 --subnet=172."+str(subnet)+".0.0/16 -o \"com.docker.network.bridge.name\"=\"bridge"+str(network_id)+"\" network"+str(network_id))
        output = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}' IGW"+str(network_id)+str(uni_uuid), stdout=subprocess.PIPE, shell=True)
  	(out, err) = output.communicate()
 	new_pid=out.strip()

	output = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}' TR"+str(uni_uuid), stdout=subprocess.PIPE, shell=True)
  	(out, err) = output.communicate()
 	tr_pid=out.strip()

	port1 = "tr"               
	port2 = "igw"+str(network_id)
	os.system("sudo ip link add "+str(port1)+" type veth peer name "+str(port2))
        port2_ip = "172.19.0."+str(counter)+"/16"
        os.system("sudo ip link set dev "+str(port1)+" netns "+str(new_pid)+" up")
        os.system("sudo ip link set dev "+str(port2)+" netns "+str(tr_pid)+" up")
        os.system("sudo docker exec IGW"+str(network_id)+str(uni_uuid)+" ip addr add "+str(port2_ip)+" dev "+str(port1))
	os.system("sudo docker exec IGW"+str(network_id)+str(uni_uuid)+" ip link set dev "+str(port1)+" up")
 	os.system("sudo ip netns exec "+str(tr_pid)+" ip link set dev "+str(port2)+" up")
	os.system("sudo docker exec TR"+str(uni_uuid)+" ip link set dev "+str(port2)+" up")
	os.system("sudo docker exec TR"+str(uni_uuid)+" brctl addif bridge1 "+str(port2))

        os.system("sudo docker exec IGW"+str(network_id)+str(uni_uuid)+" ip route del default")
        os.system("sudo docker exec IGW"+str(network_id)+str(uni_uuid)+" ip route add default via 172.19.0.1 metric 99")
        os.system("sudo docker exec IGW"+str(network_id)+str(uni_uuid)+" ip route add default via 172.17.0.1 metric 100")
        os.system("sudo docker exec TR"+str(uni_uuid)+" ip route add 172."+str(subnet)+".0.0/16 via 172.19.0."+str(counter))
	counter=counter+1

        for j in range(0,(num)):
	    print("current node"+str(current_node[j]))
            if current_node[j] == "1":
                count=count+1
		port1 = "veth"+str(c)
		c=c+1
                port2 = "veth"+str(c)
		c=c+1
		os.system("sudo ip link add "+str(port1)+" type veth peer name "+str(port2))               		
                port2_ip = "172."+str(subnet)+".0."+str(count)+"/16"
		os.system("sudo ip link set dev "+str(port1)+" netns "+str(new_pid)+" up")
	        os.system("sudo ip link set dev "+str(port2)+" netns "+str(pids[j+1])+" up")                
		os.system("sudo docker exec "+str(nodes[j])+" ip addr add "+str(port2_ip)+" dev "+str(port2))
	 	os.system("sudo docker exec IGW"+str(network_id)+str(uni_uuid)+" brctl addif bridge"+str(network_id)+" "+str(port1))
		os.system("sudo ip netns exec "+str(pids[j+1])+" ip link set dev "+str(port2)+" up")
		os.system("sudo docker exec "+str(nodes[j])+" ip link set dev "+str(port2)+" up")	
                os.system("sudo docker exec "+str(nodes[j])+" ip route del default")
                os.system("sudo docker exec "+str(nodes[j])+" ip route add default via 172."+str(subnet)+".0.1 metric 99")
                os.system("sudo docker exec "+str(nodes[j])+" ip route add default via 172.17.0.1 metric 100")

        network_id=network_id+1
        subnet=subnet+1
          


nodes.append("TR"+str(uni_uuid))
nodes.append("PGW1"+str(uni_uuid))
nodes.append("PGW2"+str(uni_uuid))


os.system("sudo docker exec TR"+str(uni_uuid)+" ip route del default")
os.system("sudo docker exec TR"+str(uni_uuid)+" ip route add default via 172.19.0.3 metric 99")
os.system("sudo docker exec TR"+str(uni_uuid)+" ip route add default via 172.19.0.4 metric 100")



output = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}' PGW1"+str(uni_uuid), stdout=subprocess.PIPE, shell=True)
(out, err) = output.communicate()
pgw1_pid=out.strip()

port1 = "trpgw1"
port2 = "pgw1"
os.system("sudo ip link add "+str(port1)+" type veth peer name "+str(port2))               
port2_ip = "172.19.0.3/16"
os.system("sudo ip link set dev "+str(port1)+" netns "+str(tr_pid)+" up")
os.system("sudo ip link set dev "+str(port2)+" netns "+str(pgw1_pid)+" up")
os.system("sudo docker exec PGW1"+str(uni_uuid)+" ip addr add "+str(port2_ip)+" dev "+str(port1))
os.system("sudo ip netns exec "+str(pgw1_pid)+" ip link set dev "+str(port2)+" up")
os.system("sudo docker exec PGW1"+str(uni_uuid)+" ip link set dev "+str(port2)+" up")	
os.system("sudo docker exec TR"+str(uni_uuid)+" brctl addif bridge1 "+str(port1))

output = subprocess.Popen("sudo docker inspect -f '{{.State.Pid}}' PGW2"+str(uni_uuid), stdout=subprocess.PIPE, shell=True)
(out, err) = output.communicate()
pgw2_pid=out.strip()

port1 = "trpgw2"
port2 = "pgw2"
os.system("sudo ip link add "+str(port1)+" type veth peer name "+str(port2))               
port2_ip = "172.19.0.4/16"
os.system("sudo ip link set dev "+str(port1)+" netns "+str(tr_pid)+" up")
os.system("sudo ip link set dev "+str(port2)+" netns "+str(pgw2_pid)+" up")
os.system("sudo docker exec PGW2"+str(uni_uuid)+" ip addr add "+str(port2_ip)+" dev "+str(port1))
os.system("sudo ip netns exec "+str(pgw2_pid)+" ip link set dev "+str(port2)+" up")
os.system("sudo docker exec PGW2"+str(uni_uuid)+" ip link set dev "+str(port2)+" up")	
os.system("sudo docker exec TR"+str(uni_uuid)+" brctl addif bridge1 "+str(port1))


os.system("sudo docker exec PGW2"+str(uni_uuid)+" iptables -t nat -A POSTROUTING -j MASQUERADE")
os.system("sudo docker exec PGW1"+str(uni_uuid)+" iptables -t nat -A POSTROUTING -j MASQUERADE")
os.system("sudo docker exec TR"+str(uni_uuid)+" iptables -t nat -A POSTROUTING -j MASQUERADE")


d = json.load(open('/home/bsinha/Downloads/winter2017-finalzip/team12/scripts/iptable_json.json'))

commandsToExecuteOnContainers=[]
commandsToExecuteOnPGW=[]
commandsToExecuteOnPrivateNetowrks=[]



for data in d['containerRules']:

    command = "sudo docker exec --privileged "+str(data["containerName"])+str(uni_uuid)+" iptables -t "+str(data["table"])+" -I "+str(data["chainToAdd"])+" "+str(data["lineNumberToAdd"])+" "

    if data['protocol']:
        command+="-p "+str(data['protocol'])+" "

    if data['source']:
        command+="-s "+str(data['source'])+" "

    if data['destination']:
        command+="-d "+str(data['destination'])+" "

    if data['sourcePort']:
        command+="--sport "+str(data['sourcePort'])+" "

    if data['destinationPort']:
        command+="--dport "+str(data['destinationPort'])+" "

    if data['action']:
        command+="-j "+str(data['action'])

    print(command)
    commandsToExecuteOnContainers.append(command)




for data in d['publicRules']:

    command1 = "sudo docker exec --privileged PGW1"+str(uni_uuid)+" iptables -t "+str(data["table"])+" -I "+str(data["chainToAdd"])+" "+str(data["lineNumberToAdd"])+" "
    print(command1)
    command2 = "sudo docker exec --privileged PGW2"+str(uni_uuid)+" iptables -t "+str(data["table"])+" -I "+str(data["chainToAdd"])+" "+str(data["lineNumberToAdd"])+" "

    if data['protocol']:
        command1+="-p "+str(data["protocol"])+" "
        command2+="-p "+str(data["protocol"])+" "


    if data["source"]:
        command1+="-s "+str(data["source"])+" "
        command2+="-s "+str(data["source"])+" "

    if data["destination"]:
        command1+="-d "+str(data["destination"])+" "
        command2+="-d "+str(data["destination"])+" "


    if data["sourcePort"]:
        command1+=" --sport "+str(data["sourcePort"])+"  " 
        command2+=" --sport "+str(data["sourcePort"])+" "

    if data["destinationPort"]:
        command1+=" --dport "+str(data["destinationPort"])+" "
        command2+=" --dport "+str(data["destinationPort"])+" "

    if data["action"]:
        command1+=" -j "+str(data["action"])
        command2+=" -j "+str(data["action"])

    commandsToExecuteOnPGW.append(command1)
    commandsToExecuteOnPGW.append(command2)





for data in d["privateRules"]:

    command = "sudo docker exec --privileged "+str(data["networkName"])+str(uni_uuid)+" iptables -t "+str(data["table"])+" -I "+str(data["chainToAdd"])+" "+str(data["lineNumberToAdd"])+" "

    if data["protocol"]:
        command+=" -p "+str(data["protocol"])+" "

    if data["source"]:
        command+=" -s "+str(data["source"])+" "

    if data["destination"]:
        command+=" -d "+str(data["destination"])+" "

    if data["sourcePort"]:
        command+=" --sport "+str(data["sourcePort"])+" "

    if data["destinationPort"]:
        command+=" --dport "+str(data["destinationPort"])+"  "

    if data["action"]:
        command+=" -j "+str(data["action"])

    commandsToExecuteOnContainers.append(command)



for command in commandsToExecuteOnContainers:
    os.system(str(command))

for command in commandsToExecuteOnPGW:
    os.system(str(command))

for command in commandsToExecuteOnPrivateNetowrks:
    os.system(str(command))





print("NODES: ---------------" +str(nodes))


## Start Quagga and ssh process and set ssh password on all Containers
for i in nodes:
        os.system("sudo docker exec "+i+" /etc/init.d/ssh start")
	os.system("sudo docker exec "+i+" useradd -U "+str(i[:-36])+" ")
	print("sudo docker exec "+i+" useradd -U "+str(i[:-36])+" ")
        child =pexpect.spawn("sudo docker exec -i -t "+i+" passwd "+str(i[-36:0]))
        child.expect('Enter new UNIX password:')
        child.sendline('root')
        child.expect('Retype new UNIX password:')
        child.sendline('root')
        child.expect('passwd: password updated successfully')
        child.expect('\n')

exit(0)


