#!/usr/bin/env python

#This program tests how quickly python accesses dict values
#on increasing sizes of dicts.

import numpy as np, random, argparse, pdb,time, string

def testDictLookup(sz,by,lo):

	for n in xrange(lo,sz,by):
		print "Creating dict of size {0}...".format(n)
		testDict = {}
		create_t = time.time()
		for i in xrange(1,n+1): #Generate a random string and put it in the dict
			testDict[i] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
		
		print "The dict took {0}secs\n\n".format(round(time.time() - create_t,2))

		print "Testing the lookup time for an index in the beginning of the range:"
		loLook_t = time.time()
		lo = testDict[n]
		print "That took {0}secs\n\n".format(round(time.time() - loLook_t,2))

		print "Testing the lookup time for an index in the middle of the range:"
		midLook_t = time.time()
		mid = testDict[(n/2)+1]
		print "That took {0}secs\n\n".format(round(time.time() - midLook_t,2))

		print "Testing the lookup time for an index in the end of the range:"
		hiLook_t = time.time()
		hi = testDict[n-1]
		print "That took {0}secs\n\n".format(round(time.time() - hiLook_t,2))

		print "Test finished!"







parser = argparse.ArgumentParser()
parser.add_argument('-m',type=int,nargs="?",default=100000,help="The maximum size you wish to test")
parser.add_argument('-l',type=int,nargs="?",default=100000,help="The minimum size you wish to test")
parser.add_argument('-b',type=int,nargs="?",default=1000,help="The interval by which sizes are tested")

cmd_args = parser.parse_args()

if __name__ == "__main__":
	testDictLookup(cmd_args.m,cmd_args.b,cmd_args.l)