#!/bin/bash

sudo apt-get update
sudo apt-get install software-properties-common
sudo apt-add-repository -y ppa:ansible/ansible
sudo apt-get update
yes | sudo apt-get -y install ansible
yes | sudo apt-get -y install python-pexpect
yes | sudo apt-get -y install python-pip
sudo pip install --upgrade pip
yes | sudo apt-get install docker.io
sudo pip install docker-py 
cd team12
sudo ansible-playbook create_tenant_image.yml
sudo ansible-playbook -i inventory $(echo $(find -iname connectivity_script.yml))
sudo python /home/bsinha/Downloads/winter2017-finalzip/team12/scripts/connectivity_script.py
