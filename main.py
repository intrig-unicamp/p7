 ################################################################################
 # Copyright 2022 INTRIG
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #     http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
 ################################################################################

from src.data import *

topo = generator('main')

# Stratum ip:port
# topo.addstratum("10.1.1.223:9559")

# Recirculation port default 68
topo.addrec_port(196)
topo.addrec_port_user(68)

# addswitch(name)
topo.addswitch("sw1")
topo.addswitch("sw2")
topo.addswitch("sw3")
topo.addswitch("sw4")
topo.addswitch("sw5")
topo.addswitch("sw6")
topo.addp4("p4src/p7calc.p4")

# addhost(name,port,D_P,speed_bps,AU,FEC,vlan)
# include the link configuration
topo.addhost("h1","1/0", 132, 10000000000, "False", "False", 1920, "192.168.0.10")
topo.addhost("h2","1/2", 134, 10000000000, "False", "False", 1920, "192.168.0.20")
# topo.addhost("h3","2/1", 137, 10000000000, "False", "False", 1920, "192.168.0.5")
# topo.addhost("h4","1/2", 130, 10000000000, "False", "False", 1920, "192.168.0.3")


# addlink(node1, node2, bw, pkt_loss, latency, jitter, percentage)
# bw is considered just for the first defined link
topo.addlink("h1","sw1", 10000000000, 0, 0, 0, 100)		#0
topo.addlink("sw1","sw2", 10000000000, 0, 0, 0, 100)	#1
topo.addlink("sw2","sw3", 10000000000, 0, 0, 0, 100)	#2
topo.addlink("sw2","sw4", 10000000000, 0, 0, 0, 100)	#3
topo.addlink("sw3","sw4", 10000000000, 0, 0, 0, 100)	#4
topo.addlink("sw3","sw5", 10000000000, 0, 0, 0, 100)	#5
topo.addlink("sw4","sw5", 10000000000, 0, 0, 0, 100)	#6
topo.addlink("sw5","sw6", 10000000000, 0, 0, 0, 100)	#7
topo.addlink("sw6","h2", 10000000000, 0, 0, 0, 100)		#8

# Forwarding models:
# 0 Default using dijkstra
# 1 PolKA - Polynomial Key-based Architecture for Source Routing
#	if polka, (ID, CRC)
topo.routing(1, 8)
#topo.routeid(["sw2","sw3","sw5"], [2,5,7], "192.168.0.20")
#topo.routeid(["sw5","sw3","sw2"], [5,2,1], "192.168.0.20")

topo.routeid(["sw2","sw3","sw4","sw5"], [2,4,6,7], "192.168.0.20")
topo.routeid(["sw5","sw4","sw3","sw2"], [6,4,2,1], "192.168.0.10")
topo.edgeroute("h1","sw1")
topo.edgeroute("sw1","sw2")
topo.edgeroute("sw5","sw6")
topo.edgeroute("sw6","h2")

# addvlan_port(port,D_P,speed_bps,AU,FEC)
# Vlan and port not P7 process
# topo.addvlan_port("6/-", 168, 100000000000, "False", "False")
# topo.addvlan_port("8/-", 184, 100000000000, "False", "False")

# addvlan_link(D_P1, D_P2, vlan)
# topo.addvlan_link(168,184, 716)

# add table entry sw1
topo.addtable('sw1','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('value','4')
topo.insert()

topo.addtable('sw1','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('value','10')
topo.insert()

# add table entry sw2
topo.addtable('sw2','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('value','5')
topo.insert()

topo.addtable('sw2','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('value','11')
topo.insert()

# add table entry sw3
topo.addtable('sw3','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('value','6')
topo.insert()

topo.addtable('sw3','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('value','12')
topo.insert()

# add table entry sw4
topo.addtable('sw4','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('value','7')
topo.insert()

topo.addtable('sw4','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('value','13')
topo.insert()

# add table entry sw5
topo.addtable('sw5','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('value','8')
topo.insert()

topo.addtable('sw5','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('value','14')
topo.insert()

# add table entry sw6
topo.addtable('sw6','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('value','9')
topo.insert()

topo.addtable('sw6','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('value','15')
topo.insert()

#Generate files
topo.generate_chassis()
topo.generate_ports()
topo.generate_p4rt()
topo.generate_bfrt()
topo.generate_p4code()
topo.generate_graph()
topo.parse_usercode()
topo.generate_setfiles()
topo.generate_multiprogram()
