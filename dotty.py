#!/usr/bin/env python
#Once upon a time...

# Count the reads from a bamfile quickly.
#
# This software is free to use and distribute.
# If you like it and would like to use a part,
# perhaps provide a link back to my github
# www.github.com/jhrf
# That would be nice of you. Thanks.

import pysam
import pdb
import sys
import os
import argparse
import numpy as np


from multiprocessing import Queue,Process
import Queue as Queue2
import time, datetime

def network_to_dot(network,outname):
	dot = open(outname,"w")
	dot.write("digraph SubtelomereGraph {\n")
	for x in xrange(network.shape[0]):
		for y in xrange(network.shape[1]):
			if network[y,x] == 1:
				dot.write( "%d -> %d;\n" % (x,y,) )
		if x % 2000 == 0: print "x:%d" % (x,)
	dot.write("}\n")
	dot.close()

if __name__ == "__main__":
	
	#  COMMAND LINE HANDLING: IN THE EVENT THIS PROGRAM 
	#  IS RUN FROM THE CMD LINE INSTALISE THE FOLLOWING
	#  PARAMETERS AND INSTALISE THE CLASSES AS FOLLOWS

	network = np.loadtxt(sys.argv[1],delimiter=",")
	network_to_dot(network,"lolapaloza.dot")

#....happily ever after.