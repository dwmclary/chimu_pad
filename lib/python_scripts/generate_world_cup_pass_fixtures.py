#! /usr/bin/env python

from glob import glob
import os, sys
import re

games_extension = "games/"

def main(directory, league_id):
	game_dir = directory+games_extension
	games = glob(game_dir+"*")
	f = lambda x:re.sub(game_dir, "",x)
	games = map(f,games)
	#determine which matches we haven't processed yet
	match_ids = []
	match_lines = open("plays.yml").readlines()
	match_lines = set(filter(lambda x:"match_id:" in x, match_lines))
	h = lambda x:re.sub("match_id:","", x)
	match_ids = map(int, map(h, match_lines))
	print "previously processed:", match_ids
	print games
	# for i in range(starting_match,len(games)+1):
	for g in games:
		if int(g) not in match_ids:
			command = "./read_pass_matrix.py"
			passes = game_dir+str(g)+"/passes.txt"
			shots = game_dir+str(g)+"/shots.txt"
			teams = directory+"teams.yml"
			matches = directory+"matches.yml"
			players = directory+"players.yml"
			to_execute = " ".join([command, str(g),passes, shots, teams, matches, players, "plays.yml", str(league_id)])
			print to_execute
			os.system(to_execute)
if __name__ == "__main__":
	world_cup_dir = sys.argv[1]
	league_id = int(sys.argv[2])
	main(world_cup_dir, league_id)
