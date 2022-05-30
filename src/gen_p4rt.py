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

def generate_rt(stratum_ip, hosts, vlans, tableEntries):
	links = []
	
	for j in range(len(hosts)):
		for i in range(len(tableEntries)):
			if tableEntries[i][2] == "send":
				if str(hosts[j][7]) == str(tableEntries[i][1]):
					entry = [tableEntries[i][0]]
					links.append(entry)

	f = open("./files/p4rt.py", "w")

	f.write("import p4runtime_sh.shell as sh\n")
	f.write("import argparse\n")
	f.write("\n")
	f.write("sh.setup(\n")
	f.write("        device_id=1,\n")
	f.write("        grpc_addr=\'" + stratum_ip + "\',  #Update with the Stratum IP\n")
	f.write("        election_id=(0, 1), # (high, low)\n")
	f.write("        config=sh.FwdPipeConfig(\'/workspace/output_dir/p4info.txt\', \'/workspace/output_dir/pipeline_config.pb.bin\')\n")
	f.write("        )\n")
	f.write("\n")

	for i in range(len(hosts)):
		f.write("te = sh.TableEntry(\'SwitchIngress.vlan_fwd\')(action=\'SwitchIngress.match\')\n")
		f.write("te.match[\'vid\'] = \'" + str(hosts[i][6]) + "\'\n")
		f.write("te.match[\'ingress_port\'] = \'" + str(hosts[i][2]) + "\'\n")
		f.write("te.action[\'link\']  = \'" + str(links[i][0]) + "\'\n")
		f.write("te.insert()\n")
		f.write("\n")

	for i in range(len(hosts)):
		f.write("te = sh.TableEntry(\'SwitchIngress.arp_fwd\')(action=\'SwitchIngress.match_arp\')\n")
		f.write("te.match[\'vid\'] = \'" + str(hosts[i][6]) + "\'\n")
		f.write("te.match[\'ingress_port\'] = \'" + str(hosts[i][2]) + "\'\n")
		f.write("te.action[\'link\']  = \'" + str(links[i][0]) + "\'\n")
		f.write("te.insert()\n")
		f.write("\n")

	for i in range(len(tableEntries)):
		if tableEntries[i][2] == "send_next":
			f.write("te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')\n")
			f.write("te.match['sw'] = \'" + str(tableEntries[i][0]) + "\'\n")
			f.write("te.match['dest_ip'] = \'" + str(tableEntries[i][1]) + "\'\n")
			f.write("te.action['sw_id']  = \'" + str(tableEntries[i][3]) + "\'\n")
			f.write("te.insert()\n")
			f.write("\n")
		elif tableEntries[i][2] == "send":
			f.write("te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send')\n")
			f.write("te.match['sw'] = \'" + str(tableEntries[i][0]) + "\'\n")
			f.write("te.match['dest_ip'] = \'" + str(tableEntries[i][1]) + "\'\n")
			f.write("te.action['port']  = \'" + str(tableEntries[i][3]) + "\'\n")
			f.write("te.insert()\n")
			f.write("\n")

	for i in range(len(vlans)):
		f.write("te = sh.TableEntry(\'SwitchIngress.vlan_fwd\')(action=\'SwitchIngress.send_direct\')\n")
		f.write("te.match[\'vid\'] = \'" + str(vlans[i][2]) + "\'\n")
		f.write("te.match[\'ingress_port\'] = \'" + str(vlans[i][0]) + "\'\n")
		f.write("te.action[\'port\']  = \'" + str(vlans[i][1]) + "\'\n")
		f.write("te.insert()\n")
		f.write("\n")

		f.write("te = sh.TableEntry(\'SwitchIngress.vlan_fwd\')(action=\'SwitchIngress.send_direct\')\n")
		f.write("te.match[\'vid\'] = \'" + str(vlans[i][2]) + "\'\n")
		f.write("te.match[\'ingress_port\'] = \'" + str(vlans[i][1]) + "\'\n")
		f.write("te.action[\'port\']  = \'" + str(vlans[i][0]) + "\'\n")
		f.write("te.insert()\n")
		f.write("\n")
	f.write("sh.teardown()\n")

	f.close()
