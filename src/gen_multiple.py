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

def gen_multiple(p4_code, routing_model): 
    f = open("./p4src/multiprogram_custom_bfrt.conf", "w")

    p4_original = p4_code # file name of original user p4 code
    p4_name = p4_original.split(".")
    if p4_name[0].find('/') != -1:
    	p4_copy = p4_name[0].split("/")
    	p4_copy = p4_copy[-1] + "_mod"
    else:
    	p4_copy = p4_name[0] + "_mod"	

    if (routing_model == 0):
        p7_p4code = "p7_default"
    if (routing_model == 1):
        p7_p4code = "p7_polka"

    f.write("{\n")
    f.write("    \"chip_list\": [\n")
    f.write("        {\n")
    f.write("            \"id\": \"asic-0\",\n")
    f.write("            \"chip_family\": \"Tofino\",\n")
    f.write("            \"instance\": 0,\n")
    f.write("            \"pcie_sysfs_prefix\": \"/sys/devices/pci0000:00/0000:00:03.0/0000:05:00.0\",\n")
    f.write("            \"pcie_domain\": 0,\n")
    f.write("            \"pcie_bus\": 5,\n")
    f.write("            \"pcie_fn\": 0,\n")
    f.write("            \"pcie_dev\": 0,\n")
    f.write("            \"pcie_int_mode\": 1,\n")
    f.write("            \"sds_fw_path\": \"share/tofino_sds_fw/avago/firmware\"\n")
    f.write("        }\n")
    f.write("    ],\n")
    f.write("    \"instance\": 0,\n")
    f.write("    \"p4_devices\": [\n")
    f.write("        {\n")
    f.write("            \"device-id\": 0,\n")
    f.write("            \"p4_programs\": [\n")
    f.write("                {\n")
    f.write("                    \"program-name\": \"" + str(p7_p4code) + "\",\n")
    f.write("                    \"bfrt-config\": \"share/tofinopd/" + str(p7_p4code) + "/bf-rt.json\",\n")
    f.write("                    \"p4_pipelines\": [\n")
    f.write("                        {\n")
    f.write("                            \"p4_pipeline_name\": \"pipe_p7\",\n")
    f.write("                            \"context\": \"share/tofinopd/" + str(p7_p4code) + "/pipe_p7/context.json\",\n")
    f.write("                            \"config\": \"share/tofinopd/" + str(p7_p4code) + "/pipe_p7/tofino.bin\",\n")
    f.write("                            \"pipe_scope\": [1]\n")
    f.write("                        }\n")
    f.write("                    ]\n")
    f.write("                },\n")
    f.write("                {\n")
    f.write("                    \"program-name\": \"" + p4_copy + "\",\n")
    f.write("                    \"bfrt-config\": \"share/tofinopd/" + p4_copy + "/bf-rt.json\",\n")
    f.write("                    \"p4_pipelines\": [\n")
    f.write("                        {\n")
    f.write("                            \"p4_pipeline_name\": \"pipe\",\n")
    f.write("                            \"context\": \"share/tofinopd/" + p4_copy + "/pipe/context.json\",\n")
    f.write("                            \"config\": \"share/tofinopd/" + p4_copy + "/pipe/tofino.bin\",\n")
    f.write("                            \"pipe_scope\": [0]\n")
    f.write("                        }\n")
    f.write("                    ]\n")
    f.write("                }\n")
    f.write("            ],\n")
    f.write("            \"agent0\": \"lib/libpltfm_mgr.so\"\n")
    f.write("        }\n")
    f.write("    ]\n")
    f.write("}\n")
