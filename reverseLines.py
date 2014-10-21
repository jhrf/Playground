#!/usr/bin/env python

#This script reads in a file and inverts it 

import sys,os

#http://stackoverflow.com/questions/2301789/read-a-file-in-reverse-order-using-python
def reverse_readline(filename, buf_size=8192):
    """a generator that returns the lines of a file in reverse order"""
    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        total_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(total_size, offset + buf_size)
            fh.seek(-offset, os.SEEK_END)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # the first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                lines[-1] += segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                yield lines[index]
        yield segment

filename = sys.argv[1]
outname = sys.argv[2]

with open(outname,"w") as out_file:
	for segment in reverse_readline(filename):
		out_file.write(segment+'\n')

print "Done"