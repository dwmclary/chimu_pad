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

def extract_player(p, id, teams):
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
		if teams[t]["abbreviation"] == team_name:
			team_id = teams[t]["id"]
			break
	
	player = Player(id, name, int(number), team_name, int(team_id), position, comment)
	return player
	
def main(roster, teams):
	roster_counter = 1
	roster = open(roster).readlines()
	players = []
	for player in roster:
		player = extract_player(player, roster_counter, teams)
		roster_counter += 1
		players.append(player.get_hash())
	
	yaml_buffer = sanitize_yaml(yaml.dump(players, default_flow_style=False))
	for y in yaml_buffer:
		print y
		
	
if __name__ == "__main__":
	roster = sys.argv[1]
	teams = yaml.load(open(sys.argv[2]).read())
	team_hash = {}
	for t in teams:
		key = t.keys()[0]
		team_hash[key] = t[key]
	main(roster, team_hash)