#! /usr/bin/env python

import extargsparse
import logging
import sys
import struct

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

def string_to_ints(s):
	ri = []
	if sys.version[0] == '3':
		rb = s.encode('utf8')
		for i in range(len(rb)):
			ri.append(int(rb[i]))
	else:
		rb = bytes(s)
		for i in range(len(rb)):
			ri.append(ord(rb[i]))
	return ri


def ints_to_string(sbyte):
	if sys.version[0] == '3':
		cb = b''
		for i in range(len(sbyte)):
			cb += sbyte[i].to_bytes(1,'little')
		return cb.decode('utf8')
	else:
		cb = b''
		for i in range(len(sbyte)):
			cb += chr(sbyte[i])
		return str(cb)


def __parse_string(sbyte):
	retbyte=[]
	leftbyte=[]
	logging.info('[0]=[%s]'%(sbyte[0]))
	if sbyte[0] != ord('"'):
		raise Exception('can not accept byte [%s]'%(sbyte[0]))
	matched = False
	idx = 1
	while idx < len(sbyte):
		cbyte = sbyte[idx]
		if cbyte == ord('"'):
			matched = True
			idx += 1
			break
		if cbyte == ord('\\'):
			idx += 1
			if idx >= len(sbyte):
				break
			nbyte = sbyte[idx]
			if nbyte == ord('b'):
				retbyte.append(ord('\b'))
			elif nbyte == ord('t'):
				retbyte.append(ord('\t'))
			elif nbyte == ord('n'):
				retbyte.append(ord('\n'))
			elif nbyte == ord('r'):
				retbyte.append(ord('\r'))
			elif nbyte == ord('"'):
				retbyte.append(ord('"'))
			elif nbyte == ord('\''):
				retbyte.append(ord('\''))
			else:
				retbyte.append(nbyte)
		else:
			retbyte.append(cbyte)
		idx += 1
	if not matched :
		raise Exception('[%s] not matched string'%(ints_to_string(sbyte)))
	if idx < len(sbyte):
		leftbyte = sbyte[idx:]
	return retbyte,leftbyte

def __parse_param(sbyte):
	


def string_handler(args,parser):
	set_logging_level(args)
	for s in args.subnargs:
		sbyte = string_to_ints(s)
		cbyte,lbyte = __parse_string(sbyte)
		logging.info('cbyte [%s] lbyte [%s]'%(cbyte,lbyte))
		cs = ints_to_string(cbyte)
		ls = ints_to_string(lbyte)
		sys.stdout.write('cbyte [%s] lbyte [%s]\n'%(cs,ls))
	sys.exit(0)
	return

def param_handler(args,parser):
	set_logging_level(args)
	for s in args.subnargs:
		sbyte = string_to_ints(s)
		params, lbyte = __parse_param(sbyte)
		ls = ints_to_string(lbyte)
		sys.stdout.write('params [%s] lbyte[%s]\n'%(params,ls))

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
