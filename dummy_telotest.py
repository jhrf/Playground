#!/usr/bin/env python
import curses
import time
import sys

def ptrnCount(seq,ptrn):
	return seq.count(ptrn)

def hasPtrn(seq,ptrn):
	if ptrn in seq: return True
	else: return False

def hasPtrn_N(seq,ptrn,N):
	if ptrn in seq:
		return seq.count(ptrn) >= N
	return False

def telomeric(seq):
	telPats  = ["TTAGGGTTAGGG","CCCTAACCCTAA"]
	thresh = 1
	res = map(lambda p : hasPtrn_N(seq,p,thresh), telPats)
	return True in res

def dummyProc(seq,mateseq,paired,mate_unmapped):
	if telomeric(seq):
		#Write telomeric read to file
		print "Written to telbam (telomere)"

		if paired and not mate_unmapped:
			if not telomeric(mateseq):  #Only add if nontelomeric
				print "Written to telbam (assoc)"

dummyProc(seq="TAGGGTTAGGGTTAGGGCTAGGGTTAGGGGTAGGGTTAGGGTTACGGTTAGGGTTAGGGTTAGGGTTAGGGTTAGGGTTAGGGTTAGGGTTAGGGTTAGG",
		  mateseq="ACAACCCTAAACATAAAAATAACCCTAAGCCTACCCCTATCCCCACCCATACTCCTAACATTAACCCGACCCCTATCCCTAAACCGCAATCTCACACGCT",
		  paired = True,
		  mate_unmapped= False)

dummyProc(seq="ACAACCCTAAACATAAAAATAACCCTAAGCCTACCCCTATCCCCACCCATACTCCTAACATTAACCCGACCCCTATCCCTAAACCGCAATCTCACACGCT",
		  mateseq="TAGGGTTAGGGTTAGGGCTAGGGTTAGGGGTAGGGTTAGGGTTACGGTTAGGGTTAGGGTTAGGGTTAGGGTTAGGGTTAGGGTTAGGGTTAGGGTTAGG",
		  paired = True,
		  mate_unmapped=True)