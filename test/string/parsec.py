#! /usr/bin/env python

import extargsparse
import logging
import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..','src'))
import strparser

def set_logging_level(args):
    loglvl= logging.ERROR
    if args.verbose >= 3:
        loglvl = logging.DEBUG
    elif args.verbose >= 2:
        loglvl = logging.INFO
    if logging.root is not None and len(logging.root.handlers) > 0:
        logging.root.handlers = []
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    return




def string_handler(args,parser):
	set_logging_level(args)
	for s in args.subnargs:
		sbyte = strparser.string_to_ints(s)
		cbyte,lbyte = strparser.parse_string(sbyte)
		logging.info('cbyte [%s] lbyte [%s]'%(cbyte,lbyte))
		cs = strparser.ints_to_string(cbyte)
		ls = strparser.ints_to_string(lbyte)
		sys.stdout.write('cbyte [%s] lbyte [%s]\n'%(cs,ls))
	sys.exit(0)	
	return

def param_handler(args,parser):
	set_logging_level(args)
	idx = 0
	for s in args.subnargs:
		sbyte = strparser.string_to_ints(s)
		startidx=0
		while startidx < len(sbyte):
			if sbyte[startidx] == ord('\x28'):				
				break
			startidx += 1
		params, lbyte = strparser.parse_param(sbyte[startidx:])
		ls = strparser.ints_to_string(lbyte)
		cs = ''
		cs += '[%s][%s]'%(idx,s)
		cs += ' params('
		i = 0
		for c in params:
			if i> 0:
				cs += ','
			cs += '%s'%(c)
			i += 1
		cs += '\x29'
		cs += 'left [%s]'%(ls)
		sys.stdout.write('%s\n'%(cs))
		idx += 1
	sys.exit(0)
	return

def unicode_handler(args,parser):
	set_logging_level(args)
	for c in args.subnargs:
		ints = strparser.string_to_uniints(c)
		cb = strparser.uniints_to_string(ints)
		sys.stdout.write('[%s] %s ret[%s]\n'%(c,ints,cb))
	sys.exit(0)
	return


def main():
	commandline='''
	{
		"verbose|v" : "+",
		"string<string_handler>##str... to parse string handler##" : {
			"$" : "+"
		},
		"param<param_handler>##str... to parse param handler##" : {
			"$" : "+"
		},
		"unicode<unicode_handler>##str... to parse unicode handler##" : {
			"$" : "+"
		}
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line(None,parser)
	raise Exception('can not parse [%s]'%(args))
	return


if __name__ == '__main__':
	main()
