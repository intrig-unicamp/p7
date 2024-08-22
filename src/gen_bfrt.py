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

def generate_bf(hosts, vlans, tableEntries, usertables, swith_id, user_code, mirror,
                routing_model, route_ids, edge_links, route_seq, link_seq, route_dest, edge_hosts, name_sw,
                slice_list, slice_number, slice_metric):
    links = []
    
    for j in range(len(hosts)):
        for i in range(len(tableEntries)):
            if tableEntries[i][2] == "send":
                if str(hosts[j][7]) == str(tableEntries[i][1]):
                    entry = [tableEntries[i][0]]
                    links.append(entry)

    default_slice = 0
    a = 0 
    default_slice_number = 99564821324324354
    for i in range(len(slice_list)):
        if slice_list[i][1] == 0: 
            default_slice = 1
            default_slice_number = slice_list[i][0]
            a = a + 1
    if (a == 2):
        print("More than one Default Slice")
        exit()
    if (default_slice == 0):
        print("WARNING, no default Slice defined. Some protocols (e.g., ARP) may not reach the destination")

    default_slice_group= []
    for i in range(len(slice_number)):
        if slice_number[i] == default_slice_number:
            default_slice_group.append(i)


    f = open("./files/bfrt.py", "w")

    user_p4 = user_code.split('/')
    p4 = user_p4[-1].split('.')

    f.write("from netaddr import IPAddress\n")
    if (routing_model == 0):
        f.write("p4p7 = bfrt.p7_default.pipe_p7\n")
    if (routing_model == 1):
        f.write("p4p7 = bfrt.p7_polka.pipe_p7\n")
    f.write("p4user = bfrt." + p4[0] + "_mod" +"." + "pipe" + "\n") # UPDATE TO USER PIPELINE
    f.write("p4mirror = bfrt.mirror\n")
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
        if (routing_model == 0):
            f.write("vlan_fwd.add_with_match(vid=" + str(hosts[i][6]) + ", ingress_port=" + str(hosts[i][2]) + ",   link=" + str(links[i][0]) + ")\n")
        if (routing_model == 1):
            if (default_slice == 0):
                f.write("vlan_fwd.add_with_match(vid=" + str(hosts[i][6]) + ", ingress_port=" + str(hosts[i][2]) + ",   link=" + str(edge_hosts[i][0]) + ")\n")
            if (default_slice == 1):
                f.write("vlan_fwd.add_with_match(vid=" + str(hosts[i][6]) + ", ingress_port=" + str(hosts[i][2]) + ",   link=" + str(edge_hosts[i][0]) + ", routeIdPacket=" + str(route_ids[default_slice_group[i]]) + ")\n")
        f.write("\n")

    for i in range(len(hosts)):
        f.write("arp_fwd = p4p7.SwitchIngress.arp_fwd\n")
        if (routing_model == 0):
            f.write("arp_fwd.add_with_match_arp(vid=" + str(hosts[i][6]) + ", ingress_port=" + str(hosts[i][2]) + ",   link=" + str(links[i][0]) + ")\n")
        if (routing_model == 1):
            if (default_slice == 0):
                f.write("arp_fwd.add_with_match_arp(vid=" + str(hosts[i][6]) + ", ingress_port=" + str(hosts[i][2]) + ",   link=" + str(edge_hosts[i][0]) + ", routeIdPacket=" + str(route_ids[i]) + ")\n")
            if (default_slice == 1):
                f.write("arp_fwd.add_with_match_arp(vid=" + str(hosts[i][6]) + ", ingress_port=" + str(hosts[i][2]) + ",   link=" + str(edge_hosts[i][0]) + ", routeIdPacket=" + str(route_ids[default_slice_group[i]]) + ")\n")
        f.write("\n")

    if (routing_model == 0):
        for i in range(len(tableEntries)):
            if tableEntries[i][2] == "send_next":
                f.write("basic_fwd = p4p7.SwitchIngress.basic_fwd\n")
                f.write("basic_fwd.add_with_send_next(sw=" + str(tableEntries[i][0]) + ", dest_ip=IPAddress(\'" + str(tableEntries[i][1]) + "\'),   link_id=" + str(tableEntries[i][3]) + ", sw_id="+ str(tableEntries[i][4]) + ")\n")
                f.write("\n")
            elif tableEntries[i][2] == "send":
                f.write("basic_fwd = p4p7.SwitchIngress.basic_fwd\n")
                f.write("basic_fwd.add_with_send(sw=" + str(tableEntries[i][0]) + ", dest_ip=IPAddress(\'" + str(tableEntries[i][1]) + "\'),   port=" + str(tableEntries[i][3]) + ")\n")
                f.write("\n")
    if (routing_model == 1):
        index_val = 0
        for i in range(len(slice_list)):
            if slice_list[i][0] != default_slice_number:
                if slice_metric == "ToS":
                    f.write("slice_dst = p4p7.SwitchIngress.slice_dst\n")
                    f.write("slice_dst.add_with_slice_select_dst(diffserv=" + str(slice_list[i][1]) + ", dest_ip=IPAddress(\'" + str(route_dest[i+index_val]) + "\'), routeIdPacket=" + str(route_ids[i+index_val]) + ")\n")
                    index_val = index_val + 1
                    f.write("slice_src = p4p7.SwitchIngress.slice_src\n")
                    f.write("slice_src.add_with_slice_select_dst(diffserv=" + str(slice_list[i][1]) + ", dest_ip=IPAddress(\'" + str(route_dest[i+index_val]) + "\'), routeIdPacket=" + str(route_ids[i+index_val]) + ")\n")
                    f.write("\n")
                else:
                    f.write("slice_dst = p4p7.SwitchIngress.slice_dst\n")
                    f.write("slice_dst.add_with_slice_select_dst(dst_port=" + str(slice_list[i][1]) + ", routeIdPacket=" + str(route_ids[i+index_val]) + ")\n")
                    index_val = index_val + 1
                    f.write("slice_src = p4p7.SwitchIngress.slice_src\n")
                    f.write("slice_src.add_with_slice_select_src(src_port=" + str(slice_list[i][1]) + ", routeIdPacket=" + str(route_ids[i+index_val]) + ")\n")
                    f.write("\n")

        for i in range(len(edge_links)):
            if (i == 0):
                f.write("basic_fwd = p4p7.SwitchIngress.basic_fwd\n")
                f.write("basic_fwd.add_with_send_next(sw=" + str(edge_links[i]) + ", dest_ip=IPAddress(\'" + str(route_dest[0]) + "\'),   sw_id=" + str(int(edge_hosts[0][1][2:])-1) + ")\n")
                f.write("\n")
            if (i == 1):
                f.write("basic_fwd = p4p7.SwitchIngress.basic_fwd\n")
                f.write("basic_fwd.add_with_send_next(sw=" + str(edge_links[i]) + ", dest_ip=IPAddress(\'" + str(route_dest[0]) + "\'),   sw_id=" + str(int(edge_hosts[0][1][2:])) + ")\n")
                f.write("\n")
            if (i == 2):
                f.write("basic_fwd = p4p7.SwitchIngress.basic_fwd\n")
                f.write("basic_fwd.add_with_send_next(sw=" + str(edge_links[i]) + ", dest_ip=IPAddress(\'" + str(route_dest[1]) + "\'),   sw_id=" + str(int(edge_hosts[1][1][2:])-2) + ")\n")
                f.write("\n")
            if (i == 3):
                f.write("basic_fwd = p4p7.SwitchIngress.basic_fwd\n")
                f.write("basic_fwd.add_with_send_next(sw=" + str(edge_links[i]) + ", dest_ip=IPAddress(\'" + str(route_dest[1]) + "\'),   sw_id=" + str(int(edge_hosts[1][1][2:])-1) + ")\n")
                f.write("\n")

        unique_lines = set()
        for i in range(len(route_seq)):
            if route_dest[i] == route_dest[0]:
                for j in range(len(route_seq[i])):
                    if j < (len(route_seq[i])-1):
                        line = (
                            "basic_fwd = p4p7.SwitchIngress.basic_fwd\n"
                            f"basic_fwd.add_with_send_next(sw={link_seq[i][j]}, dest_ip=IPAddress('{route_dest[i]}'), "
                            f"  sw_id={int(route_seq[i][j+1][2:])-1})\n"
                        )
                    else:
                        line = (
                            "basic_fwd = p4p7.SwitchIngress.basic_fwd\n"
                            f"basic_fwd.add_with_send_next(sw={link_seq[i][j]}, dest_ip=IPAddress('{route_dest[i]}'), "
                            f"  sw_id={int(route_seq[i][j][2:])})\n"
                        )
                    unique_lines.add(line)
            else:
                for j in range(len(route_seq[i])):
                    if j < (len(route_seq[i])-1):
                        line = (
                            "basic_fwd = p4p7.SwitchIngress.basic_fwd\n"
                            f"basic_fwd.add_with_send_next(sw={link_seq[i][j]}, dest_ip=IPAddress('{route_dest[i]}'), "
                            f"  sw_id={int(route_seq[i][j+1][2:])-1})\n"
                        )
                    else:
                        line = (
                            "basic_fwd = p4p7.SwitchIngress.basic_fwd\n"
                            f"basic_fwd.add_with_send_next(sw={link_seq[i][j]}, dest_ip=IPAddress('{route_dest[i]}'), "
                            f"  sw_id={int(route_seq[i][j][2:])-2})\n"
                        )
                    unique_lines.add(line)

        for line in unique_lines:
            f.write(line)
            f.write("\n")  # Add a newline for separation

        f.write("basic_fwd = p4p7.SwitchIngress.basic_fwd\n")
        f.write("basic_fwd.add_with_send(sw=" + str(edge_links[0]) + ", dest_ip=IPAddress(\'" + str(route_dest[1]) + "\'),   port=" + str(hosts[0][2]) + ")\n")
        f.write("basic_fwd.add_with_send(sw=" + str(edge_links[-1]) + ", dest_ip=IPAddress(\'" + str(route_dest[0]) + "\'),   port=" + str(hosts[-1][2]) + ")\n")
        f.write("\n")

        f.write("basic_fwd_hash = p4p7.SwitchIngress.basic_fwd_hash\n")
        f.write("basic_fwd_hash.add_with_send_next_" + str(name_sw[0][2:]) + "(sw_id=" + str(int(name_sw[0][2:])-1) + ", dest_ip=IPAddress(\'" + str(route_dest[0]) + "\'), link_id=1)\n")
        f.write("basic_fwd_hash.add_with_send_next_" + str(name_sw[0][2:]) + "(sw_id=" + str(int(name_sw[0][2:])-1) + ", dest_ip=IPAddress(\'" + str(route_dest[1]) + "\'), link_id=" + str(edge_hosts[0][0]) + ")\n")
        f.write("basic_fwd_hash.add_with_send_next_" + str(name_sw[-1][2:]) + "(sw_id=" + str(int(name_sw[-1][2:])-1) + ", dest_ip=IPAddress(\'" + str(route_dest[1]) + "\'), link_id=7)\n")
        f.write("basic_fwd_hash.add_with_send_next_" + str(name_sw[-1][2:]) + "(sw_id=" + str(int(name_sw[-1][2:])-1) + ", dest_ip=IPAddress(\'" + str(route_dest[0]) + "\'), link_id=" + str(edge_hosts[-1][0]) + ")\n")
        f.write("\n")
        for i in range(1, len(name_sw) - 1):
            for j in range(2):
                f.write("basic_fwd_hash = p4p7.SwitchIngress.basic_fwd_hash\n")
                f.write("basic_fwd_hash.add_with_send_next_" + str(name_sw[i][2:]) + "(sw_id=" + str(int(name_sw[i][2:])-1) + ", dest_ip=IPAddress(\'" + str(route_dest[j]) + "\'))\n")
                f.write("\n")

    for i in range(len(vlans)):
        f.write("vlan_fwd.add_with_send_direct(vid=" + str(vlans[i][2]) + ", ingress_port=" + str(vlans[i][0]) + ",   port=" + str(vlans[i][1]) + ")\n")
        f.write("\n")

        f.write("vlan_fwd.add_with_send_direct(vid=" + str(vlans[i][2]) + ", ingress_port=" + str(vlans[i][1]) + ",   port=" + str(vlans[i][0]) + ")\n")
        f.write("\n")

        f.write("arp_fwd = p4p7.SwitchIngress.arp_fwd\n")
        f.write("arp_fwd.add_with_match_arp_direct(vid=" + str(vlans[i][2]) + ", ingress_port=" + str(vlans[i][0]) + ",   port=" + str(vlans[i][1]) + ")\n")
        f.write("arp_fwd.add_with_match_arp_direct(vid=" + str(vlans[i][2]) + ", ingress_port=" + str(vlans[i][1]) + ",   port=" + str(vlans[i][0]) + ")\n")
        f.write("\n")
    f.write("\n")

    table_list = []
    for i in range(len(usertables)):
        table = usertables[i][0][0][1].split('.')
        table_list.append(table[1]) 
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
    table_list = [*set(table_list)]

    for i in range(len(mirror)):
        mirror_type = mirror[i][0][0][0]
        sid = mirror[i][0][0][1]
        direction = mirror[i][0][0][2]
        session_enable = mirror[i][0][0][3]
        ucast_egress_port = mirror[i][0][0][4]
        ucast_egress_port_valid = mirror[i][0][0][5]
        max_pkt_len = mirror[i][0][0][6]
        f.write("mirror = " + "p4mirror." + "cfg" + "\n")
        f.write("mirror" + ".entry_with_" + mirror_type  + "(" +  "sid=" + str(sid) + ", " +  "direction=\'" + direction +  "\', " +  "session_enable=" + session_enable + ", " +  "ucast_egress_port=" + str(ucast_egress_port) + ", " +  "ucast_egress_port_valid=" + str(ucast_egress_port_valid) + ", " +  "max_pkt_len=" +  str(max_pkt_len) + ").push()\n")
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

    for i in range(len(table_list)):
        f.write("print (\"Table " + table_list[i] + ":\")\n")
        f.write(table_list[i] + ".dump(table=True)\n")

    f.write("print (\"Mirror:\")\n")
    f.write("p4mirror" + ".dump()\n")
