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
 
from collections import defaultdict

#class to represent the graph used in the dijkstra algorithm
class Graph:
	def __init__(self):
		self.nodes = set()
		self.edges = defaultdict(list)
		self.distances = {}
    
	def addNode(self,value):
		self.nodes.add(value)
    
	def addEdge(self, fromNode, toNode, distance):
		self.edges[toNode].append(fromNode)
		self.distances[(toNode, fromNode)] = distance
		self.edges[fromNode].append(toNode)
		self.distances[(fromNode, toNode)] = distance

#dijkstra algorithm to get the shortest between all hosts, params = (graph and initial node)
def dijkstra(graph, initial):
    visited = {initial : 0}
    path = defaultdict(list)

    nodes = set(graph.nodes)

    while nodes:
        minNode = None
        for node in nodes:
            if node in visited:
                if minNode is None:
                    minNode = node
                elif visited[node] < visited[minNode]:
                    minNode = node
        if minNode is None:
            break

        nodes.remove(minNode)
        currentWeight = visited[minNode]

        for edge in graph.edges[minNode]:
            weight = currentWeight + graph.distances[(minNode, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge].append(minNode)
    
    return visited, path


#function do find the interconnection ID from two nodes
def findConnectionID(nodeOne, nodeTwo, interconnections, path):
	for i in interconnections:
		if i[0] == path[nodeOne] and i[1] == path[nodeTwo]:
			return i[2]
		if i[0] == path[nodeTwo] and i[1] == path[nodeOne]:
			return i[2]

#funcion to generate all table entries to perform the l3 addressing, params: (all hosts, all switches and all interconnections)
def generateTableEntries(hostsReceived, switchesReceived, intReceived, sw_ids):
	print(sw_ids)
	#data structures used in the processment
	hosts = []
	hostAndIPs = {}
	switches = []
	interconnections = []
	pysPorts = {}	
	#parser the list of hosts, the dictionary of hosts and IPs and the dictionary of hosts and physical port
	for i in hostsReceived:
		hosts.append(i[0])
		hostAndIPs.update({i[0]:i[7]})
		pysPorts.update({i[0]:i[2]})
	#parser the list of switches
	for j in switchesReceived:
		switches.append(j)
	#parser the list of interconnections and create a unique ID for each interconnection
	for index, k in enumerate(intReceived):
		aux = [k[0], k[1], index]		
		interconnections.append(aux)

	#list of all pathes, created pathes (to not generate duplicated pathes) and table entries
	allPathes = []
	visi= []
	tableEntries = []

	#create the graph using network informations
	g = Graph();
	for host in hosts:
		g.addNode(host)

	for sw in switches:
		g.addNode(sw)
	#sets the weight of all edges to 1 for dijkstra process
	for inter in interconnections:
		g.addEdge(inter[0], inter[1], 1)


	#iterate for all hosts to generate pathes from all hosts
	for hosti in hosts:
		
		#run dijkstra from the current node
		vis, pat=dijkstra(g, hosti)
		
		#find a host that there is no path starting from hosti
		h = "NULL"
		for i in hosts:
			if i in visi:
				continue
			else:
				h = i
				break
		#if cannot find, break this interaction because all pathes from this node were created
		if h == "NULL":
			break
		visi.append(h);	

		#recreate the paths
		for host in hosts:
			if host == h:
				break
			path = []
			current = host
			while current != h:
				path.append(current)
				current = pat[str(current)][0]
			path.append(current)
			path.reverse()
			allPathes.append(path)
	
	#from all pathes created, create the table entries
	for path in allPathes:
		hStart = path[0]
		hFinal = path[len(path)-1]
		ipStart = hostAndIPs[hStart]
		ipFinal = hostAndIPs[hFinal]
		#for this path, create the entries for all switches
		for node in range(1, len(path)-2):
			ID = findConnectionID(node, node+1, interconnections, path)
			IDprevious = findConnectionID(node-1, node, interconnections, path)
			IDnext = findConnectionID(node+1, node+2, interconnections, path)
			entry = [ID, ipStart, "send_next", IDprevious, sw_ids[path[node]]]
			if entry not in tableEntries:
				tableEntries.append(entry)
			entry = [ID, ipFinal, "send_next", IDnext, sw_ids[path[node +1]]]
			if entry not in tableEntries:
				tableEntries.append(entry)

		#for this path, create the entry for host interconnection if the host is connected in other host
		if len(path) == 2:
			ID = findConnectionID(0, 1, interconnections, path)
			entry = [ID, ipStart, "send", pysPorts[hStart]]
			if entry not in tableEntries:
				tableEntries.append(entry)
			entry = [ID, ipFinal, "send", pysPorts[hFinal]]
			if entry not in tableEntries:
				tableEntries.append(entry)
		#create the entry for the host interconnection if the host is connected with one switch
		else:
			#create the entry for the initial host
			IDst = findConnectionID(0, 1, interconnections, path)
			IDdest = findConnectionID(1, 2, interconnections, path)
			entry = [IDst, ipStart, "send", pysPorts[hStart]]
			if entry not in tableEntries:
				tableEntries.append(entry)
			entry = [IDst, ipFinal, "send_next", IDdest, sw_ids[path[1]]]
			if entry not in tableEntries:
				tableEntries.append(entry)
			#creathe the entry for the final host
			IDst = findConnectionID(len(path)-2, len(path)-1, interconnections, path)
			IDdest = findConnectionID(len(path)-3, len(path)-2, interconnections, path)
			entry = [IDst, ipFinal, "send", pysPorts[hFinal]]
			if entry not in tableEntries:
				tableEntries.append(entry)
			entry = [IDst, ipStart, "send_next", IDdest, sw_ids[path[len(path)-2]]]
			if entry not in tableEntries:
				tableEntries.append(entry)
	#2 1 1 0 2 0
	#return all table entries
	#print(tableEntries)
	return tableEntries, allPathes



