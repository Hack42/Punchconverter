#!/usr/bin/env python

__author__ =  'macsimski'
import argparse
import csv
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='just copy usefull rows.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i','--input', help='csv input filename',required=True)
    parser.add_argument('-b','--bitlength', help='code bitlength in odf',required=True)
args = parser.parse_args()
(name,ext)=os.path.splitext(args.input)
with open(args.input,"rb") as source:
    rdr= csv.reader( char.replace('\0','') for char in source )
    with open(name +"_lookup.csv","wb") as result:
        wtr= csv.writer( result )
        for r in rdr:
		if r[3]:
			wtr.writerow( (r[1], r[2], r[3], r[4) )
