#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Daniel McClary on 2011-02-20.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import networkx as nx
import random
from math import fabs,log10

NUMBALLS = 2000000
MAXTABLE = 10000

BETWEENNESS_TUPLES = 26

rating_scale = 10.0

meanW = 4.34
stdW = 0.235

meanLW = 3.168
stdLW = 0.4051
name = lambda n:n[0]
weight = lambda e:e[2]["weight"]
to = lambda e:e[1]
accuracy = lambda n:n[1]["accuracy"]
in_capacity = lambda n,G:sum(map(weight,G.in_edges(n, data=True)))
out_capacity = lambda n,G:sum(map(weight,G.out_edges(n, data=True)))
ignored_nodes = ["shots_wide", "shots_on_goal","lost"]
def determine_ball_count(G):
	#for each player, compute the likelihood of losing the ball

	for node in G.nodes(data=True):
		if name(node) not in ignored_nodes:
			outweight = 0
			for edge in G.edges(name(node), data=True):
				if to(edge) not in ignored_nodes:
					outweight += weight(edge)
			if accuracy(node) > 0:  
				outweight = int(outweight*100.0/accuracy(node))-outweight
			else:
				outweight = 100
			#we're re-weighting the node "lost" to reflect the likelihood of a lost pass
			if "lost" in map(to, G.out_edges(name(node))):
				G.remove_edge(name(node),"lost")
				G.add_edge(name(node),"lost", weight=outweight)
			
	#capacity is flow capacity -- the sum of edge weights, both in and out
	#determine the number of plays created and translate that to a ball count
	plays_created = 0
	for node in G.nodes():
		creation = (out_capacity(node,G) - in_capacity(node,G))
		if creation > 0:
			plays_created += creation
	ball_count = float(plays_created)
	return ball_count

def simulate_ball_movement(G1, G2):
	#simulate ball movement for the DiGraph G
	ball_counts = []
	graphs = [G1,G2]
	normalized_graphs = []
	for G in [G1, G2]:
		ball_counts.append(determine_ball_count(G))
	f = lambda x:x/sum(ball_counts)
	ball_ratio = map(f, ball_counts)
	print ball_counts, ball_ratio
	betweenness_node_weight = {}
	betweenness_node_weights = []
    
	betweenness_link_weight = {}
	betweenness_link_weights = []
	
	unified_bcws = []
	unified_bclws = []

	for G in graphs:
		
		betweenness_node_weight[G.graph["team"]] = {}
		betweenness_link_weight[G.graph["team"]] = {}

		
		#I'm not sure if this hash needs to be here or if it's just more or Jordi's copy-paste bullshit
		players = {}
		for node in G.nodes(data=True):
			total_weight = out_capacity(name(node),G)
			next = {}
			ballsW = 0
			i = 0
			for edge in G.out_edges(name(node), data=True):
				for j in range(i, i+weight(edge)):
					next[j] = to(edge)
				i += int(weight(edge))
			node_info = {"total_weight": total_weight, "next": next, "ballsW":ballsW}
			if name(node) not in ignored_nodes:
				players[name(node)] = node_info
				
		#I believe this is computing player pass differentials and placing them in a hash
		player_pass_difference = {}
		plays_created = 0
		for node in G.nodes():
			if (out_capacity(node,G) - in_capacity(node,G)) > 0:
				player_pass_difference[node] = out_capacity(node,G) - in_capacity(node,G)
				plays_created += player_pass_difference[node]
		

				
		minimum_pass = 0
		create_play_node = [0 for i in range(MAXTABLE)]
		
		for k_2, v_2 in player_pass_difference.items():
			for i in range(minimum_pass, minimum_pass+v_2*MAXTABLE/plays_created):
				create_play_node[i] = int(k_2)
			minimum_pass += v_2*MAXTABLE/plays_created
		

		tmp = create_play_node[minimum_pass-2]
		for i in range(minimum_pass-1,MAXTABLE):
			create_play_node[i]=tmp
		

		#begin random walk
		completed_plays = 0
		play_lengths = []

		for walk in range(0,int(NUMBALLS*ball_ratio[graphs.index(G)])):
			# #quick percentage tracking output
			# 		if int((walk/(NUMBALLS*ball_ratio[graphs.index(G)]))*100) % 2 == 0:
			# 			print str(100*float(walk)/(NUMBALLS*ball_ratio[graphs.index(G)])) + "%"
			lost, goal, wide = False, False, False
			passes, passes_to = [], []
			
			#select the node at which play starts
			play_at = random.randint(0,MAXTABLE-1)
 			i = 0
			nodes = G.nodes()

			while str(nodes[i]) != str(create_play_node[play_at]):
				i += 1
				if i >= len(G.nodes()):
					print play_at, create_play_node[play_at], "---"
			actual_node = G.nodes(data = True)[i]

			passes.append(name(actual_node))
			play_count = 0
			while not (lost or goal or wide):
				play_count += 1
				#this is an arbitrary/sane threshold set to prevent plays from going too deep -- 
				#1000 passes is unlikely to occur in a soccer match
				#without a turnover
				if play_count > 1000:
					lost = True
				play_at = random.randint(0,players[name(actual_node)]["total_weight"]-1)

				next_node = players[name(actual_node)]["next"][play_at]
				
				if next_node == "shots_on_goal":
					goal = True
				elif next_node == "shots_wide":
					wide = True
				elif next_node == "lost":
					lost = True
				else:
					passes.append(next_node)
					passes_to.append((name(actual_node), next_node))
				
				if goal or wide:
					if goal:
						for p in passes:
							players[p]['ballsW'] += 1.0
						for p in passes_to:
							if p in betweenness_link_weight[G.graph["team"]]:
								betweenness_link_weight[G.graph["team"]][p] += 1
							else:
								betweenness_link_weight[G.graph["team"]][p] = 1
					else:
						for p in passes:
							players[p]['ballsW'] += 0.5
						for p in passes_to:
							if p in betweenness_link_weight[G.graph["team"]]:
								betweenness_link_weight[G.graph["team"]][p] += 0.5
							else:
								betweenness_link_weight[G.graph["team"]][p] = 0.5
								
					completed_plays += 1
					play_lengths.append(len(passes))

		total_play_lengths = sum(play_lengths)

		betweenness_link_weights = filter(lambda x:x > 0, betweenness_link_weight[G.graph["team"]].values())
		betweenness_node_weights = filter(lambda x:x > 0, betweenness_node_weight[G.graph["team"]].values())
		
		normalized_graph = nx.DiGraph(team=G.graph["team"])
		bcWs = []
		bcLWs = []
		for node in G.nodes():
			if node not in ignored_nodes:
				normalized_graph.add_node(node)
				bcW = players[node]['ballsW']
				if bcW == 0:
					bcWs.append((0 - meanW)/stdW)
					G.node[node]["size"] = (0.0 - meanW)/stdW
					G.node[node]["bcW"] = 0
					G.node[node]["log_bcW"] = 0
					normalized_graph.node[node]["size"] = (0 - meanW)/stdW
					normalized_graph.node[node]["bcW"] = 0
					normalized_graph.node[node]["log_bcW"] = 0
				else:
					bcWs.append((log10(bcW) - meanW)/stdW)
					G.node[node]["size"] = (log10(bcW) - meanW)/stdW
					G.node[node]["bcW"] = bcW
					G.node[node]["log_bcW"] = log10(bcW)
					normalized_graph.node[node]["size"] = (log10(bcW) - meanW)/stdW
					normalized_graph.node[node]["bcW"] = bcW
					normalized_graph.node[node]["log_bcW"] = log10(bcW)
					
		for pass_entry in betweenness_link_weight[G.graph["team"]]:
			bcLW = betweenness_link_weight[G.graph["team"]][pass_entry]
			if bcLW > 0:
				bcLWs.append(float(log10(bcLW)-meanLW))
				G.edge[pass_entry[0]][pass_entry[1]]['lb_weight'] = float(log10(bcLW)-meanLW)
				G.edge[pass_entry[0]][pass_entry[1]]['b_weight'] = bcLW
				G.edge[pass_entry[0]][pass_entry[1]]['log_b'] = log10(bcLW)
				normalized_graph.add_edge(pass_entry[0],pass_entry[1], weight=float(log10(bcLW)-meanLW), b_weight=bcLW, log_b=log10(bcLW))
		for node in G.nodes(data=True):
			if "size" in node[1]:
				node[1]["scaled_size"] = ((node[1]["size"]-min(bcWs))/(max(bcWs) - min(bcWs)))*rating_scale
		for edge in G.edges(data=True):
			if "lb_weight" in edge[2]:
				edge[2]['scaled_lb_weight'] = ((edge[2]["lb_weight"]-min(bcLWs))/(max(bcLWs) - min(bcLWs)))*rating_scale
		
		unified_bcws += bcWs
		unified_bclws += bcLWs
		#finally, normalize the node sizes and lb_weights between 0 and 10
		normalized_graphs.append(normalized_graph)
		
	#create a unified graph and rescale it 
	unified_graph = nx.DiGraph()
	for G in graphs:
		unified_graph.add_nodes_from(G.nodes(data=True))
		unified_graph.add_edges_from(G.edges(data=True))

	for n in unified_graph.nodes(data=True):
		if "size" in n[1]:
			n[1]["scaled_size"] = ((n[1]["size"]-min(unified_bcws))/(max(unified_bcws) - min(unified_bcws)))*rating_scale
	for e in unified_graph.edges(data=True):
		if "lb_weight" in e[2]:
			e[2]['scaled_lb_weight'] = ((e[2]["lb_weight"]-min(unified_bclws))/(max(unified_bclws) - min(unified_bclws)))*rating_scale
	print unified_graph.nodes(data=True)
	return [graphs, unified_graph]


if __name__ == '__main__':
	main()

