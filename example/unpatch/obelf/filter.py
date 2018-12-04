#! /usr/bin/env python

import extargsparse
import sys
import os
import logging
import random
import re
import time


def set_logging_level(args):
    loglvl= logging.ERROR
    if args.verbose >= 3:
        loglvl = logging.DEBUG
    elif args.verbose >= 2:
        loglvl = logging.INFO
    if logging.root is not None and len(logging.root.handlers) > 0:
        logging.root.handlers = []
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    random.seed(time.time())
    return

def read_file(infile=None):
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')
    rets = ''
    for l in fin:
        s = l
        if 'b' in fin.mode:
            if sys.version[0] == '3':
                s = l.decode('utf-8')
        rets += s

    if fin != sys.stdin:
        fin.close()
    fin = None
    return rets


def write_file_direct(s,fout):
    outs = s
    if 'b' in fout.mode:
        outs = s.encode('utf-8')
    fout.write(outs)
    return


def write_file(s,outfile=None):
    fout = sys.stdout
    if outfile is not None:
        fout = open(outfile, 'w+b')
    write_file_direct(s,fout)
    if fout != sys.stdout:
        fout.close()
    fout = None
    return 



def filter_handler(args,parser):
	set_logging_level(args)
	started = 0
	startexpr = re.compile('^format\s+')
	matchexpr = re.compile('^0x0')
	outs = ''
	ins = read_file(args.input)
	sarr = re.split('\n', ins)
	for l in sarr:
		l = l.rstrip('\r\n')
		if started == 0:
			if startexpr.match(l):
				outs += '%s\n'%(l)
				started = 1
		else:
			if matchexpr.match(l):
				outs += '%s\n'%(l)
			else:
				outs += '\n'
				started = 0
	write_file(outs,args.output)
	sys.exit(0)
	return

def filterfunc_handler(args,parser):
	set_logging_level(args)
	started = 0
	startexpr = re.compile('^format\s+')
	matchexpr = re.compile('^0x0')
	funcexpr = re.compile('.*\[%s\].*'%(args.subnargs[0]))
	outs = ''
	ins = read_file(args.input)
	sarr = re.split('\n', ins)
	for l in sarr:
		l = l.rstrip('\r\n')
		if started == 0:
			if startexpr.match(l) and \
				funcexpr.matchexpr(l):
				started = 1
				outs += '%s\n'%(l)
		else:
			if matchexpr.match(l):
				outs += '%s\n'%(l)
			else:
				outs += '\n'
				started = 0
	write_file(outs, args.output)
	sys.exit(0)
	return


def filterset_handler(args,parser):
	set_logging_level(args)
	filterpos = []
	filterexpr = dict()
	exprkeys = []
	curkeys = []
	for a in args.subnargs:
		try:
			if a.startswith('x') or a.startswith('X'):
				iv = int(a[1:],16)
			elif a.startswith('0x') or a.startswith('0X'):
				iv = int(a[2:],16)
			else:
				iv = int(a)
			if iv not in filterpos:
				filterpos.append(iv)
				# to get the 
				filteriv = iv >> 4 
				filteriv = filteriv << 4
				pos = '^0x%08x'%(filteriv)
				exprkeys.append(pos)
				if pos not in curkeys:
					logging.info('compile [%s]'%(pos))
					filterexpr[pos] = re.compile(pos)
					curkeys.append(pos)
		except:
			pass
	ins = read_file(args.input)
	sarr = re.split('\n', ins)
	lineno = 0
	expri = 0
	outs = ''
	for l in sarr:
		lineno += 1
		l = l.rstrip('\r\n')
		curprint = False
		for k in curkeys:
			if curprint:
				break
			if filterexpr[k].match(l):
				expri = 0
				for ck in exprkeys:
					if ck == k:						
						modval = filterpos[expri] % 16
						
						# now to give the modval
						sarr = re.split(':',l) 
						if len(sarr) > 1 :
							logging.info('[%s] [0x%x]modval  [%s] val [%s]'%(k, filterpos[expri],modval,sarr[1]))
							sarr[1] = sarr[1].strip(' \t')
							sarr[1] = sarr[1].rstrip(' \t')
							sarr = re.split('\s+',sarr[1])
							if len(sarr[modval]) > 5:
								curprint = True
								break
					expri += 1
		if curprint:
			outs += '[%d].[%s]\n'%(lineno, l)
	write_file(outs,args.output)
	sys.exit(0)
	return


def main():
	commandline='''
	{
		"verbose|v" : "+",
		"input|i" : null,
		"output|o" : null,
		"filter<filter_handler>" : {
			"$" : 0
		},
		"filterfunc<filterfunc_handler>" : {
			"$" : 1
		},
		"filterset<filterset_handler>" : {
			"$" : "+"
		}
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line(None,parser)
	raise Exception('can not accept [%s]'%(args))

if __name__ == '__main__':
	main()