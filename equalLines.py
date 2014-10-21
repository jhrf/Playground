#!/usr/bin/env python

#This script checks wether all the 

import sys

def remove_newline(line):
	return line.strip()

def write_and_give(line,desired):
	line = remove_newline(line)
	if len(line) >= desired:
		sys.stdout.write(line[:desired]+"\n")
		return write_and_give(line[desired:],desired)
	else:
		return line

desired = int(sys.argv[1])
prev_line = ""

for line in sys.stdin:
	if ">" in line:
		prev_line = remove_newline(prev_line)
		if prev_line: sys.stdout.write(prev_line+"\n")
		sys.stdout.write(line)
	else:
		prev_line = write_and_give(prev_line+line,desired)