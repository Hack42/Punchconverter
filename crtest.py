#!/usr/bin/env python

import csv

upperdict ={}
lowerdict={}
try:
	infile = open("crtest.csv",mode='r')
	reader = csv.reader(infile)
	for r in reader:
		if r[3]:
			upperdict[r[4]] = chr(int(r[0]))
			lowerdict[r[3]] = hex(int(r[0]))
except "FileNotFoundError":
		print "codefile cannot be found. sorry"
		
print chr(lowerdict['8'])