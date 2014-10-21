#!/usr/bin/env python

#This program tests how quickly numpy loads and saves files]
# Example invocation:
#	./numpyLoadTester.py -x 3 -y 1080000 -n test1

import numpy as np, random, argparse, pdb,time

def createNp():
	arr = np.zeros(shape=(cmd_args.y,cmd_args.x),dtype=float)
	print "Starting"

	st_tm = time.time()
	for i in xrange(cmd_args.y):
		arr[i,:] = [random.randint(0,1000) for x in xrange(cmd_args.x)]
	print "Generating Table took {0}".format(time.time() -st_tm)

	csv_st_tm = time.time()
	np.savetxt("CSV" + cmd_args.n, arr, delimiter=",")
	print "Saving CSV took {0}".format(time.time() - csv_st_tm)
	np_st_tm = time.time()
	np.save("NP" + cmd_args.n, arr)
	print "Saving NP took {0}".format(time.time() - np_st_tm)

	del(arr)

	csv_st_tm = time.time()
	arr_csv = np.loadtxt("CSV" + cmd_args.n, delimiter=",")
	print "Loading CSV took {0}".format(time.time() - csv_st_tm)
	np_st_tm = time.time()
	arr_np = np.load("NP" + cmd_args.n + ".npy")
	print "Loading NP took {0}".format(time.time() - np_st_tm)

parser = argparse.ArgumentParser()
parser.add_argument('-x',type=int,nargs="?",default=4,help="x (across) dimension for numpy array")
parser.add_argument('-y',type=int,nargs="?",default=1000,help='y (down) dimension for numpy array')
parser.add_argument('-n',type=str,nargs="?",default="NPfile",help='File name for numpy')

cmd_args = parser.parse_args()

if __name__ == "__main__":
	createNp()