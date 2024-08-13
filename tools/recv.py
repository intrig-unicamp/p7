#!/usr/bin/python

import os
import sys

if os.getuid() !=0:
    print("ERROR")
    quit()

from scapy.all import *
try:
    iface=sys.argv[1]
except:
    iface="enp6s0f1.1920"

print("Sniffing on ", iface)
print("Press Ctrl-C to stop...")
sniff(iface=iface, prn=lambda p: "Result = " + str(p[IP].ttl))
