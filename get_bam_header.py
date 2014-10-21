#!/usr/bin/env python

import sys


def get_header_end(file_path):
	with open(file_path,"r") as bam_binary_object:
		slide = 5
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
	print get_header_end(sys.argv[1])


