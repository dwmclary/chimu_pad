#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Daniel McClary on 2011-02-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import yaml
from sanitize_yaml import sanitize_yaml


class Match(object):
	
	def __init__(self, id, league_id, home_team_id, away_team_id, home_team_score, away_team_score, location, won_id=None, date_string=None):
		self.league_id = league_id
		self.id = id
		self.home_team_id = home_team_id
		self.away_team_id = away_team_id
		self.home_team_score = home_team_score
		self.away_team_score = away_team_score
		self.location = location
		if won_id:
			self.won_id = won_id
		else:
			self.won_id = -1
		if date_string:
			year = "2010" #hack for world cup, needs to be fixed for generality
			seconds = "00"
			d, t = date_string.split("-")
			month, day = d.split("/")
			h, m = t.split(":")
			self.date_string = year+"-"+day+"-"+month+" "+h+":"+m+":"+seconds
	
	def get_hash(self):
		return {"Match_"+str(self.id):{"id":self.id,"league_id":self.league_id, "home_team_id":self.home_team_id, "away_team_id":self.away_team_id,\
		"home_team_score":self.home_team_score, "away_team_score":self.away_team_score, "location":self.location, "winning_team_id":self.won_id,\
		"match_date":self.date_string}}
			

def parse_match(line, teams, league_id):
	line = line.split(";")
	match_id = int(line[0])
	match_date = line[1]
	location = line[2].split("-")[0].strip()
	home_team = line[3]
	away_team = line[4]
	home_score = int(line[5])
	away_score = int(line[6])
	home_id = None
	away_id = None
	won_id = None
	for t in teams:
		if teams[t]["abbreviation"] == home_team and teams[t]["league_id"] == league_id:
			home_id = teams[t]["id"]
			league_id = teams[t]["league_id"]
		elif teams[t]["abbreviation"] == away_team and teams[t]["league_id"] == league_id:
			away_id = teams[t]["id"]
		elif away_id and home_id:
			break
	if home_score > away_score and home_id:
		won_id = home_id
	elif away_score > home_score and away_id:
		won_id = away_id
	
	return Match(match_id, league_id, home_id, away_id, home_score, away_score, location, won_id, match_date)

	
def main(match_file, teams, league_id, fixture=False, existing_matches=None):
	matches = open(match_file).readlines()
	if existing_matches:
		match_list = yaml.load(open(existing_matches))
	else:
		match_list = []
	for m in matches:
		match = parse_match(m, teams, league_id)
		match_list.append(match.get_hash())
	
	if fixture:
		yaml_buffer = sanitize_yaml(yaml.dump(match_list, default_flow_style=False))
		for y in yaml_buffer:
			print y
	else:
		print yaml.dump(match_list, default_flow_style=False)
	
	


if __name__ == '__main__':
	if len(sys.argv) > 2:
		match_list = sys.argv[1]
		team_file = sys.argv[2]
		teams = yaml.load(open(sys.argv[2]).read())
		team_hash = {}
		league_id = 1
		existing_matches = None
		if len(sys.argv) > 3:
			league_id = int(sys.argv[3])
		if len(sys.argv) > 4:
			existing_matches = sys.argv[4]
		if len(sys.argv) > 5:
			fixture = True
		else:
			fixture = False
		for t in teams:
			key = t.keys()[0]
			team_hash[key] = t[key]
		main(match_list, team_hash, league_id, fixture, existing_matches)

