#!/usr/bin/env python

#This script checks wether all the 

import sys

bp = "\n" if sys.argv[1] == "break" else " "

for i in xrange(int(sys.argv[2])):
	sys.stdout.write("123FED135" + bp)


