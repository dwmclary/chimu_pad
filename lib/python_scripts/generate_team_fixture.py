#! /usr/bin/env python
import sys
import yaml
from sanitize_yaml import sanitize_yaml

class Team(object):
	
	def __init__(self, id, league_id, name, country, abbrv, current_rating=0.0):
		self.id = id
		self.league_id = league_id
		self.name = name
		self.country = country
		self.abbreviation = abbrv
	
	def get_hash(self):
		return {self.name:{"id":self.id, "league_id":self.league_id, "name":self.name, "country":self.country, "abbreviation":self.abbreviation}}

def main(team_file, fixture, league_id = 1):
	#read in a match file and make a set of match objects out of it
	#assume for world and euro cup that the country name is the same as the team name
	team_hash = {}
	output = []
	team_counter = 1
	teams = open(team_file).readlines()
	for line in teams:
		data = line.strip().split(";")
		t = Team(team_counter, league_id, data[1], data[1], data[0])
		output.append(t.get_hash())
		team_hash[team_counter] = t
		team_counter += 1
	if fixture:
		yaml_buffer = sanitize_yaml(yaml.dump(output, default_flow_style=False))
		for y in yaml_buffer:
			print y
	else:
		print yaml.dump(output, default_flow_style=False)
	

if __name__ == "__main__":
	team_file = sys.argv[1]
	if len(sys.argv) > 2:
		fixture = True
	else:
		fixture = False
	main(team_file, fixture)