from netaddr import IPAddress
p4 = bfrt.p7_default.pipe

def clear_all(verbose=True, batching=True):
    global p4
    global bfrt

    for table_types in (['MATCH_DIRECT', 'MATCH_INDIRECT_SELECTOR'],
                        ['SELECTOR'],
                        ['ACTION_PROFILE']):
        for table in p4.info(return_info=True, print_info=False):
            if table['type'] in table_types:
                if verbose:
                    print("Clearing table {:<40} ... ".
                          format(table['full_name']), end='', flush=True)
                table['node'].clear(batch=batching)
                if verbose:
                    print('Done')

clear_all(verbose=True)

vlan_fwd = p4.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=136,   link=0)

vlan_fwd = p4.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=130,   link=3)

arp_fwd = p4.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=136,   link=0)

arp_fwd = p4.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=130,   link=3)

basic_fwd = p4.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=2, dest_ip=IPAddress('192.168.0.5'),   link_id=3, sw_id=2)

basic_fwd = p4.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=2, dest_ip=IPAddress('192.168.0.1'),   link_id=1, sw_id=1)

basic_fwd = p4.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=1, dest_ip=IPAddress('192.168.0.5'),   link_id=2, sw_id=1)

basic_fwd = p4.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=1, dest_ip=IPAddress('192.168.0.1'),   link_id=0, sw_id=0)

basic_fwd = p4.SwitchIngress.basic_fwd
basic_fwd.add_with_send(sw=3, dest_ip=IPAddress('192.168.0.5'),   port=130)

basic_fwd = p4.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=3, dest_ip=IPAddress('192.168.0.1'),   link_id=2, sw_id=2)

basic_fwd = p4.SwitchIngress.basic_fwd
basic_fwd.add_with_send(sw=0, dest_ip=IPAddress('192.168.0.1'),   port=136)

basic_fwd = p4.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=0, dest_ip=IPAddress('192.168.0.5'),   link_id=1, sw_id=0)

vlan_fwd.add_with_send_direct(vid=716, ingress_port=168,   port=184)

vlan_fwd.add_with_send_direct(vid=716, ingress_port=184,   port=168)

calculate = p4.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 0, dst_addr = IPAddress('192.168.0.3'), value = 20)
calculate = p4.SwitchIngress.calculate
calculate.add_with_operation_xor(sw_id= 1, dst_addr = IPAddress('192.168.0.2'), value = 15)
calculate = p4.SwitchIngress.calculate
calculate.add_with_operation_or(sw_id= 2, dst_addr = IPAddress('192.168.0.1'), value = 10)

bfrt.complete_operations()

print("""
******************* PROGAMMING RESULTS *****************
""")
print ("Table vlan_fwd:")
vlan_fwd.dump(table=True)
print ("Table arp_fwd:")
arp_fwd.dump(table=True)
print ("Table basic_fwd:")
basic_fwd.dump(table=True)
