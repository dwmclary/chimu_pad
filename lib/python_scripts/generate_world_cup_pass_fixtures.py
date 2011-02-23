#! /usr/bin/env python

from glob import glob
import os, sys
import re

games_extension = "games/"
starting_match = 2

def main(directory):
	game_dir = directory+games_extension
	games = glob(game_dir+"*")
	f = lambda x:re.sub(game_dir, "",x)
	games = map(f,games)
	#determine which matches we haven't processed yet
	match_ids = []
	match_lines = open("plays.yml").readlines()
	match_lines = set(filter(lambda x:"match_id:" in x, match_lines))
	g = lambda x:re.sub("match_id:","", x)
	match_ids = map(int, map(g, match_lines))
	print "previously processed:", match_ids
	for i in range(starting_match,len(games)+1):
		if i not in match_ids:
			command = "./read_pass_matrix.py"
			passes = game_dir+str(i)+"/passes.txt"
			shots = game_dir+str(i)+"/shots.txt"
			teams = directory+"teams.yml"
			matches = directory+"matches.yml"
			players = directory+"players.yml"
			to_execute = " ".join([command, str(i),passes, shots, teams, matches, players, "plays.yml"])
			print to_execute
			os.system(to_execute)
if __name__ == "__main__":
	world_cup_dir = sys.argv[1]
	main(world_cup_dir)
