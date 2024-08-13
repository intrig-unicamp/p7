#!/usr/bin/python

import os
import sys

if os.getuid() !=0:
    print("""
ERROR: This script requires root privileges. 
       Use 'sudo' to run it.
""")
    quit()

from scapy.all import *

try:
    ip_dst = sys.argv[1]
    inter = sys.argv[2]
    ttl_val = sys.argv[3]
except:
    ip_dst = "192.168.100.12"
    inter = "enp3s0f0.1920"
    ttl_val = 1

print("Sending IP packet to ", ip_dst)
p = (Ether()/
     IP(ttl=int(ttl_val), dst=ip_dst)/
     UDP(sport=7,dport=7)/
     "This is a test")
sendp(p, iface=inter)
