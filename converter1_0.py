#!/usr/bin/env python

#~ punchconverter

#~ to convert plain ascii to the punchcodes available on several 
#~ non-ascii machines using punchtape. Tape can be 5,6,7 or 8 bit, 
#~ but that translation is not done here (could be build in though)
#- call script like this:

#- $ python converter1_0.py -f fb -i textfile.txt

#- The filename is first printed as ascii-art followed by the code format
#- so the command above will translate into:
#- textfile.txt code: fb >| blabla
#- so it is clear for what machine the punchtape is


#- someinput = raw_input("input: ")

__author__ =  'macsimski'
import argparse
import csv
import serial
import array


#- use stio as display to save punch paper. ascii-art representation of the tape
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

def puchtape(h): #output
	displaytape(h)
	
	
	
#- lookup code and set shiftstate
def translate(pri):
	for i in pri:
		try:
			p = lowerdict[i]
			uppercase = False
		except KeyError:
			try:
				p= upperdict[i]
				uppercase = True
			except: 
				punchtape(' ')
				break
		if (uppercase != oldcase) & uppercase:
			punchtape(lowerdict['@@ucs'])
			oldcase = uppercase
		elif (uppercase != oldcase) & not uppercase:
			punchtape(lowerdict['@@lcs'])
			oldcase = uppercase
		else:
			punchtape(p)
	

def punchheader(): # punch asciiart filename at beginning
	room = '  '
	translate(room)
	for b in args.input: translate(b)
	translate('  code ')
	translate(args.format)
	translate('  >>|')


# ------------------ main code ----------------

# cli arguments handling

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

codedict = { 'fb':'friden_spd_lookup.csv',
		'fp':'friden_pres_lookup.csv',
		'tsa':'teletypeset_a_lookup.csv',
		'tsb':'teletypeset_b_lookup.csv',
		'tx':'ita2.csv'
		'txt':'plaintext_lookup.csv' # not used yet. should produce a banner without header
		}
		
#some filenames
plaintextfile="plaintext_lookup.csv"
try:
	codefile = codedict[args.format]
except 'KeyError':
	print 'no known translation for that format found'
	break # should be exit program gracefully
#some debug feedback

print("Input file: %s" % args.input )
print("format: %s" % args.format )

#read single chars from source file and parse them
# different coded from codefile
try:
	infile = open(plaintextfile, mode='r')
	reader = csv.reader(infile)
	plaindict = {rows[0]:rows[1].decode('hex') for rows in reader}
except "FileNotFoundError":
	print plaintextfile, " is not found"
	
try:
	infile = open(codefile,mode='r')
	reader = csv.reader(infile)
	upperdict = {row[3]:row[1] for rows in reader}
	lowerdict = {row[2]:row[1] for rows in reader}
except "FileNotFoundError":
		print codefile, " cannot be found. sorry"

global uppercase
uppercase = false
oldcase = false

# ----------------- start punching ----------------
punchheader()	
with open(args.input) as f:
	while True:
		c= f.read(1)
		if not c:
			print "EOF"
			break
		if c == '@': # escape char?
			try: c=f.read(1)
			except: 
				print "eof"
				break
				
			if c == '@': # ! second @ can be the beginning of a escape sequence
				try: c=f.read(3)
				except: 
					print "kloar"
					break
				if c == "str":
					translate('@@str')
				elif c == "swr":
					translate('@@swr')
				elif c == "pof":
					translate('@@pof')
				else: translate("@@" + c) # no escape seq. print all
			else: translate("@"+ c) # print first '@' with the following 1 
		else: # normal char
				translate(c)


# convert between escapechars in the format @@xyz. if no solution is found, print all the chars
# including @@