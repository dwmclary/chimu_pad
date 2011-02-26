#! /usr/bin/env python
from glob import glob
import networkx as nx
import re
graphs = glob("Match*.gml")
scaling = lambda x:(x+18.45)*0.465

def graph_to_js_list(G):
	nodes = []
	edges = []
	for n in G.nodes(data=True):
		if "scaled_size" in n[1]:
			node_string = str(n[1]["label"]) + " size:%s"%n[1]["scaled_size"]
		else:
			node_string = str(n[1]["label"])
		nodes.append(node_string)
		
	for e in G.edges(data=True):
		if "scaled_lb_weight" in e[2]:
			edge_string = str(G.node[e[0]]["label"]) + " " + str(G.node[e[1]]["label"]) + " weight:%s"%e[2]["scaled_lb_weight"]
		else:
			edge_string = str(G.node[e[0]]["label"]) + " " + str(G.node[e[1]]["label"])
		edges.append(edge_string)
	return ",".join(nodes), ",".join(edges)

f = open("graphs.csv", "w")
print >> f, "id,match_id,team_id,kind,nodes,edges"

graph_id = 1
for g in graphs:
	G = nx.read_gml(g)
	g = re.sub(".gml", "",g)
	match_data = g.split("_")
	if "_t" in g:
		kind = "single"
	else:
		kind = "double"
	match_id = int(re.sub("m","", match_data[1]))
	if kind == "single":
		team_id = int(re.sub("t","", match_data[2]))
	else:
		team_id = None
		
	#rescale the nodes
	for n in G.nodes(data=True):
		if "size" in n[1]:
			if scaling(n[1]["size"]) >= 0:
				n[1]["scaled_size"] = scaling(n[1]["size"])
		else:
			n[1]["scaled_size"] = 0.0
	
	#get the node and edge lists
	nodes, edges = graph_to_js_list(G)
	
	#write it to file
	if kind == "single":
		print >> f, str(graph_id)+","+str(match_id)+","+str(team_id)+","+"single,"+'"'+nodes+'","'+edges+'"'
	elif kind == "double":
		print >> f, str(graph_id)+","+str(match_id)+","+","+"double,"+'"'+nodes+'","'+edges+'"'
	
	graph_id += 1

f.close()
		
	
	
	

	
