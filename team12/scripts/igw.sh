#!/bin/bash
sudo docker $1 exec apt-get update
sudo docker $1 exec apt-get -y --force-yes install iproute2
sudo docker $1 exec apt-get -y --force-yes install telnet
sudo docker $1 exec apt-get -y --force-yes install openssh-server
sudo docker $1 exec apt-get -y --force-yes install iptables
sudo docker $1 exec apt-get -y --force-yes install iputils-ping
sudo docker $1 exec apt-get -y --force-yes install traceroute
sudo docker $1 exec apt-get -y --force-yes install tcpdump
sudo docker $1 exec apt-get -y --force-yes install iperf
sudo docker $1 exec apt-get -y --force-yes install vim
sudo docker $1 exec apt-get -y --force-yes install python
sudo docker $1 exec apt-get -y --force-yes install python-pip
sudo docker $1 exec apt-get -y --force-yes install docker.io
sudo docker $1 exec pip install --upgrade pip
sudo docker $1 exec apt-get -y --force-yes install python-pexpect
sudo docker $1 exec pip install paramiko
sudo docker $1 exec apt-get -y --force-yes install nano
sudo docker $1 exec sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
sudo docker $1 exec sysctl -w net.ipv4.ip_forward=1
