#!/usr/bin/env python
import colorsys
import pdb

def get_N_HexCol(N=5):

	HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in xrange(N)]
	hex_out = []
	for rgb in HSV_tuples:
		rgb = map(lambda x: int(x*255),colorsys.hsv_to_rgb(*rgb))
		hex_out.append("".join(map(lambda x: chr(x).encode('hex'),rgb)))
	return hex_out

print get_N_HexCol()
print get_N_HexCol_old()