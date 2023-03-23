import regex as re

def editP4(): #put the file names as parameter

	#files used
	p4_original = 'p7teste.p4' # file name of original user p4 code
	p4_headers = 'hd.p4'  # file name of original headers file
	p4_parser = 'p7teste.p4'   # file name of original parser file
	p4_copy = 'p7_copy.p4' # name of regenerated p4 file (all blocks in the same file)

	allContent = "" # content generated

	# read the content from parser file
	with open(p4_parser, 'r') as parserFile:
		# read all the file content
		content = parserFile.read()

	allContent = allContent + content

	# read the content from table file
	with open(p4_original, 'r') as tablesFile:
		# read all the file content
		content = tablesFile.read()

	
	##allContent = allContent + content #commented now

	#--------------- C H A N G E  H E A D E R S ---------------
	
	# regex expression for match with header definitions
	patternHeaders = "\.*struct\s+headers\s*\{[\s\w;]+ethernet;"

	#rec header
	rec_header = "header rec_h {\n\tbit<32> ts;\n\tbit<32> jitter;\n\tbit<32> num;\n\tbit<16> sw;\n\tbit<16> sw_id\n\tbit<16> ether_type;\n\tPortId_t out_port;\n\tbit<23> flags;\n\tbit<1> signal;\n\tbit<7> pad;\n}\n\n"

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
		newState = "\n\tstate rec { \n\t\tpacket.extract(hdr.rec);\n\t\ttransition select(hdr.rec.ether_type){\n"+ transitionContent   +"\n\t}\n"
		
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

	ingressProcess1 = "\.*Pipeline[\w\s(]+\)\s*,\s*"
	y = re.search(ingressProcess1, allContent)
	
	ig2 = re.match("\w+", allContent[y.end():]).group()

	ig3 = re.search("\.*control\s+"+ig2+"\s*\(", allContent)

	matchi = re.search(patternApply, allContent[ig3.end():])
	st = matchi.start()
	en = matchi.end()

	allContent = allContent[:ig3.end()+en-1] + "\tig_intr_tm_md.ucast_egress_port = 1;\n\t" + allContent[ig3.end()+en-1:]

	#--------------- W R I T E  F I N A L  C O D E ---------------
	
	#write the new p4code
	with open(p4_copy, 'w') as new_file:
		# write the data
		new_file.write(allContent)

editP4()
