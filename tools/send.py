#!/usr/bin/python

import os
import sys

if os.getuid() !=0:
    print """
ERROR: This script requires root privileges. 
       Use 'sudo' to run it.
"""
    quit()

from scapy.all import *

try:
    ip_dst = sys.argv[1]
    ttl_val = sys.argv[2]
except:
    ip_dst = "192.168.0.3"
    ttl_val = 20

print "Sending IP packet to", ip_dst
p = (Ether(dst="ac:1f:6b:67:06:70", src="00:1b:21:a0:52:d4")/
     IP(ttl=int(ttl_val),src="192.168.0.1", dst=ip_dst)/
     UDP(sport=7,dport=7)/
     "This is a test")
sendp(p, iface="vlan1920") 
