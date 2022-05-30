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
 
import p4runtime_sh.shell as sh
import argparse

sh.setup(
        device_id=1,
        grpc_addr='10.1.1.223:9559',  #Update with the Stratum IP
        election_id=(0, 1), # (high, low)
        config=sh.FwdPipeConfig('/workspace/output_dir/p4info.txt', '/workspace/output_dir/pipeline_config.pb.bin')
        )

te = sh.TableEntry('SwitchIngress.vlan_fwd')(action='SwitchIngress.match')
te.match['vid'] = '1920'
te.match['ingress_port'] = '136'
te.action['link']  = '0'
te.insert()

te = sh.TableEntry('SwitchIngress.vlan_fwd')(action='SwitchIngress.match')
te.match['vid'] = '1920'
te.match['ingress_port'] = '130'
te.action['link']  = '1'
te.insert()

te = sh.TableEntry('SwitchIngress.vlan_fwd')(action='SwitchIngress.match')
te.match['vid'] = '1920'
te.match['ingress_port'] = '128'
te.action['link']  = '2'
te.insert()

te = sh.TableEntry('SwitchIngress.vlan_fwd')(action='SwitchIngress.match')
te.match['vid'] = '1920'
te.match['ingress_port'] = '129'
te.action['link']  = '3'
te.insert()

te = sh.TableEntry('SwitchIngress.arp_fwd')(action='SwitchIngress.match_arp')
te.match['vid'] = '1920'
te.match['ingress_port'] = '136'
te.action['link']  = '0'
te.insert()

te = sh.TableEntry('SwitchIngress.arp_fwd')(action='SwitchIngress.match_arp')
te.match['vid'] = '1920'
te.match['ingress_port'] = '130'
te.action['link']  = '1'
te.insert()

te = sh.TableEntry('SwitchIngress.arp_fwd')(action='SwitchIngress.match_arp')
te.match['vid'] = '1920'
te.match['ingress_port'] = '128'
te.action['link']  = '2'
te.insert()

te = sh.TableEntry('SwitchIngress.arp_fwd')(action='SwitchIngress.match_arp')
te.match['vid'] = '1920'
te.match['ingress_port'] = '129'
te.action['link']  = '3'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '4'
te.match['dest_ip'] = '192.168.0.5'
te.action['sw_id']  = '1'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '4'
te.match['dest_ip'] = '192.168.0.1'
te.action['sw_id']  = '0'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send')
te.match['sw'] = '1'
te.match['dest_ip'] = '192.168.0.5'
te.action['port']  = '130'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '1'
te.match['dest_ip'] = '192.168.0.1'
te.action['sw_id']  = '4'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send')
te.match['sw'] = '0'
te.match['dest_ip'] = '192.168.0.1'
te.action['port']  = '136'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '0'
te.match['dest_ip'] = '192.168.0.5'
te.action['sw_id']  = '4'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '5'
te.match['dest_ip'] = '192.168.0.2'
te.action['sw_id']  = '2'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '5'
te.match['dest_ip'] = '192.168.0.1'
te.action['sw_id']  = '4'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '4'
te.match['dest_ip'] = '192.168.0.2'
te.action['sw_id']  = '5'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send')
te.match['sw'] = '2'
te.match['dest_ip'] = '192.168.0.2'
te.action['port']  = '128'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '2'
te.match['dest_ip'] = '192.168.0.1'
te.action['sw_id']  = '5'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '0'
te.match['dest_ip'] = '192.168.0.2'
te.action['sw_id']  = '4'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '5'
te.match['dest_ip'] = '192.168.0.5'
te.action['sw_id']  = '1'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '2'
te.match['dest_ip'] = '192.168.0.5'
te.action['sw_id']  = '5'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '1'
te.match['dest_ip'] = '192.168.0.2'
te.action['sw_id']  = '5'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '7'
te.match['dest_ip'] = '192.168.0.3'
te.action['sw_id']  = '3'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '7'
te.match['dest_ip'] = '192.168.0.1'
te.action['sw_id']  = '0'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send')
te.match['sw'] = '3'
te.match['dest_ip'] = '192.168.0.3'
te.action['port']  = '129'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '3'
te.match['dest_ip'] = '192.168.0.1'
te.action['sw_id']  = '7'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '0'
te.match['dest_ip'] = '192.168.0.3'
te.action['sw_id']  = '7'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '7'
te.match['dest_ip'] = '192.168.0.5'
te.action['sw_id']  = '4'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '4'
te.match['dest_ip'] = '192.168.0.3'
te.action['sw_id']  = '7'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '3'
te.match['dest_ip'] = '192.168.0.5'
te.action['sw_id']  = '7'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '1'
te.match['dest_ip'] = '192.168.0.3'
te.action['sw_id']  = '4'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '6'
te.match['dest_ip'] = '192.168.0.3'
te.action['sw_id']  = '3'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '6'
te.match['dest_ip'] = '192.168.0.2'
te.action['sw_id']  = '2'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '3'
te.match['dest_ip'] = '192.168.0.2'
te.action['sw_id']  = '6'
te.insert()

te = sh.TableEntry('SwitchIngress.basic_fwd')(action='SwitchIngress.send_next')
te.match['sw'] = '2'
te.match['dest_ip'] = '192.168.0.3'
te.action['sw_id']  = '6'
te.insert()

sh.teardown()
