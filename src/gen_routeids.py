# Copyright [2019-2022] Universidade Federal do Espirito Santo
#                       Instituto Federal do Espirito Santo
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

from polka.tools import calculate_routeid, print_poly
DEBUG = False

def generateRouteIDs(route_seq, link_seq, size):

	if (size == 16):
		s = [
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],  # s1
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],  # s2
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],  # s3
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],  # s4
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],  # s5
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1],  # s6
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],  # s7
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1],  # s8
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1],  # s9
			[1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1]]  # s10
	elif (size == 8):
		s = [
			[1, 0, 0, 0, 1, 1, 0, 1, 1],  # s1
			[1, 0, 0, 0, 1, 1, 1, 0, 1],  # s2
			[1, 0, 0, 1, 0, 1, 0, 1, 1],  # s3
			[1, 0, 0, 1, 0, 1, 1, 0, 1],  # s4
			[1, 0, 0, 1, 1, 1, 0, 0, 1],  # s5
			[1, 0, 0, 0, 0, 0, 0, 0, 0],  # s6
			[1, 0, 0, 0, 0, 0, 0, 0, 0],  # s7
			[1, 0, 0, 0, 0, 0, 0, 0, 0],  # s8
			[1, 0, 0, 0, 0, 0, 0, 0, 0],  # s9
			[1, 0, 0, 0, 0, 0, 0, 0, 0]]  # s10
	else:
		print("CRC %d not supported", size)

	routeids = []

	for i in range(len(route_seq)):
		route = "From " + ", ".join(route_seq[i]) + " ===="	
		print(route)

		# Parse user data
		route_numbers = [int(item[2:]) -1 for item in route_seq[i]]

		nodes = []
		# defining the nodes 
		for n in route_numbers: 
			nodes.append(s[n])

		# defining output ports
		o = [list(map(int, bin(ports)[2:])) for ports in link_seq[i]]

		ids = calculate_routeid(nodes, o, debug=DEBUG)

		binary_string = ''.join(map(str, ids))

		# Convert the binary string to a decimal number
		routeids.append(int(binary_string, 2))

	return routeids, s
