#!/usr/bin/env python

#Create a bam file with all the putatative telomere reads

import gzip
import time
import os
import pdb

from collections import namedtuple
import SamBam
import pysam
import subprocess32 as subprocess
import sh

SamRead = namedtuple("SamRead","name flag chrm pos mapq cigar mref mpos tlen seq qual")

def get_read_native(path,query_name,chrm,ref,pos):
	qref = chrm
	if chrm == "=":
		qref = ref
	
	with subprocess.Popen(["samtools","view",path,"%s:%d-%d" % (qref,pos,pos)],
			stdout=subprocess.PIPE,bufsize=100000) as out:
		for line in out.stdout:
			if line.split('\t')[0] == query_name:
				return (line_to_read(line))

def line_to_read(line):
	return SamRead(*line.split("\t")[:11])

def get_read_pysam(path,alig):
	master = pysam.Samfile(path,"rb")
	mate = master.mate(alig)
	master.close()
	return mate

def is_unmapped(read):
	return read.flag & 4 > 0

#Bench mark using subproces
def native_mate_benchmark(path,N=1000):
	mate_f = get_read_native
	line_f = line_to_read
	sub_start = time.time()
	out = subprocess.Popen(["samtools","view"],stdout=subprocess.PIPE,bufsize=10)
	for i,line in enumerate(out.stdout):
		sam_read = line_f(line)
		if not sam_read.mref == "*":
			mate = mate_f(path,sam_read.name,sam_read.mref,sam_read.chrm,int(sam_read.mpos))
		if N == i:
			break
	return time.time() - sub_start

def pysam_mate_benchmark(path,N=1000):
	master = pysam.Samfile(path,"rb")
	pysam_start = time.time()
	for i,alig in enumerate(master.fetch(until_eof=True)):
		if not alig.mate_is_unmapped:
			mate = get_read_pysam(path,alig)
		if N == i:
			break
	return time.time() - pysam_start

def pysam_iter_benchmark(path,N=10000):
	pysam_start = time.time()
	master = pysam.Samfile(path,"rb")
	for i,alig in enumerate(master.fetch(until_eof=True)):
		if i == N: break
		continue
	return time.time() - pysam_start

def native_iter_benchmark(path,N=10000):
	sub_start = time.time()
	line_f = line_to_read #speed alias
	out = subprocess.Popen(["samtools","view",path],stdout=subprocess.PIPE,bufsize=4096)
	for i,line in enumerate(out.stdout):
		if i == N:
			break
	out.kill()
	return time.time() - sub_start

def bam_generator(path):
	bam_it = SamBam.BamIterator(open(path,"rb"))
	for read in bam_it:
		yield read

def sam_bam_benchmark(path,N=10000):
	sb_start=time.time()
	for i,read in enumerate(bam_generator(path)):
		if i == N:
			break
	return time.time() - sb_start

N = 10000000
path = "/Users/Farmer01/dat/BAMS/SS6003059.bam"

print "pysam:"
print pysam_iter_benchmark(path,N=N)
print "Native:"
print native_iter_benchmark(path,N=N)

