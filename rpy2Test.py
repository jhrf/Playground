#!/usr/bin/env python
import math, datetime,time,pdb
import rpy2.robjects.lib.ggplot2 as ggplot2
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import pickle,sys

def getRelDat(patDat,pat):
	for k in list(patDat):
		if k == pat:
			pass

datasets = importr('datasets')
stats = importr('stats')
grdevices = importr('grDevices')
mtcars = datasets.__rdata__.fetch('mtcars')['mtcars']

patDat = pickle.load(open(sys.argv[1],"rb"))
relDat = getRelDat(patDat,sys.argv[2])

gp = ggplot2.ggplot(patDat)

pp = gp + \
     ggplot2.aes_string(x='wt', y='mpg') + \
     ggplot2.geom_point()

ro.r.pdf("~/Pictures/lolgasm.pdf")

pp.plot()

grdevices.dev_off()

raw_input("Please type enter...")
