#!/usr/bin/env python

#This program is the first attempt at simulating the ploidy correction

import random
import sys
import pdb

def read_allocation(tel_size=50000,boundary_size=300,read_n=1,extra_chrms=0):
	
	chrm_sizes =[249240600,135524700,134946500,133841850,115109850,107289500,102521350,90294750,81195250,78017200,59118950,243189350,62965500,48119850,51244550,197962400,191044250,180905250,171055050,159128650,146304000,141153400,155260550,59363550]

	if extra_chrms > 0:
		for ext in range(extra_chrms):
			chrm_sizes.append(chrm_sizes[random.randint(0,len(chrm_sizes)-1)])

	chrm_amnt = len(chrm_sizes)
	tot_chrm = float(sum(chrm_sizes))

	read_n = read_n * 1000000000 #times 1billion
	total_telo = 0.0
	total_boundary = 0.0
	total_reads = 0.0

	for i in xrange(chrm_amnt):
		cur_size = chrm_sizes[i]

		cur_ratio = cur_size / tot_chrm 
		telo_ratio = float(tel_size) / cur_size
		cur_read_n = random.gauss(read_n * cur_ratio,1000)
		cur_boundary = random.gauss(cur_read_n * (boundary_size / cur_read_n),10)

		total_telo += (cur_read_n * telo_ratio)
		total_boundary += cur_boundary
		total_reads += cur_read_n

	print "Total Reads: %.3f" % (total_reads,)
	print "Total Telo Reads: %.3f" % (total_telo,)
	print "Total Boundary Reads: %.3f " % (total_boundary,)
	print "Ratio: %.3f " % (total_telo/total_boundary,) 

if __name__ == "__main__":
	if len(sys.argv) > 1:
		read_allocation(*map(int,sys.argv[1:]))
	else:
		read_allocation()