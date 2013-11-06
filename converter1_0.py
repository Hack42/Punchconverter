#!/usr/bin/env python

# someinput = raw_input("input: ")

__author__ =  'macsimski'
import argparse
import csv
import serial

class Writer():
    def __init__(name, table):
        self._name = name
        self._table = table 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Universal punchcode translator.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i','--input', help='text input filename',required=True)
    parser.add_argument('-f','--format', help="""fb=flexowriter Bull 
	fp=flexo president
	tsa=typesetter 6bit version a
	tsb=typesetter version b
	tx=ita2 telex""",required=True)
    parser.add_argument('-p','--port', help='serial port',required=False)
args = parser.parse_args()

#some filenames
plaintextfile="plaintext_lookup.csv"


#some feedback

print("Input file: %s" % args.input )
print("format: %s" % args.format )

def pushout(ch):
	displaytape(ch)

		
def displaytape(ch):
	for b in ch:
		print '|',
		for n in range(8):
			if n==3:
				print '*',
			if ord(b)&(1<<n):
				print 'O',
			else: print '.',
		print '|', b

def translate(pri):
	displaytape(int(chr(plaindict[pri])))
	
def escapechar(e):
	d="-"
	if e == '@':
#		print "one"
		try: e=f.read(1)
		except: 
			print "eof"
			return
			
		if e == '@':
#			print "two"
			try: d=f.read(3)
			except: 
				print "eof"
#			print d
			e="-"
			if d == "str":
				e=0x19
			elif d == "swr":
				e='xx'
				print e, "dus"
			elif d == "lcs":
				e =0x37
			elif d == "ucs":
				e=0x57
			elif d == "pof":
				e=0x67
			else: return("1@")
			return ("p")
		else: return("2@")
	else: 
			return(e)

# setup serial port to puncher (ours works on 1200BAUD max)
# port = serial.Serial(args.port) # open serial port
# port.baudrate = 1200
# print port.name
    
#read single chars from source file and parse them	
with open(plaintextfile, mode='r') as infile:
	reader = csv.reader(infile)
	plaindict = {rows[1]:rows[2] for rows in reader}
	
with open(args.input) as f:
	while True:
		c= f.read(1)
		if not c:
			print "EOF"
			break
		d="-"
		if c == '@':
			try: c=f.read(1)
			except: 
				print "eof"
				break
				
			if c == '@':
				try: c=f.read(3)
				except: 
					print "eof"
				e="-"
				if c == "str":
					translate('\x19')
				elif c == "swr":
					translate('\x78\xa0\xa0\x78\x00')
				elif c == "lcs":
					translate('\x37')
				elif c == "ucs":
					translate('\x57')
				elif c == "pof":
					translate('\x67')
				else: print "1@"
			else: translate("@"+ c)
		else: 
				translate(c)
#		escapechar(c)
#		displaytape(c)



# convert between escapechars in the format @@xyz. if no solution is found, print all the chars
# including @@
			
			
