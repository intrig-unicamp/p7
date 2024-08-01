from netaddr import IPAddress
p4p7 = bfrt.p7_default.pipe_p7
p4user = bfrt.p7calc_mod.pipe
p4mirror = bfrt.mirror

def clear_all(verbose=True, batching=True):
    global p4p7
    global p4user
    global bfrt

    for table_types in (['MATCH_DIRECT', 'MATCH_INDIRECT_SELECTOR'],
                        ['SELECTOR'],
                        ['ACTION_PROFILE']):
        for table in p4p7.info(return_info=True, print_info=False):
            if table['type'] in table_types:
                if verbose:
                    print("Clearing table {:<40} ... ".
                          format(table['full_name']), end='', flush=True)
                table['node'].clear(batch=batching)
                if verbose:
                    print('Done')
        for table in p4user.info(return_info=True, print_info=False):
            if table['type'] in table_types:
                if verbose:
                    print("Clearing table {:<40} ... ".
                          format(table['full_name']), end='', flush=True)
                table['node'].clear(batch=batching)
                if verbose:
                    print('Done')

clear_all(verbose=True)

vlan_fwd = p4p7.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=136,   link=0)

vlan_fwd = p4p7.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=128,   link=1)

vlan_fwd = p4p7.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=137,   link=2)

vlan_fwd = p4p7.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=130,   link=3)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=136,   link=0)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=128,   link=1)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=137,   link=2)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=130,   link=3)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=4, dest_ip=IPAddress('192.168.0.7'),   link_id=1, sw_id=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=4, dest_ip=IPAddress('192.168.0.1'),   link_id=0, sw_id=0)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send(sw=1, dest_ip=IPAddress('192.168.0.7'),   port=128)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=1, dest_ip=IPAddress('192.168.0.1'),   link_id=4, sw_id=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send(sw=0, dest_ip=IPAddress('192.168.0.1'),   port=136)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=0, dest_ip=IPAddress('192.168.0.7'),   link_id=4, sw_id=0)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=5, dest_ip=IPAddress('192.168.0.5'),   link_id=2, sw_id=2)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=5, dest_ip=IPAddress('192.168.0.1'),   link_id=4, sw_id=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=4, dest_ip=IPAddress('192.168.0.5'),   link_id=5, sw_id=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send(sw=2, dest_ip=IPAddress('192.168.0.5'),   port=137)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=2, dest_ip=IPAddress('192.168.0.1'),   link_id=5, sw_id=2)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=0, dest_ip=IPAddress('192.168.0.5'),   link_id=4, sw_id=0)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=5, dest_ip=IPAddress('192.168.0.7'),   link_id=1, sw_id=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=2, dest_ip=IPAddress('192.168.0.7'),   link_id=5, sw_id=2)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=1, dest_ip=IPAddress('192.168.0.5'),   link_id=5, sw_id=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=6, dest_ip=IPAddress('192.168.0.3'),   link_id=3, sw_id=3)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=6, dest_ip=IPAddress('192.168.0.1'),   link_id=5, sw_id=2)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=5, dest_ip=IPAddress('192.168.0.3'),   link_id=6, sw_id=2)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=4, dest_ip=IPAddress('192.168.0.3'),   link_id=5, sw_id=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send(sw=3, dest_ip=IPAddress('192.168.0.3'),   port=130)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=3, dest_ip=IPAddress('192.168.0.1'),   link_id=6, sw_id=3)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=0, dest_ip=IPAddress('192.168.0.3'),   link_id=4, sw_id=0)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=6, dest_ip=IPAddress('192.168.0.7'),   link_id=5, sw_id=2)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=3, dest_ip=IPAddress('192.168.0.7'),   link_id=6, sw_id=3)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=1, dest_ip=IPAddress('192.168.0.3'),   link_id=5, sw_id=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=6, dest_ip=IPAddress('192.168.0.5'),   link_id=2, sw_id=2)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=3, dest_ip=IPAddress('192.168.0.5'),   link_id=6, sw_id=3)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=2, dest_ip=IPAddress('192.168.0.3'),   link_id=6, sw_id=2)


calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 0, dst_addr = IPAddress('192.168.0.1'), value = 5)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 0, dst_addr = IPAddress('192.168.0.3'), value = 10)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 0, dst_addr = IPAddress('192.168.0.5'), value = 15)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 0, dst_addr = IPAddress('192.168.0.7'), value = 20)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 1, dst_addr = IPAddress('192.168.0.1'), value = 6)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 1, dst_addr = IPAddress('192.168.0.3'), value = 11)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 1, dst_addr = IPAddress('192.168.0.5'), value = 16)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 1, dst_addr = IPAddress('192.168.0.7'), value = 21)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 2, dst_addr = IPAddress('192.168.0.1'), value = 7)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 2, dst_addr = IPAddress('192.168.0.3'), value = 12)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 2, dst_addr = IPAddress('192.168.0.5'), value = 17)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 2, dst_addr = IPAddress('192.168.0.7'), value = 22)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 3, dst_addr = IPAddress('192.168.0.1'), value = 8)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 3, dst_addr = IPAddress('192.168.0.3'), value = 13)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 3, dst_addr = IPAddress('192.168.0.5'), value = 18)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 3, dst_addr = IPAddress('192.168.0.7'), value = 23)


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
print ("Table calculate:")
calculate.dump(table=True)
print ("Mirror:")
p4mirror.dump()
