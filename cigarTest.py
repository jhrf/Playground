#!/usr/bin/env python

#This program tests how quickly numpy loads and saves files
#	Example innvocation:
#		./numpyLoadTester.py -x 3 -y 1080000 -n test1

import pickle
import time
from collections import namedtuple
from pprint import pprint as ppr
import sh
import pdb
import numpy as np

def master():

	with open("./cigarlist.pkl","r") as cigarlist:
		cigarDat = pickle.load(cigarlist)

	cigarDat.extend(cigarDat)
	print "Dat Length = %d" % (len(cigarDat))
	
	res = {}
	funcs = [method_1,method_2,method_3,method_4]
	tries = 10
	
	for fu in funcs:
		tot = 0
		print "Starting: %s" % (fu.__name__,)
		for x in xrange(tries):
			tot += loader(method_1,cigarDat)
		res[fu.__name__] = float(tot) / tries

	print "FINISHED. RESULTS:"
	ppr(res)

def loader(func,dat):
	Profile = namedtuple("Profile","has4 dub4 score")
	start = time.time()
	for cig in dat:
		func(cig,Profile)
	end = time.time()

	return end - start

def method_1(cigar,Profile):
		
		has4 = False
		dub4 = False
		score = 0

		if cigar == [(0,100)]:
			return Profile(has4,dub4,100)
		else:
			for typ,cou in cigar:
				if typ == 4 and has4:
					dub4 = True
				elif typ == 4:
					has4 = True
				elif typ == 0:
					score += cou
			return Profile(has4,dub4,score)

def method_2(cigar,Profile):
		has4 = False
		dub4 = False
		score = 0

		for typ,cou in cigar:
			if typ == 4 and has4:
				dub4 = True
			elif typ == 4:
				has4 = True
			elif typ == 0:
				score += cou
		return Profile(has4,dub4,score)

def method_3(cigar,Profile):

	amount_of_4 = len(filter(lambda (typ,cout): typ == 4,cigar))
	score = sum(filter(None,map(lambda (typ,cout): cout if typ == 0 else None,cigar)))

	return Profile(has4=amount_of_4 > 0,dub4=amount_of_4 > 1,score=score)

def method_4(cigar,Profile):
	has4 = False
	dub4 = False
	score = 0

	for typ,cou in iter(cigar):
		if typ == 4 and has4:
				dub4 = True
		elif typ == 4:
			has4 = True
		elif typ == 0:
			score += cou

	return Profile(has4= has4,dub4=dub4,score=score)

master()


