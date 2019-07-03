#!/bin/sh

a=172.19.0.3
b=172.19.0.4

while true
do 
	sleep 10
	ping -c 1 $a
	if [ $? -gt 0 ]
	then 
		ip route del default
		ip route add default via $b metric 99
		c=$a
		a=$b
		b=$c
	fi
done


