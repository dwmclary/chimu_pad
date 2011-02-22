#! /usr/bin/env python
import sys
import re
import networkx as nx
import ball_simulation
import yaml

class Play(object):
	#this class is the representation of a player's performance which can be dumped to JSON
	def __init__(self, pid, mid, player_id, position, shots, goals,pc, pa,rating):
		self.id = pid
		self.match_id = mid
		self.player_id = player_id
		self.position = position
		self.shots = shots
		self.goals = goals
		self.pc = pc
		self.pa = pa
		self.rating = rating
	
def get_teams(data):
	#determine who the teams are:
	teams = set()
	team_count = {}
	#teams always come first
	for line in data:
		teams = teams.union([line[0]])
	#determine the number of players on each team
	for line in data:
		if line[0] in teams:
			if line[0] not in team_count:
				team_count[line[0]] = 1
			else:
				team_count[line[0]] += 1
	#split the file into teams
	team_data_sets = {}
	offset = 0
	for team in team_count:
		team_data_sets[team] = data[offset:offset+team_count[team]]
		offset += team_count[team]
		
	return team_data_sets

def build_pass_matrix(tds, players):
	pass_matrix = {}
	player_count = len(tds)
	#offset accounts for team name and player number
	for i in range(len(tds)):
		#for each row
		team_name = tds[i][0]
		player_number = fetch_player_id(tds[i][1], players)
		pass_matrix[player_number] = {}
		player_passes = []
		j_count = 0
		end_of_passes = len(tds)
		f = lambda x:re.sub("-","0",x)
		pass_slice = map(int, map(f, tds[i][2:end_of_passes+1]))
		pass_count = 0
		pass_index = 0
		
		while pass_count < len(pass_slice)+1:
			if pass_count == i:
				player_passes.append({tds[pass_count][1]:0})
			else:
				player_passes.append({tds[pass_count][1]:pass_slice[pass_index]})
				pass_index += 1
			pass_count += 1
				
		#offsets for completed, attempted passes, accuracy
		pc = end_of_passes+1
		pa = end_of_passes+2
		accuracy = end_of_passes+3
		pass_matrix[player_number]["passes_completed"] = int(tds[i][pc])
		pass_matrix[player_number]["passes_attempted"] = int(tds[i][pa])
		pass_matrix[player_number]["accuracy"] = int(re.sub("%","",tds[i][accuracy]))
		pass_matrix[player_number]["passes"] = player_passes
	return pass_matrix

def build_shot_dictionary(shots, teams):
	shot_dictionary = {}
	for t in teams:
		shot_dictionary[t] = {}
		
	for s in shots:
		team, player, goals, shots_on_goal, total_shots= s.split()
		shot_dictionary[team][player] = {"goals":int(goals), "shots_on_goal":int(shots_on_goal),\
		 "shots_wide":int(total_shots)-int(shots_on_goal), "total_shots": int(total_shots)}
	return shot_dictionary
	
def append_shots(team, pass_matrix, shot_dictionary, players):
	for p in pass_matrix:
		#look up the shot data for this player
		shots = shot_dictionary[team][fetch_player_number(p,players)]
		for s in shots:
			pass_matrix[p][s] = shots[s]
			
def build_team_graph(t, pass_matrix, players):
	G = nx.DiGraph(team=t)
	#add two nodes for shots wide and shots on goal
	G.add_node('shots_wide')
	G.add_node('shots_on_goal')
	G.add_node('lost')
	for p in pass_matrix:
		G.add_node(p)
		G.node[p]["accuracy"] = pass_matrix[p]["accuracy"]
		#add the shots wide and on goal edges
		f = lambda x:x.values()[0]
		all_passes = map(f,pass_matrix[p]["passes"])
		g = lambda x:int(x)
		all_pass_percentages = map(g,all_passes)
		if pass_matrix[p]["shots_on_goal"] > 0:
			G.add_edge(p,"shots_on_goal", weight=int(pass_matrix[p]["shots_on_goal"]))
		if pass_matrix[p]["shots_wide"] > 0:
			G.add_edge(p, "shots_wide", weight=int(pass_matrix[p]["shots_wide"]))
		G.add_edge(p, "lost", weight=int(pass_matrix[p]["passes_attempted"]-pass_matrix[p]["passes_completed"]))
		#add a weighted edge for each pass
		passes = pass_matrix[p]["passes"]
		for k in passes:
			if k.values()[0] != 0:
				G.add_edge(p,fetch_player_id(k.keys()[0], players), weight=all_pass_percentages[passes.index(k)])
	return G
	
def fetch_team_id(team_name, teams):
	for t in teams:
		key = t.keys()[0]
		if t[key]["abbreviation"] == team_name:
			return t[key]["id"]
	return None
	
def fetch_player_id(player_number, players):
	for p in players:
		if str(players[p]["number"]) == player_number:
			return players[p]["id"]
	return None
	
def fetch_player_number(player_id, players):
	for p in players:
		if player_id == players[p]["id"]:
			return str(players[p]["number"])
	return None
	
def fetch_player_position(player_id, players):
	for p in players:
		if player_id == players[p]["id"]:
			return str(players[p]["position"])
	return None
	
def make_plays(match_id, pass_matrix, players, starting_play_id=1):
	play_id = starting_play_id
	plays = []
	for p in pass_matrix:
 		player_id = p
		position = fetch_player_position(p, players)
		shots = pass_matrix[p]["total_shots"]
		goals = pass_matrix[p]["goals"]
		pa = pass_matrix[p]["passes_attempted"]
		pc = pass_matrix[p]["passes_completed"]
		rating = 0.0
		new_play = Play(play_id, match_id, player_id, position, shots, goals, pc, pa, rating)
		plays.append(new_play)
	return plays
	
def graph_to_js_list(G):
	nodes = []
	edges = []
	for n in G.nodes(data=True):
		if "scaled_size" in n[1]:
			node_string = str(n[0]) + " {size:%s}"%n[1]["scaled_size"]
		else:
			node_string = str(n[0])
		nodes.append(node_string)
		
	for e in G.edges(data=True):
		if "scaled_lb_weight" in e[2]:
			edge_string = str(e[0]) + " " + str(e[1]) + " {weight:%s}"%e[2]["scaled_lb_weight"]
		else:
			edge_string = str(e[0]) + " " + str(e[1])
		edges.append(edge_string)
	return ",".join(nodes), ",".join(edges)
	
def main(match_id, pass_file, shots_file, teams, matches, players):
	team_data = yaml.load(open(teams).read())
	matches = yaml.load(open(matches).read())
	players = yaml.load(open(players).read())
	plays = []
	if "passes.txt" not in pass_file:
		print >> sys.stderr, "Not a pass file"
		exit()
	if "shots.txt" not in shots_file:
		print >> sys.stderr, "Not a shots file"
		exit()
	
	pass_data = open(pass_file).readlines()
	shot_data = open(shots_file).readlines()

	#sanitize the pass data and split on whitespace
	for i in range(len(pass_data)):
		pass_data[i] = pass_data[i].strip().split()
		
	teams = get_teams(pass_data)
	shot_d = build_shot_dictionary(shot_data, teams)
	graphs = {}
	for team in teams:
		p = build_pass_matrix(teams[team], players)
		team_id = fetch_team_id(team, team_data)
		append_shots(team, p, shot_d, players)
		play_id = len(plays)+1
		plays += make_plays(match_id, p, players, play_id)
		graphs[team] = build_team_graph(team_id, p, players)
	team_graphs, unified_graph = ball_simulation.simulate_ball_movement(*graphs.values())
	#append the unified ratings to the play objects
	for p in plays:
		for n in unified_graph.nodes(data=True):
			if n[0] == p.player_id:
				p.rating = n[1]["scaled_size"]
				
	#dump the graphs to js compatible strings
	u_nodes, u_edges = graph_to_js_list(unified_graph)
	print u_nodes
	print u_edges


if __name__ == "__main__":
	match_id = int(sys.argv[1])
	passes = sys.argv[2]
	shots = sys.argv[3]
	teams = sys.argv[4]
	matches = sys.argv[5]
	players = sys.argv[6]

	main(match_id, passes, shots, teams, matches, players)