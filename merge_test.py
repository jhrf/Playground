#!/usr/bin/env python

#This script checks wether all the 

import sys
import time
import pysam
import pdb
import os

def run_merge_types():
	bam_paths = sys.argv[1:]

	dum_obj 	= pysam.Samfile(sys.argv[1],"rb")
	unique  	= int(time.time())
	multi_path  = "merge_multi_%d.bam" % (unique,)
	multi_out   = pysam.Samfile(multi_path,"wb",template=dum_obj) 

	start = time.time()
	print "Starting Multi File Merge"
	for cur_path in bam_paths:
		cur_obj = pysam.Samfile(cur_path,"rb")
		for alig in cur_obj.fetch(until_eof=True):
			multi_out.write(alig)
		cur_obj.close()
	multi_out.close()

	print "Multi took %d" % (int(time.time() - start))

	single_path  = "merge_single_%d.bam" % (unique,)
	single_out = pysam.Samfile(single_path,"wb",template=dum_obj)

	start = time.time()
	single_obj = pysam.Samfile(multi_path,"rb")
	print "Starting Single File Merge"
	for alig in single_obj.fetch(until_eof=True):
		single_out.write(alig)
	print "Single took %d" % (int(time.time() - start))
	
	os.remove(multi_path)
	os.remove(single_path)

	print "Starting Samtools Cat"
	start = time.time()
	cat_path = "merge_cat_%d.bam" % (unique,)
	pysam.cat("-o",cat_path,*bam_paths)
	print "Samtools took %d" % (int(time.time() - start))

	dum_obj.close()
	os.remove(cat_path)



def run_process_bench():
	bam_path = sys.argv[1]

	start = time.time()
	native_test_obj_in = open(bam_path,"r")
	native_test_obj_out = open("native_out.bam","w")

	for line in native_test_obj_in.readlines():
		native_test_obj_out.write(line)

	native_test_obj_out.close()
	native_test_obj_in.close()
	print "Native took %d" % (int(time.time() - start),)

	start = time.time()
	pysam_test_obj_in  = pysam.Samfile(bam_path,"rb")
	pysam_test_obj_out = pysam.Samfile("pysam_out.bam","wb",template=pysam_test_obj_in)

	for read in pysam_test_obj_in.fetch(until_eof=True):
		pysam_test_obj_out.write(read)

	pysam_test_obj_in.close()
	pysam_test_obj_out.close()
	print "Pysam took %d" % (int(time.time() - start),)

def binary_merge_test(by_bytes,bam1_path,bam2_path):
	out_path = "merge_tester.bam"
	out_object = open(out_path,"w")
	bam1_object = open(bam1_path,"r")
	bam2_object = open(bam2_path,"r")
	
	out_object.write(bam1_object.read(get_header_end(bam1_path))) #write bam1 header
	bam2_object.seek(get_header_end(bam2_path)) #skip over header
	last = ""

	for block in block_gen(bam1_object,by_bytes):
		but_one = last
		last = block
		out_object.write(block)
	out_object.seek(out_object.tell() - 28)

	for block in block_gen(bam2_object,by_bytes):
		but_one = last
		last = block
		out_object.write(block)

	bam1_object.close()
	bam2_object.close()
	out_object.close()

def block_gen(obj,by_bytes):
	out = obj.read(by_bytes)
	while out:
		yield out
		out = obj.read(by_bytes)

def get_header_end(file_path):
	with open(file_path,"r") as bam_binary_object:
		slide = 50
		window = 256
		first_header_found = False
		while True:
			block = bam_binary_object.read(window)
			if '\x1f\x8b\x08\x04' in block:
				if not first_header_found:
					first_header_found = True
				else:
					loc_in_block = block.find('\x1f\x8b\x08\x04') 
					return bam_binary_object.tell() - window + loc_in_block
			bam_binary_object.seek(bam_binary_object.tell() - window + slide)

if __name__ == "__main__":
	by_bytes = int(sys.argv[1])
	bam1_path = sys.argv[2]
	bam2_path = sys.argv[3]
	binary_merge_test(by_bytes,bam1_path,bam2_path)


