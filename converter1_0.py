#!/usr/bin/env python

__author__ =  'macsimski'
import argparse
import csv
import serial

class Writer():
    def __init__(name, table):
        self._name = name
        self._table = 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Universal punchcode translator.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i','--input', help='text input filename',required=True)
    parser.add_argument('-f','--format', help="""fb=flexowriter Bull
fp=flexo president
tsa=typesetter 6bit version a
tsb=typesetter version b
tx=ita2 telex""",required=True)
    args = parser.parse_args()
    
    print("Input file: %s" % args.input )
    print("format: %s" % args.format )


    # setup serial port
    port = serial.Serial(0) # open serial port
    port.baudrate = 1200
    print port.name
    
    with open(args.input) as f:
	    while True:
		    c= f.read(1)
		    if not c:
			    print "EOF"
			    break
		
