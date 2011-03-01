#! /usr/bin/env python

import sys
import yaml
from sanitize_yaml import sanitize_yaml

class Player(object):
	
	def __init__(self, id, name, number, team, team_id, position, comment="", current_rating=0.0):
		self.id = id
		self.name = name
		self.number = number
		self.team = team
		self.team_id = team_id
		self.position = position
		self.comment = comment
		self.current_rating = current_rating
		
	def get_hash(self):
		return {self.name:{"id": self.id, "name":self.name, "number":self.number, "team_id":self.team_id, "position":self.position,\
		 "comment":self.comment, "current_rating":self.current_rating, "team":self.team}}

def transform_to_list_entry(entry):
	name = entry.keys()[0]
	entry = entry[name]
	return {name:{"id": entry["id"], "name":entry["name"], "number":entry["number"], "team_id":entry["team_id"], "position":entry["position"],\
	 "comment":entry["comment"], "current_rating":entry["current_rating"], "team":entry["team"]}}
	
def extract_player(p, id, teams, league_id):
	#get the fields from the text file
	p = p.strip().split(";")
	team_name = p[0]
	number = p[1]
	name = p[2]
	position = p[3]
	comment = p[5]
	team_id = None
	#find the appropriate team name and team_id from the hash
	#this holds for the world cup, remains to be seen for EC and other leagues/teams
	for t in teams:
		if teams[t]["abbreviation"] == team_name and teams[t]["league_id"] == league_id:
			team_id = teams[t]["id"]
			break
	
	player = Player(id, name, int(number), team_name, int(team_id), position, comment)
	return player
	
def main(roster, teams, league_id, players):
	roster_counter = 1
	roster = open(roster).readlines()
	if len(roster) == 1:
		#this is indicative of the \r that Jordi's (probably windows) text editor uses as newlines (so check for it)
		if "\r" in roster[0]:
			roster = roster[0].split("\r")
		else:
			print roster[0]
			exit()
	output = []
	if not players:
		players = {}
	else:
		for p in players:
			output.append({p:players[p]})
			roster_counter += 1
		
	for player in roster:
		player = extract_player(player, roster_counter, teams, league_id)
		roster_counter += 1
		players[player.name] = player.get_hash()
		output.append(player.get_hash())
		

	yaml_buffer = sanitize_yaml(yaml.dump(output, default_flow_style=False))
	for y in yaml_buffer:
		print y
		
	
if __name__ == "__main__":
	roster = sys.argv[1]
	teams = yaml.load(open(sys.argv[2]).read())
	league_id = 1 #quick hack for league id's
	if len(sys.argv) > 3:
		league_id = int(sys.argv[3])
	if len(sys.argv) > 4:
		players = yaml.load(open(sys.argv[4]).read())
	else:
		players = None
	team_hash = {}
	for t in teams:
		key = t.keys()[0]
		team_hash[key] = t[key]
	main(roster, team_hash, league_id, players)