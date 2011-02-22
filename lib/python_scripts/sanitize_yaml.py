#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Daniel McClary on 2011-02-18.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""
import re

help_message = '''
Sanitizes YAML dumps for RoR.
'''


def sanitize_yaml(yaml_string):
	yaml_string = yaml_string.split("\n")
	yaml_buffer = []
	for y in yaml_string:
		#if this is an object start
		y = y.lstrip()
		if y.startswith("-"):
			yaml_buffer.append("\n")
			y = re.sub("-","",y)
		 	y = y.lstrip()
		else:
			y = "  "+y.lstrip()
		yaml_buffer.append(y)
	return yaml_buffer
