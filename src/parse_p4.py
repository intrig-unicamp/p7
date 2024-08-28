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

import regex as re


def encontrar_chave(string):
    penultimo = 0
    contador = 0
    for match in re.finditer(r'{|}', string):
        if match.group() == '{':
            contador += 1
        elif match.group() == '}':
            if contador == 0:
                return penultimo
            else:
                penultimo = match.start()
                contador -= 1
    return None





def editP4(p4_code, u_port,
		   links, links_rec, rec_bw):

	#files used
	p4_original = p4_code # file name of original user p4 code
	p4_name = p4_original.split(".")
	if p4_name[0].find('/') != -1:
		p4_copy = p4_name[0].split("/")
		p4_copy = "files/" + p4_copy[-1] + "_mod.p4"
	else:
		p4_copy = "files/" + p4_name[0] + "_mod.p4"

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

	user_port = u_port

	allContent = "" # content generated

	# read the content from parser file
	with open(p4_original, 'r') as parserFile:
		# read all the file content
		content = parserFile.read()

	allContent = allContent + content

	# read the content from table file
	with open(p4_original, 'r') as tablesFile:
		# read all the file content
		content = tablesFile.read()

	#--------------- C H A N G E  H E A D E R S ---------------
	
	#OBS: adicionar suporte ao //

	# regex expression for match with header definitions
	patternHeaders = "\.*struct\s+headers\s*\{[\s\w;]+ethernet;"

	#rec header
	rec_header = "header rec_h {\n\tbit<32> ts;\n\tbit<32> num;\n\tbit<32> jitter;\n\tbit<16> sw;\n\tbit<16> sw_id;\n\tbit<16> ether_type;\n\tbit<32> dest_ip;\n\tbit<1> signal;\n\tbit<31> pad;\n\tbit<160> routeid;\n}\n\n"
	
	#match
	matchi = re.search(patternHeaders, allContent)
	st = matchi.start()
	en = matchi.end()

	#add the recirculation header before
	allContent = allContent[:st] + rec_header + allContent[st:en] + "\n\trec_h\trec;" + allContent[en:]

	#--------------- C H A N G E  P A R S E R ---------------

	# Regex expressions for parser
	patternEthernetFull = r'state\s+parse_ethernet\s*\{(?:[^{}]*{[^{}]*}[^{}]*|[^{}]+)*\}' # state start with multiple {} blocks
	patternEthernet = '\.*state\s+parse_ethernet\s*\{' # state start with multiple {} blocks
	patternTransitionStart = '\.*transition\s+select\([\w.]+\)\s*\{'
	add = "\n\t\t\t16w0x9966:   parse_rec;\n"

	transitionOptions = 0

	ethers = re.finditer(patternEthernet, allContent)
	for eth in ethers:
		ethStart = eth.start()
		ethFinal = eth.end()

		matchess = re.search(patternTransitionStart, allContent[ethFinal:])
		
		a = matchess.end()
		b = re.search("\}", allContent[ethFinal+a:]).start()

		transitionContent = allContent[ethFinal+a+1:ethFinal+a+b+1]

		allContent = allContent[:ethFinal+a+1] + add + allContent[ethFinal+a:]		

		#new state to parser rec header
		newState = "\n\tstate parse_rec { \n\t\tpacket.extract(hdr.rec);\n\t\ttransition select(hdr.rec.ether_type){\n"+ transitionContent   +"\n\t}\n"
		aux = re.search(patternEthernetFull, allContent[a-2:])
		allContent = allContent[:a-2+aux.end()+1] + newState +allContent[a-2+aux.end()+1:]

	#--------------- C H A N G E  T A B L E S ---------------

	#regex expression for match and change all tables
	patternTable = r'table\s+[^{]+\s*\{(?:[^{}]*{[^{}]*}[^{}]*|[^{}]+)*\}' # exp to identify all tables
	keyMatch = "\.*key\s*=\s*{" #exp to identify the key section of a table

	#find the name of headers
	intrMD = "out\s+headers\s+"
	finalParent = "out\s+headers\s+\w+\\s*,"

	aux = re.search(intrMD, allContent)
	aux2 = re.search(finalParent, allContent)
	hdrName = allContent[aux.end():aux2.end()-1]

	#adapt the tables
	allTables = re.finditer(patternTable, allContent)

	for table in allTables:
		#print(table)
		a = table.start()
		b = table.end()
		newMat = re.finditer(keyMatch, allContent[a:b])
		for n in newMat:
			#print(n)
			c = n.end()
			allContent = allContent[0:a+c] + "\n\t\t\t"+hdrName+".rec.sw_id   : exact;" + allContent[a+c:]

	#--------------- C H A N G E  E G R E S S  P O R T  ---------------
	
	#regex expression for match and change apply block
	patternApply = r'apply\s*\{(?:[^{}]*\{(?:[^{}]*\{[^{}]*\}[^{}]*|[^{}]+)*\}[^{}]*|[^{}]+)*\}' # exp to identify apply block
	
	#testing
	#patternApply = r'apply\s*\{\n*\t*((\t.*\n)|(^$\n))*^\}'









	ingressProcess1 = "\.*Pipeline[\w\s(]+\)\s*,\s*"
	y = re.search(ingressProcess1, allContent)
	
	ig2 = re.match("\w+", allContent[y.end():]).group()

	ig3 = re.search("\.*control\s+"+ig2+"\s*\([\s\S]*?\)\s*\{", allContent)

	matchi = re.search(patternApply, allContent[ig3.end():])

	mm = encontrar_chave(allContent[ig3.end()+1:])

	st = matchi.start()
	en = matchi.end()

	new_apply = allContent[ig3.end()+st+8:ig3.end()+en-5]

	fw_p7 = "\tif ("
	links_condition = "\tif (hdr.rec.sw == "
	for i in range(len(links_rec)):
		if i == 0 :
			fw_p7 = fw_p7 + "ig_intr_md.ingress_port == " + str(rec_bw[1] + i)
			links_condition = links_condition + str(links_rec[i]) + "){\n\t\tig_intr_tm_md.ucast_egress_port = " + str(rec_bw[1] + i) + ";\n\t}\n"
		elif i < (len(links_rec)) and i > 0:
			fw_p7 = fw_p7 + " || ig_intr_md.ingress_port == " + str(rec_bw[1] + i)
			links_condition = links_condition + "\telse if (hdr.rec.sw == "+ str(links_rec[i]) + "){\n\t\tig_intr_tm_md.ucast_egress_port = " + str(rec_bw[1] + i) + ";\n\t}\n"
		if i == (len(links_rec) -1):
			fw_p7 = fw_p7 + "){\n\t\tig_intr_tm_md.ucast_egress_port = " + str(user_port) + ";\n\t}\n\telse{\n" + new_apply + "\n" + links_condition + "\telse{\n\t\tig_intr_tm_md.ucast_egress_port = " + str(user_port) + ";\n\t}\n\t}\n"

	if different_bw == 1:
		allContent = allContent[:ig3.end()+st+8] + fw_p7 + allContent[ig3.end()+en-1:]
	else:
		allContent = allContent[:ig3.end()+1 + mm-1] + "\tig_intr_tm_md.ucast_egress_port = " + str(user_port) + ";\n\t" + allContent[ig3.end()+1 + mm-1:]	

	
	#allContent = allContent[:ig3.end()+en-1] + "\tig_intr_tm_md.ucast_egress_port = " + str(user_port) + ";\n\t" + allContent[ig3.end()+en-1:]

	#--------------- W R I T E  F I N A L  C O D E ---------------
	
	#write the new p4code
	with open(p4_copy, 'w') as new_file:
		# write the data
		new_file.write(allContent)
