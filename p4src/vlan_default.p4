/*******************************************************************************
 * Copyright 2022 INTRIG
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/

#include <tna.p4>

#include "common/headers.p4"
#include "common/util.p4"


/*************************************************************************
 ************* C O N S T A N T S    A N D   T Y P E S  *******************
**************************************************************************/
const vlan_id_t p7_vlan = 1920;        // vlan for P7
const bit<16> total_sw = 0;         // total number of switches
const bit<10> pkt_loss = 0x0;       // packet loss  - 0xCC - 20%
const PortId_t out_port = 28;      // output port
const PortId_t rec_port = 68;       // recirculation port
const bit<32> latency = 0;   // latency  - 10000000 - 10ms


/*************************************************************************
 **************  I N G R E S S   P R O C E S S I N G   *******************
 *************************************************************************/

    /***********************  H E A D E R S  ************************/

struct headers {
    ethernet_h   ethernet;
    rec_h        rec;
    vlan_tag_h   vlan_tag;
    ipv4_h       ipv4;
}

struct my_ingress_metadata_t {
    bit<32>  ts_diff;
}

    /******  G L O B A L   I N G R E S S   M E T A D A T A  *********/

parser SwitchIngressParser(
       packet_in packet, 
       out headers hdr, 
       out my_ingress_metadata_t md,
       out ingress_intrinsic_metadata_t ig_intr_md) {

    state start {
        packet.extract(ig_intr_md);
        packet.advance(PORT_METADATA_SIZE);
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.ether_type) {
            ETHERTYPE_IPV4:  parse_ipv4;
            ETHERTYPE_VLAN:  parse_vlan;
            ETHERTYPE_REC:   parse_rec;   // Recirculation header
            default: accept;
        }
    }
    
    state parse_vlan {
        packet.extract(hdr.vlan_tag);
        transition accept;
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition accept;
    }

    state parse_rec {
        packet.extract(hdr.rec);
        transition accept;
    }
}


control SwitchIngressDeparser(
        packet_out pkt,
        inout headers hdr,
        in my_ingress_metadata_t ig_md,
        in ingress_intrinsic_metadata_for_deparser_t ig_intr_dprsr_md) {

    apply {
        pkt.emit(hdr);
    }
}


control SwitchIngress(
        inout headers hdr, 
        inout my_ingress_metadata_t md,
        in ingress_intrinsic_metadata_t ig_intr_md,
        in ingress_intrinsic_metadata_from_parser_t ig_intr_prsr_md,
        inout ingress_intrinsic_metadata_for_deparser_t ig_intr_dprsr_md,
        inout ingress_intrinsic_metadata_for_tm_t ig_intr_tm_md) {

    action drop() {
        ig_intr_dprsr_md.drop_ctl = 0x1;
    }

    // Forward a packet directly without any P7 processing
    action send_direct(PortId_t port) {
        ig_intr_tm_md.ucast_egress_port = port;
    }

    // Table to verify the VLAN_ID to be processed by P7
    // Match the VLAN_ID and the ingress port
    table vlan_fwd {
        key = {
            hdr.vlan_tag.vid   : exact;
            ig_intr_md.ingress_port : exact;
        }
        actions = {
            send_direct;
            @defaultonly drop;
        }
        const default_action = drop();
        size = 1024;
    }

    apply {
        // Can be remove, just for internal use
        // if (ig_intr_md.ingress_port == 136 || ig_intr_md.ingress_port == 137){drop();}
        
        // Validate if the incoming packet has VLAN header
        // Match the VLAN_ID with P7
        if (hdr.vlan_tag.isValid()) {
            vlan_fwd.apply();
        } else {
            drop();
        }
        
        // No need for egress processing, skip it and use empty controls for egress.
        ig_intr_tm_md.bypass_egress = 1w1;
    }
}


Pipeline(SwitchIngressParser(),
         SwitchIngress(),
         SwitchIngressDeparser(),
         EmptyEgressParser(),
         EmptyEgress(),
         EmptyEgressDeparser()) pipe;

Switch(pipe) main;
