#!/usr/bin/env python
import pickle
import sys,pdb
import pysam
from pprint import pprint as ppr
from merecat.src.stat import StatPack

fnm = sys.argv[1]
to_print = int(sys.argv[2])
sam = pysam.Samfile(fnm,"rb")

stat_pack = StatPack(2) 
comps = stat_pack.getComps(100)

pairs = {}

for alig in sam.fetch(until_eof=True):
	try:
		pairs[alig.qname].append({"is_rev":alig.mate_is_reverse,"is_unm":alig.is_unmapped,"seq":alig.seq})
	except KeyError:
		pairs[alig.qname] = [{"is_rev":alig.mate_is_reverse,"is_unm":alig.is_unmapped,"seq":alig.seq}]

full = {}

for i,(name,dat) in enumerate(pairs.items()):
	if not len(dat) == 2: continue 
	r1_seq = dat[0]["seq"]
	r2_seq = dat[1]["seq"]
	scores = map(lambda s: stat_pack.quickScore(comps,s),[r1_seq,r2_seq])
	is_hun = map(lambda sc: sc == 100,scores)

	if any(is_hun):
		full[name] = [((r1_seq,scores[0],dat[0]["is_unm"]),(r2_seq,scores[1],dat[1]["is_unm"]))]
	if i % 10000 == 0: print i

ppr(full.items()[:to_print])