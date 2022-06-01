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

import networkx as nx
import sys
import re
import matplotlib.pyplot as plt
import PIL

#pre-processing
lines=""

def gen_topo(lines):
	lines = str(lines)
	lines = lines.replace(" ", "").replace("'", "")
	lines = lines[1:-1]

	pattern=r',(?=\[)'
	splitted = re.split(pattern, lines)

	pattern=r','
	lines = lines[1:-1]
	lines = re.split(pattern, lines)

	#store unique nodes
	nodeSet = set()
	for i in range(len(splitted)):
		temp = str(splitted[i])
		temp = temp[1:-1]
		temp = temp.split(',')
		for j in range(len(temp)):
			if temp[j] not in nodeSet:
				nodeSet.add(temp[j])

	#store unique links
	linkSet = set()
	link_id = []
	l = 0
	for i in range(len(splitted)):
		temp = str(splitted[i]).replace("'", "")
		temp = temp[1:-1]
		temp = temp.split(',')

		for j in range(len(temp)-1):
			if (temp[j],temp[j+1]) not in linkSet and (temp[j+1],temp[j]) not in linkSet:
				linkSet.add((temp[j],temp[j+1]))
				link_id.append(l)
				l = l+1

	#graph definition
	g = nx.Graph()

	#color map for the nodes
	color_map=[]

	#add nodes
	for node in nodeSet:
		if "s" in node:
			g.add_node(node)
			color_map.append('green')
		else:
			g.add_node(node)
			color_map.append('yellow')

	#add links
	#for link, i in zip(linkSet, range(len(linkSet))):
		#g.add_edge(link[0], link[1], link=('L' + str(link_id[i])))
		#print("link: " + str(link[0]) + ", " + str(link[1]))

	for link in linkSet:
		g.add_edge(link[0], link[1], link=(str(link[0])+"-"+str(link[1])))


	colors = [u[1] for u in g.nodes(data="color")]
	
	node_cfg = nx.spring_layout(g)

	nx.draw(g, pos=node_cfg, node_size=1000, node_color=color_map, with_labels = True)

	edge_labels = nx.get_edge_attributes(g, "link")
	nx.draw_networkx_edge_labels(g, pos=node_cfg, edge_labels=edge_labels)

	plt.savefig("files/topo.png", format="PNG")
	