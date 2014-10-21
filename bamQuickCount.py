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
import operator
from multiprocessing import Queue,Process
import Queue as Queue2
import time, datetime

class ChrmCount(object):

	def __init__(self,masterName,fetchRef,verbose=False):
		self._masterName = masterName
		self._fetchRef = fetchRef
		self._verbose = verbose

	# Scans the master bam against a list of ordered `deadcerts` to find
	# non telomeric associations amongst the reads. If fetchRef is none
	# it will search all chrms, otherwise just the one specified by fetchRef
	# Returns:
	# ~ Path to a bamfile of mate pair associated reads
	def runQuickCount(self):
		master = pysam.Samfile(self._masterName,"rb")
		stTime = time.time()
		total = 0
		for alig in master.fetch(self._fetchRef,until_eof=True):
			total += 1
		master.close()
		return total

class CountParallel():

	def __init__(self,masterName,procN,verbose=False):
		self._masterName = masterName
		self._procN = procN
		self._verbose = verbose

		self._outQu = Queue()
		
	# Concurrently submits second pass processes. Given a list of "deadcerts"
	# (reads which are associated to telomeric reads by mate piar) creates
	# a bam file for each reference.
	# Returns:
	# ~ A list of bam file paths containing non-telomeric associated reads. 
	def runQuickCountPar(self,stTime=None):

		master = pysam.Samfile(self._masterName,"rb")
		references = master.references
		master.close()

		refGen = self.__chrmGenerator__(references)

		currentRef = {}
		procs = []
		completed = 0
		iterations = 0
		total = 0

		while len(references) != completed:

			#For the differences between procN and current processes
			#get an entry from refGen while it still has refs to give
			for i,chrm in zip(range(self._procN - len(procs)),refGen):
				if self._verbose: print "[Status] %s submitted for processing" % (chrm,)
				p = Process(
					target=self.__qckCntProcess__,
					args=(chrm,self._verbose))
				
				procs.append(p)
				p.start() #Create process and send to queue
				currentRef[chrm] = time.time()

			for i in range(len(procs)):
				iterations += 1
				try:
					res = self._outQu.get(block=True,timeout=2)
					tTaken = currentRef[res[0]]
					del currentRef[res[0]]
					completed += 1
					total += res[1]
					if self._verbose: print "[Status] %s finished and found %d reads in %d secs"  \
												% (res[0],res[1],secSince(tTaken))
				except Queue2.Empty:
					# No results have come back yet so 
					# we just carry on in the loop
					pass

			if iterations % 10 == 0 and stTime != None:
					print "[Status] Time so far: %d secs | Completed: %d/%d"\
							" | Waiting for %d processes to finish: " \
							% (secSince(stTime),completed,len(references),len(currentRef))

					sys.stdout.write("\t| ")
					for pr in currentRef.keys():
						sys.stdout.write("%s : %d secs | " % (pr,secSince(currentRef[pr])))
					sys.stdout.write("\n")
						
			for p in procs:
				if not p.is_alive():
					#p.join()
					procs.remove(p)

		return total

	# A process which when runs the second pass on a
	# given chrm (fetchRef) in parralell. 
	# Returns: 
	# ~ Path to created bam, 
	# ~ The chrm it was working on
	# ~ The amount of assocd reads found
	def __qckCntProcess__(self,fetchRef,verbose):
		
		counter = ChrmCount(masterName=self._masterName,
						fetchRef=fetchRef,
						verbose=verbose)
		
		total = counter.runQuickCount()

		self._outQu.put((fetchRef,total))

	#A generator which spits out references (chrm) belonging to a bam
	def __chrmGenerator__(self,references):
		for re in references: yield re

def run(bamNames,procN,verbose):

	for b in bamNames:

		stTime = time.time()

		if verbose: 
			print "[Status] Starting quickCount process for %s" % (b,)

		#Do the second pass
		qcHandler = CountParallel(masterName=b,
								procN = procN,
								verbose=verbose)
	
		total = qcHandler.runQuickCountPar(stTime)

		if verbose: 
			print "[Status] Quickcount completed in %d secs" % (secSince(stTime),) 

		if verbose:
			sys.stdout.write("=== Total reads in file ===\n\t")
		print "%d" % (total,)

def secSince(srt):
	return int(time.time() - srt)

if __name__ == "__main__":
	
	#  COMMAND LINE HANDLING: IN THE EVENT THIS PROGRAM 
	#  IS RUN FROM THE CMD LINE INSTALISE THE FOLLOWING
	#  PARAMETERS AND INSTALISE THE CLASSES AS FOLLOWS

	parser = argparse.ArgumentParser()
	parser.add_argument('bams',metavar='BAMS', nargs='+',
		help='The file(s) whose telomeric reads we wish to extract')
	parser.add_argument('-v',action="store_true",default=False
		,help='If set the program will output more information to terminal')
	parser.add_argument('-p',type=int,nargs='?',default=3
		,help="The amount of processors you wish the program to use.")

	cmd_args = parser.parse_args()

	print "Welcome to bamQuickCount. Start Time: " \
		+ datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

	run(cmd_args.bams,cmd_args.p,cmd_args.v)

	print "bamQuickCount has finished. End Time: " \
			+ datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

#....happily ever after.