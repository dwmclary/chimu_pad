#! /usr/bin/env python
import sys

def compare_triple(x,y):
	duplicate = 0
	same = False
	for i in range(len(x)):
		if x[i] == y[i]:
			duplicate +=1
	if duplicate == len(x):
		same = True
	return same

def duplicate_triple(line, existing_lines):
	line_data = line.split(",")
	duplicate = False
	
	for element in existing_lines:
		element_data = element.split(",")
		if compare_triple(line_data[1:4], element_data[1:4]):
			duplicate = True
			break
	return duplicate

graph_lines = open(sys.argv[1]).readlines()
output_lines = []
for line in graph_lines:
	if not duplicate_triple(line, output_lines):
		output_lines.append(line.strip())
		
f = open("pruned_graph.csv", "w")
for line in output_lines:
	print >> f, line
	
f.close()

		