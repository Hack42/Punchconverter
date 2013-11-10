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
		print '|', i

def punchtape(h): #output
	displaytape(h) # to screen
#-	punch(h) # to paper # not done yet
		
	
#- lookup code and set shiftstate
def translate(pri):
	global oldcase
	global i
	for i in pri:
		try:
			p = lowerdict[i]
			uppercase = False
		except KeyError:
			print i, 'not lower'
			try:
				p= upperdict[i]
				uppercase = True
			except: 
				print 'not upper'
				punchtape(' ')
				break
		if (uppercase != oldcase) & uppercase:
			punchtape(lowerdict['@@ucs'])
			oldcase = uppercase
		elif (uppercase != oldcase) & (uppercase == False):
			punchtape(lowerdict['@@lcs'])
			oldcase = uppercase
		else:
			punchtape(p)
			
def plainpunch(pri):
	global i
	for i in pri:
		try:
			p = plaindict[i]
			punchtape(p)
		except: punchtape(' ')

def punchheader(): # punch asciiart filename at beginning
#	print plaindict.items()
#	print upperdict.items()
	room = '  '
	plainpunch(room)
	for b in args.input: plainpunch(b)
	plainpunch('  code ')
	plainpunch(args.format)
	plainpunch('  >>|')


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

codedict = { 'fb':'friden_spd.csv',
		'fp':'friden_pres.csv',
		'tsa':'teletypeset_a.csv',
		'tsb':'teletypeset_b.csv',
		'tx':'ita2_table.csv',
		'pt':'plaintext.csv' # not used yet. should produce a banner without header
		}
		
#- ---------- declaration of several vars
global uppercase
global oldcase

uppercase = False
oldcase = False
plaintextfile="plaintext.csv"


try:
	codefile = codedict[args.format]
except 'KeyError':
	print 'no known translation for that format found'
	 # should be exit program gracefully
#some debug feedback

print("Input file: %s" % args.input )
print("format: %s" % args.format )

#read single chars from source file and parse them
# different coded from codefile
plaindict={}
try:
	infile = open(plaintextfile, mode='r')
	reader = csv.reader(infile)
	for rows in reader:
		if rows[3]:
			plaindict[rows[2]]=rows[3].decode('hex')
except "FileNotFoundError":
	print plaintextfile, " is not found"
upperdict ={}
lowerdict={}
try:
	infile = open(codefile,mode='r')
	reader = csv.reader(infile)
	for r in reader:
		if r[3]:
			upperdict[r[4]] = r[2]
			lowerdict[r[3]] = r[2]
except "FileNotFoundError":
		print codefile, " cannot be found. sorry"


# ----------------- start punching ----------------
punchheader()	# punch plaintext filename and codeformat on begin of tape
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
					print "kloar" # ----- needs real code ---------
					break
				try:
					t= lowerdict['@@' + c ] # lookup @@xyz as one thing
					punchtape(t)
				except 'KeyError':
					translate("@@") # no escape seq. print all
					translate(c)
			else: translate("@"+ c) # print first '@' with the following 1 
		else: # normal char
				translate(c)


# convert between escapechars in the format @@xyz. if no solution is found, print all the chars
# including @@