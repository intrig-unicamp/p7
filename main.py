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
topo.addrec_port(68)
topo.addrec_port_user(128)

# addswitch(name)
topo.addswitch("sw1")
#topo.addswitch("sw2")
#topo.addswitch("sw3")
#topo.addswitch("sw4")
topo.addp4("p4src/p7calc.p4")

# addhost(name,port,D_P,speed_bps,AU,FEC,vlan)
# include the link configuration
topo.addhost("h1","2/0", 136, 10000000000, "False", "False", 1920, "192.168.0.1")
topo.addhost("h2","1/2", 130, 10000000000, "False", "False", 1920, "192.168.0.2")
#topo.addhost("h3","1/2", 130, 10000000000, "False", "False", 1920, "192.168.0.3")
#topo.addhost("h4","1/2", 130, 10000000000, "False", "False", 1920, "192.168.0.4")


# addlink(node1, node2, bw, pkt_loss, latency, jitter, percentage)
# bw is considered just for the first defined link
topo.addlink("h1","sw1", 10000000000, 0, 0, 0, 100)
topo.addlink("h2","sw1", 10000000000, 0, 0, 0, 100)
#topo.addlink("h1","sw1", 10000000000, 0, 0, 0, 100)
#topo.addlink("h2","sw2", 10000000000, 0, 0, 0, 100)
#topo.addlink("h3","sw3", 10000000000, 0, 0, 0, 100)
#topo.addlink("h4","sw4", 10000000000, 0, 0, 0, 100)
#topo.addlink("sw1","sw2", 10000000000, 0, 0, 0, 100)
#topo.addlink("sw2","sw3", 10000000000, 0, 0, 0, 100)
#topo.addlink("sw3","sw4", 10000000000, 0, 0, 0, 100)

# addvlan_port(port,D_P,speed_bps,AU,FEC)
# Vlan and port not P7 process
# topo.addvlan_port("6/-", 168, 100000000000, "False", "False")
# topo.addvlan_port("8/-", 184, 100000000000, "False", "False")

# addvlan_link(D_P1, D_P2, vlan)
# topo.addvlan_link(168,184, 716)

# add table entry sw1
topo.addtable('sw1','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.1\')')
topo.addactionvalue('value','10')
topo.insert()

topo.addtable('sw1','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.2\')')
topo.addactionvalue('value','20')
topo.insert()


# add table entry
#topo.addtable('sw2','SwitchIngress.calculate')
#topo.addaction('SwitchIngress.operation_xor')
#topo.addmatch('dst_addr','IPAddress(\'192.168.0.2\')')
#topo.addactionvalue('value','15')
#topo.insert()

# add table entry
#topo.addtable('sw3','SwitchIngress.calculate')
#topo.addaction('SwitchIngress.operation_or')
#topo.addmatch('dst_addr','IPAddress(\'192.168.0.1\')')
#topo.addactionvalue('value','10')
#topo.insert()

topo.generate_chassis()
topo.generate_ports()
topo.generate_p4rt()
topo.generate_bfrt()
topo.generate_p4code()
topo.generate_graph()
topo.parse_usecode()
