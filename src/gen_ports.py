 ################################################################################
 # Copyright 2024 INTRIG
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

def generate_port(hosts, links, vlans, rec_bw):
	
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

	different_bw = 0
	rec_port_bw = 0
	values_at_position = [sublist[2] for sublist in links]
	if len(set(values_at_position)) != 1:
		different_bw = 1
		try:
			index = rec_bw[0].index("/")
			rec_port_bw = rec_bw[0][0:index]
		except ValueError:
			rec_port_bw = rec_bw[0]
		if rec_bw[1] == 9999:
			print("Multiple Bandwidth values defined, need an additional recirculation port")
			print("Use topo.addrec_port_bw(port, D_P)")
			print("e.g. topo.addrec_port_bw(\"8/-\", 188)")
			exit()

	print(rec_port_bw)

	f = open("./files/ports_config.txt", "w")

	#Acces ucli/pm
	f.write("ucli\n")
	f.write("pm\n")

	a = 0
	links_rec = []
	#Ports configuration
	for i in range(len(hosts)):
		if hosts[i][5] == "False":
			feec = "NONE"
		f.write("port-add " + str(hosts[i][1]) + " " + str(int(hosts[i][3]/1000000000)) + "G" + " " + str(feec) + "\n")
		f.write("port-enb " + str(hosts[i][1]) + "\n")
		if hosts[i][4] == "False":
			f.write("an-set " + str(hosts[i][1]) + " 2" + "\n")
		if different_bw == 1 and a == 0 :
			for l in range(len(links)):
				if links[l][2] < hosts[i][3]:
					if a == 4:
						print("Only 4 different Bandwidth available")
						exit()
					f.write("port-add " + str(rec_port_bw) + "/" + str(a) + " " + "10" + "G NONE\n")
					f.write("port-loopback " + str(rec_port_bw) + "/" + str(a) + " mac-near\n")
					f.write("port-enb " + str(rec_port_bw) + "/" + str(a) + "\n")
					links_rec.append(l)
					a += 1
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

	a = 0
	if (len(hosts) > 0):
		f.write("exit" + "\n")
		f.write("bfrt_python" + "\n")
		for i in range(len(hosts)):
			f.write("tf1.tm.port.sched_cfg.mod(dev_port=" + str(hosts[i][2]) + ", max_rate_enable=True)\n")
			if (len(links) > 1 and different_bw == 0):
				f.write("tf1.tm.port.sched_shaping.mod(dev_port=" + str(hosts[i][2]) + ", unit='BPS', provisioning='MIN_ERROR', max_rate=" + str(int(links[i][2]/1000)) + ", max_burst_size=9000)" + "\n")
			else:
				f.write("tf1.tm.port.sched_shaping.mod(dev_port=" + str(hosts[i][2]) + ", unit='BPS', provisioning='MIN_ERROR', max_rate=" + str(int(links[0][2]/1000)) + ", max_burst_size=9000)" + "\n")
			if different_bw == 1 and a == 0 :
				for l in range(len(links)):
					if links[l][2] < hosts[i][3]:
						f.write("tf1.tm.port.sched_cfg.mod(dev_port=" + str(rec_bw[1] + a) + ", max_rate_enable=True)\n")
						f.write("tf1.tm.port.sched_shaping.mod(dev_port=" + str(rec_bw[1] + a) + ", unit='BPS', provisioning='MIN_ERROR', max_rate=" + str(int(links[l][2]/1000)) + ", max_burst_size=9000)" + "\n")
						a += 1

	f.close()

	return links_rec