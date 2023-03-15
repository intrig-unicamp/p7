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

import re

def generate_port(hosts, links, vlans):
	
	#Identify channels in port
	channel = [0 for i in range(len(hosts))]
	slot = [0 for x in range(len(hosts))]
	port = [0 for x in range(len(hosts))]
	for i in range(len(hosts)):
		m = re.search('/(.+?)', str(hosts[i][1]))
		m2 = re.search('(.+?)/', str(hosts[i][1]))
		if m:
			channel[i] = 1
			slot[i] = int(m.group(1))
			port[i] = int(m2.group(1))

	f = open("./files/ports_config.txt", "w")

	#Acces ucli/pm
	f.write("ucli\n")
	f.write("pm\n")

	#Ports configuration
	for i in range(len(hosts)):
		if hosts[i][5] == "False":
			feec = "NONE"
		f.write("port-add " + str(hosts[i][1]) + " " + str(int(hosts[i][3]/1000000000)) + "G" + " " + str(feec) + "\n")
		f.write("port-enb " + str(hosts[i][1]) + "\n")
		if hosts[i][4] == "False":
			f.write("an-set " + str(hosts[i][1]) + " 2" + "\n")


	#Vlan ports configuration
	for i in range(len(vlans)):
		if vlans[i][4] == "False":
			feec = "NONE"
		f.write("port-add " + str(vlans[i][0]) + " " + str(int(vlans[i][2]/1000000000)) + "G" + " " + str(feec) + "\n")
		f.write("port-enb " + str(vlans[i][0]) + "\n")
		if vlans[i][3] == "False":
			f.write("an-set " + str(vlans[i][0]) + " 2" + "\n")

	f.write("port-dis -/-" + "\n")
	f.write("port-enb -/-" + "\n")
	f.write("show" + "\n")

	if (len(hosts) > 0):
		f.write("exit" + "\n")
		f.write("bfrt_python" + "\n")
		for i in range(len(hosts)):
			f.write("tf1.tm.port.sched_shaping.mod(dev_port=" + str(hosts[i][2]) + ", unit='BPS', provisioning='MIN_ERROR', max_rate=" + str(int(links[i][2]/1000)) + ", max_burst_size=9000)" + "\n")

	f.close()
