#!/usr/bin/env python

from netaddr import IPNetwork, IPAddress
import sys

#ip = str(sys.argv[1])


def ip_check():
   with open('ip') as input:
    for line in input:
     ip, date = line.strip().split(',')
     if IPAddress(ip) in IPNetwork("192.168.0.0/24"):
          print "DA!"
     else :
          print "Ne !"

ip_check()
