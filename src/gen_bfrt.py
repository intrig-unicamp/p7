 ################################################################################
 # Copyright 2023 INTRIG
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

def generate_bf(hosts, vlans, tableEntries, usertables, swith_id):
    links = []
    
    for j in range(len(hosts)):
        for i in range(len(tableEntries)):
            if tableEntries[i][2] == "send":
                if str(hosts[j][7]) == str(tableEntries[i][1]):
                    entry = [tableEntries[i][0]]
                    links.append(entry)

    f = open("./files/bfrt.py", "w")

    f.write("from netaddr import IPAddress\n")
    f.write("p4p7 = bfrt.p7_default.pipe_p7\n")
    f.write("p4user = bfrt.p7_default." + "pipe" + "\n") # UPDATE TO USER PIPELINE
    f.write("\n")
    f.write("def clear_all(verbose=True, batching=True):\n")
    f.write("    global p4p7\n")
    f.write("    global p4user\n")
    f.write("    global bfrt\n")
    f.write("\n")
    f.write("    for table_types in (['MATCH_DIRECT', 'MATCH_INDIRECT_SELECTOR'],\n")
    f.write("                        ['SELECTOR'],\n")
    f.write("                        ['ACTION_PROFILE']):\n")
    f.write("        for table in p4p7.info(return_info=True, print_info=False):\n")
    f.write("            if table['type'] in table_types:\n")
    f.write("                if verbose:\n")
    f.write("                    print(\"Clearing table {:<40} ... \".\n")
    f.write("                          format(table['full_name']), end='', flush=True)\n")
    f.write("                table['node'].clear(batch=batching)\n")
    f.write("                if verbose:\n")
    f.write("                    print('Done')\n")
    f.write("        for table in p4user.info(return_info=True, print_info=False):\n")
    f.write("            if table['type'] in table_types:\n")
    f.write("                if verbose:\n")
    f.write("                    print(\"Clearing table {:<40} ... \".\n")
    f.write("                          format(table['full_name']), end='', flush=True)\n")
    f.write("                table['node'].clear(batch=batching)\n")
    f.write("                if verbose:\n")
    f.write("                    print('Done')\n")
    f.write("\n")
    f.write("clear_all(verbose=True)\n")
    f.write("\n")

    for i in range(len(hosts)):
        f.write("vlan_fwd = p4p7.SwitchIngress.vlan_fwd\n")
        f.write("vlan_fwd.add_with_match(vid=" + str(hosts[i][6]) + ", ingress_port=" + str(hosts[i][2]) + ",   link=" + str(links[i][0]) + ")\n")
        f.write("\n")

    for i in range(len(hosts)):
        f.write("arp_fwd = p4p7.SwitchIngress.arp_fwd\n")
        f.write("arp_fwd.add_with_match_arp(vid=" + str(hosts[i][6]) + ", ingress_port=" + str(hosts[i][2]) + ",   link=" + str(links[i][0]) + ")\n")
        f.write("\n")

    for i in range(len(tableEntries)):
        if tableEntries[i][2] == "send_next":
            f.write("basic_fwd = p4p7.SwitchIngress.basic_fwd\n")
            f.write("basic_fwd.add_with_send_next(sw=" + str(tableEntries[i][0]) + ", dest_ip=IPAddress(\'" + str(tableEntries[i][1]) + "\'),   link_id=" + str(tableEntries[i][3]) + ", sw_id="+ str(tableEntries[i][4]) + ")\n")
            f.write("\n")
        elif tableEntries[i][2] == "send":
            f.write("basic_fwd = p4p7.SwitchIngress.basic_fwd\n")
            f.write("basic_fwd.add_with_send(sw=" + str(tableEntries[i][0]) + ", dest_ip=IPAddress(\'" + str(tableEntries[i][1]) + "\'),   port=" + str(tableEntries[i][3]) + ")\n")
            f.write("\n")

    for i in range(len(vlans)):
        f.write("vlan_fwd.add_with_send_direct(vid=" + str(vlans[i][2]) + ", ingress_port=" + str(vlans[i][0]) + ",   port=" + str(vlans[i][1]) + ")\n")
        f.write("\n")

        f.write("vlan_fwd.add_with_send_direct(vid=" + str(vlans[i][2]) + ", ingress_port=" + str(vlans[i][1]) + ",   port=" + str(vlans[i][0]) + ")\n")
        f.write("\n")

    for i in range(len(usertables)):
        table = usertables[i][0][0][1].split('.')
        switch = swith_id[usertables[i][0][0][0]]
        action = usertables[i][1][0].split('.')
        f.write(table[1] + " = p4user." + table[0] + "." + table[1] + "\n")
        match = "sw_id= " + str(switch) + ", "# Switch ID
        for j in range(len(usertables[i][2])):
            if j == 0:
                match =  match + usertables[i][2][j][0] + " = " + usertables[i][2][j][1]
            else:
                match =  match + ", " + usertables[i][2][j][0] + " = " + usertables[i][2][j][1]
        for j in range(len(usertables[i][3])):
            if j == 0:
                action_value =  usertables[i][3][j][0] + " = " + usertables[i][3][j][1]
            else:
                action_value =  action_value + ", " + usertables[i][3][j][0] + " = " + usertables[i][3][j][1]
        
        f.write(table[1] + ".add_with_" + action[1] + "(" + match  + ", " +  action_value + ")\n")

    f.write("\n")
    f.write("bfrt.complete_operations()\n")
    f.write("\n")
    f.write("print(\"\"\"\n")
    f.write("******************* PROGAMMING RESULTS *****************\n")
    f.write("\"\"\")\n")
    f.write("print (\"Table vlan_fwd:\")\n")
    f.write("vlan_fwd.dump(table=True)\n")
    f.write("print (\"Table arp_fwd:\")\n")
    f.write("arp_fwd.dump(table=True)\n")
    f.write("print (\"Table basic_fwd:\")\n")
    f.write("basic_fwd.dump(table=True)\n")