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
    parser.add_argument('-f','--format', help="""fb=flexowriter SPD Bull code
fp=flexo president
tsa=typesetter 6bit version a
tsb=typesetter version b
tx=ita2 telex""",required=True)
	parser.add_argument('-p','--port', help='serial port',required=False)
args = parser.parse_args()

# filemapping
lookupfile = { fs : friden_spd_lookup.csv,
		fp : friden_pres_lookup.csv,
		tsa : typeset_a.csv,
		tsb : typeset_b.csv,
		}

#some feedback
print("Input file: %s" % args.input )
print("format: %s" % args.format )



#read single chars from source file and parse them	
with open(args.input) as f:
	while True:
		c= f.read(1)
		if not c:
			print "EOF"
			break
		
parseto = {@ : escapechar,
		1 : sqr,
					
}

# convert between escapechars in the format @@xyz. if no solution is found, print all the chars
# including @@
def escapechar():
		c=f.read(1)
		if c == '@'
			c=f.read(3)
			if c == 'str':
				c=0x19
			elif c == 'swr':
				c=0x1F
			elif c == 'lcs':
				c =0x37
			elif c == 'ucs':
				c=0x57
			elif c == 'pof':
				c=0x67
			else pushout('@')
			
		else pushout('@')
				pushout(c)
			
			