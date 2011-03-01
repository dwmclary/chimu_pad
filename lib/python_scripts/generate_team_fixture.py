#! /usr/bin/env python
import sys
import yaml
from sanitize_yaml import sanitize_yaml
import random

class Team(object):
	
	def __init__(self, id, league_id, name, country, abbrv, current_rating=0.0, altname=None):
		self.id = id
		self.league_id = league_id
		self.name = name
		self.country = country
		self.abbreviation = abbrv
		self.altname = altname
	def get_hash(self):
		if self.altname:
			return {self.altname:{"id":self.id, "league_id":self.league_id, "name":self.name, "country":self.country, "abbreviation":self.abbreviation}}
		else:
			return {self.name:{"id":self.id, "league_id":self.league_id, "name":self.name, "country":self.country, "abbreviation":self.abbreviation}}

def get_max_team_id(team_list):
	max_counter = 0
	team_id = lambda x:x.values()[0]["id"]
	for t in team_list:
		if max_counter < team_id(t):
			max_counter = team_id(t)
	max_counter += 1 #we're starting at 1 past the last id
	return max_counter
	
def exists(team_name, team_hash):
	for t in team_hash.values():
		if team_name in t.keys()[0]:
			return True
	return False

def main(team_file, fixture, existing_teams=None, league_id = 1):
	#read in a match file and make a set of match objects out of it
	#assume for world and euro cup that the country name is the same as the team name
	team_hash = {}
	output = []
	team_counter = 1
	teams = open(team_file).readlines()
	#check to see if we've been provided a set of existing teams
	if existing_teams:
		existing_teams = yaml.load(open(existing_teams))
		for t in existing_teams:
			team_hash[team_counter] = t
			team_counter += 1
		output = existing_teams
		#get the new initial counter value
		#team_counter = get_max_team_id(existing_teams)
		
	for line in teams:
		data = line.strip().split(";")
		name = data[1]
		country = data[1]
		abbrv = data[0]
		if exists(name, team_hash):
			alt_name =  name + str(random.randint(1,1000)) #I'm making an assumption that we won't have 1000 teams with the same name
			print alt_name
			t = Team(team_counter, league_id, name, country, abbrv,altname=alt_name)
		else:
			t = Team(team_counter, league_id, name, country, abbrv)
		output.append(t.get_hash())
		team_hash[team_counter] = t.get_hash()
		team_counter += 1
	if fixture:
		yaml_buffer = sanitize_yaml(yaml.dump(output, default_flow_style=False))
		for y in yaml_buffer:
			print y
	else:
		print yaml.dump(output, default_flow_style=False)
	

if __name__ == "__main__":
	team_file = sys.argv[1]
	team_yaml = None
	league_id = 1 # this is all a very quick hack, so here's a default team id
	if len(sys.argv) > 3:
		team_yaml = sys.argv[2]
		league_id = int(sys.argv[3])
	
 	if len(sys.argv) > 4:
		fixture = True
	else:
		fixture = False
	main(team_file, fixture, team_yaml, league_id)