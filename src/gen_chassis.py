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

def generate_cha(hosts, links, vlans):
	
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

	f = open("./files/chassis_config.pb.txt", "w")

	#Chassis header
	f.write("description: \"Default Chassis Config for dgecore Wedge100BF-32x\"\n")
	f.write("chassis {\n")
	f.write("  platform: PLT_GENERIC_BAREFOOT_TOFINO\n")
	f.write("  name: \"Edgecore Wedge100BF-32x\"\n")
	f.write("}\n")

	# Node configuration
	f.write("nodes {\n")
	f.write("  id: 1\n")
	f.write("  slot: 1\n")
	f.write("  index: 1\n")
	f.write("}\n")

	#Ports configuration
	for i in range(len(hosts)):
		f.write("singleton_ports {\n")
		f.write("  id: " + str(hosts[i][2]) + "\n")
		if channel[i] == 0:
			f.write("  name: \"" + str(hosts[i][1]) + "/" + "0" +"\"\n")
			f.write("  slot: 1\n")
			f.write("  port: " + str(hosts[i][1]) + "\n")
			f.write("  channel: " + str(hosts[i][1]) + "\n")
		else:
			f.write("  name: \"" + str(hosts[i][1]) +"\"\n")
			f.write("  slot: " + str(slot[i]+1) + "\n")
			f.write("  port: " + str(port[i]) + "\n")
			f.write("  channel: " + str(slot[i]+1) + "\n")
		f.write("  speed_bps: " + str(hosts[i][3]) + "\n")
		f.write("  config_params {\n")
		f.write("    admin_state: ADMIN_STATE_ENABLED\n")
		if hosts[i][4] == "False":
			f.write("    autoneg: TRI_STATE_FALSE\n")
		else:
			f.write("    autoneg: TRI_STATE_TRUE\n")
		if hosts[i][5] == "True":
			f.write("    fec_mode: FEC_MODE_ON\n")
		f.write("  }\n")
		f.write("  node: 1\n")
		f.write("}\n")

	#Vlan ports configuration
	for i in range(len(vlans)):
		f.write("singleton_ports {\n")
		f.write("  id: " + str(vlans[i][1]) + "\n")
		f.write("  name: \"" + str(vlans[i][0]) + "/" + "0" +"\"\n")
		f.write("  slot: 1\n")
		f.write("  port: " + str(vlans[i][0]) + "\n")
		f.write("  speed_bps: " + str(vlans[i][2]) + "\n")
		f.write("  config_params {\n")
		f.write("    admin_state: ADMIN_STATE_ENABLED\n")
		if vlans[i][3] == "False":
			f.write("    autoneg: TRI_STATE_FALSE\n")
		else:
			f.write("    autoneg: TRI_STATE_TRUE\n")
		if vlans[i][4] == "True":
			f.write("    fec_mode: FEC_MODE_ON\n")
		f.write("  }\n")
		f.write("  node: 1\n")
		f.write("}\n")

	if (len(hosts) > 0):
		f.write("vendor_config {\n")
		f.write("  tofino_config {\n")
		f.write("    node_id_to_port_shaping_config {\n")
		f.write("      key: 1\n")
		f.write("      value {\n")
		f.write("        per_port_shaping_configs {\n")
		f.write("          key: " + str(hosts[0][2]) + "\n")
		f.write("          value {\n")
		f.write("            byte_shaping {\n")
		f.write("              max_rate_bps: " + str(links[0][2]) + "# 10000000000 10Gbps 500000000\n")
		f.write("              max_burst_bytes: 9000 # 2x jumbo frame\n")
		f.write("            }\n")
		f.write("          }\n")
		f.write("        }\n")
		f.write("      }\n")
		f.write("    }\n")
		f.write("  }\n")
		f.write("}\n")


	f.close()