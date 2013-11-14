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

#----------  preparation  --------------------

#~ export the .odf file to csv with the following settings:
#~ 	-carrakter set: western europe (ascii)
#~ 	-field delimiter= ,
#~ 	-text delimiter="
#~ 	-save cell contents as shown
#~ 	-quote all text cells

#~ ----------- TODO ---------------

 #~ no conversion for punch

#~ ----------- DONE ---------------

 #~ -flexo spd
 #~ -ita2
 #~ -header and footer
 #~ -plaintext code
 
__author__ =  'macsimski'

import argparse
import csv
import serial
import array
import sys
from time import sleep

#- use stio as display to save punch paper. ascii-art representation of the tape
def displaytape(ch):
	global i
	print '-',
	for n in range(8):
		if n==3:
			print '*',
		if ((ch>>n)&1):
			print 'O',
		else: 
			print '.',
	print '|', 
	print i
	#~ print  (ch>>2)&1
	
def punch(ch):
#	sleep(0.05)
	port.write (chr(ch))

def punchtape(h): #output function accepts dec ascii number
#	print h.encode("hex")
	if args.verbose:
		displaytape(h) # to screen
	if not args.punch:
		punch(h) # to paper # not done yet
		
	
#- lookup code and set shiftstate
def translate(pri): # can be string of length 1
	global oldcase
	global uppercase
	global i
	for i in pri:
		try:
			p = lowerdict[i]
			uppercase = False
		except KeyError:
			try:
				p= upperdict[i]
				uppercase = True
			except: 
				t=i
				if ord(i) == 10: # dicts don't like cr	
					i='cr'
					punchtape(lowerdict['@@ret'])
					break
				elif  ord(i) == 13:
					i='lf'
					punchtape(lowerdict['@@lfd'])
					break
				else:
					i='???'
					punchtape(lowerdict[' '])
					break
				i=t
		if (uppercase != oldcase):
			t=i # temp buffer for actual char
			if uppercase:
				i='Uc'
				punchtape(lowerdict['@@ucs']) #	print 'uppercase '
			else:
				i='Lc'
				punchtape(lowerdict['@@lcs']) #	print 'lowercase'
			oldcase = uppercase
			i=t # restore actual char
		punchtape(p) # p is ascii number
			
def plainpunch(pri):
	global i
	for i in pri:
		try:
			p = plaindict[i]
			for d in range(0,len(p),2):
#				print p[d:d+2]
#				punchtape()
				punchtape(int(p[d:d+2],16)>>8-bytedict[args.format])
		except: 
			print 'plain???'

def punchheader(): # punch asciiart filename at beginning
	room = '  '
	plainpunch(room)
	for b in args.input: plainpunch(b)
	plainpunch (' ')
	plainpunch('  code ')
	plainpunch(args.format)
	plainpunch('  >>|')

def punchfooter():
	room = '         '
	plainpunch(room)

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
		tx=ita2 telex
		pt=no conversion""",required=True)
	parser.add_argument('-p','--port', help='serial port',default='/dev/ttyUSB0') # change for macs and or windows
	parser.add_argument('-v','--verbose', help='y or n display on screen default n', action='store_true')
	parser.add_argument('-n','--punch', help='do not open a serial port to punch', action='store_true')
	args = parser.parse_args()

	codedict = { 'fb':'friden_spd.csv',
			'fp':'friden_pres.csv',
			'tsa':'teletypeset_a.csv',
			'tsb':'teletypeset_b.csv',
			'tx':'ita2.csv',
			'pt':'plaintext.csv' # not used yet. should produce a banner without header
			}
			
	bytedict = { 'fb':8,
			'fp':8,
			'tsa':6,
			'tsb':6,
			'tx':5,
			'pt':8
			}
	#- ---------- declaration of several vars
	global uppercase
	global oldcase

	uppercase = False
	oldcase = False
	plaintextfile="plaintext.csv"
	if not args.punch:
		try:
			port = serial.Serial(
				port=args.port, 
				baudrate=600, 
	#			timeout=1,
				parity=serial.PARITY_NONE,
				stopbits=serial.STOPBITS_ONE,
				bytesize=serial.EIGHTBITS,
				)
			print 'using: ', port.name
		except:
			print args.port, " not available, sorry"
			sys.exit(1)
	try:
		codefile = codedict[args.format]
		print' '
		print 'codebase: ',codefile
	except 'KeyError':
		print 'no known translation for that format found'
		sys.exit(1)		 
		
	#some debug feedback
	

	#read single chars from source file and parse them
	# different coded from codefile
	plaindict={}
	try:
		infile = open(plaintextfile, mode='r')
		reader = csv.reader(infile)
		for rows in reader:
			if rows[3]:
				plaindict[rows[2]]=rows[3]
		print("Input file: %s" % args.input )
	except "FileNotFoundError":
		print plaintextfile, " is not found"
	upperdict ={}
	lowerdict={}
	if not args.format=='pt':
		try:
			infile = open(codefile,mode='r')
			reader = csv.reader(infile)
			for r in reader:
				if r[3]:
					upperdict[r[4]] = int(r[0])
					lowerdict[r[3]] = int(r[0])
		except "FileNotFoundError":
				print codefile, " cannot be found. sorry"
				sys.exit(1)
	else:
		print 'no conversion'
	# ----------------- start punching ----------------
	punchheader()	# punch plaintext filename and codeformat on begin of tape
	if not args.format=='pt':
		with open(args.input) as f:
			global i
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
							i=c
							punchtape(t)
						except 'KeyError':
							translate("@@") # no escape seq. print all
							translate(c)
					else: translate("@"+ c) # print first '@' with the following 1 
				else: # normal char
						translate(c)
	else:
		with open(args.input) as f:
			global i
			for line in f:
				for i in line:
					c=i
					if i==chr(13):
						i='cr'
					elif i==chr(10):
						i='lf'
					punchtape(ord(c))	
	punchfooter()

	# convert between escapechars in the format @@xyz. if no solution is found, print all the chars
	# including @@