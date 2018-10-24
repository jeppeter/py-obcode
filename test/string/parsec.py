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

def __parse_string(sbyte):
	retbyte=[]
	leftbyte=[]
	logging.info('[0]=[%s]'%(sbyte[0]))
	if sbyte[0] != ord('"'):
		raise Exception('can not accept byte [%s]'%(sbyte[0]))
	idx = 1
	while idx < len(sbyte):
		cbyte = sbyte[idx]
		if cbyte == ord('"'):
			idx += 1
			if idx < len(sbyte):
				leftbyte = sbyte[idx:]
			return retbyte, leftbyte
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
	raise Exception('[%s] not matched string'%(ints_to_string(sbyte)))
	return retbyte,leftbyte

def __parse_raw_string(sbyte):
	retbyte=[]
	leftbyte=[]
	if sbyte[0] != ord('"'):
		raise Exception('can not accept byte [%s]'%(ints_to_string(sbyte)))
	idx = 1
	while idx < len(sbyte):
		cbyte = sbyte[idx]
		if cbyte == ord('"'):
			idx += 1
			if idx < len(sbyte):
				leftbyte = sbyte[idx:]
			return retbyte, leftbyte
		if cbyte == ord('\\'):
			idx += 1
			if idx >= len(sbyte):
				break
			nbyte = sbyte[idx]
			retbyte.append(cbyte)
			retbyte.append(nbyte)
		else:
			retbyte.append(cbyte)
		idx += 1
	raise Exception('[%s] not matched string'%(ints_to_string(sbyte)))
	return retbyte,leftbyte

def __parse_single_quote(sbyte):
	return

def __parse_raw_single_quote(sbyte):
	return

def __is_common_char(c):
	if c >= ord('a') and c <= ord('z'):
		return True
	if c >= ord('A') and c <= ord('Z'):
		return True
	if c >= ord('0') and c <= ord('9') :
		return True
	if c == ord('_'):
		return True
	if c == ord('-') or c == ord('*') or c == ord('/') or \
		c == ord('+'):
		return True
	if c == ord('<') or c == ord('>') or c == ord('='):
		return True
	if c == ord('?') or c == ord(':') or c == ord(';'):
		return True
	return False

def __is_space_char(c):
	if c == ord(' ') or c == ord('\t'):
		return True
	return False

def __parse_lbrace(sbyte):
	rbyte = []
	if sbyte[0] != ord('('):
		raise Exception('[%s] not startwith [(]'%(ints_to_string(sbyte)))
	idx = 1
	rbyte = []
	while idx < len(sbyte):
		cbyte = sbyte[idx]
		if cbyte == ord(')'):
			idx += 1
			lbyte = []
			if idx < len(sbyte):
				lbyte = sbyte[idx:]
			return rbyte,lbyte
		elif cbyte == ord('('):
			crbyte , lbyte= __parse_lbrace(sbyte[idx:])
			rbyte.append(ord('('))
			rbyte.extend(crbyte)
			rbyte.append(ord(')'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('{'):
			crbyte, lbyte = __parse_bracket(sbyte[idx:])
			rbyte.append(ord('{'))
			rbyte.extend(crbyte)
			rbyte.append(ord('}'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('"'):
			crbyte, lbyte = __parse_raw_string(sbyte[idx:])
			rbyte.append(ord('"'))
			rbyte.extend(crbyte)
			rbyte.append(ord('"'))
		elif (idx + 1) < len(sbyte):
			nbyte = sbyte[(idx + 1)]
			if cbyte == ord('/') and nbyte == ord('/'):
				raise Exception('[%s]can not accept for the // comment'%(ints_to_string(sbyte)))
			elif cbyte == ord('/') and nbyte == ord('*'):
				crbyte, lbyte = __parse_comment(sbyte[idx:])
				idx = (len(sbyte) - len(lbyte))
			elif __is_common_char(cbyte):
				rbyte.append(cbyte)
				idx += 1
			else:
				raise Exception('[%s] not accept [%d]'%(ints_to_string(sbyte), idx))
		elif __is_common_char(cbyte):
			rbyte.append(cbyte)
			idx += 1
		elif __is_space_char(cbyte):
			idx += 1
		else:
			raise Exception('[%s] not accept [%d]'%(ints_to_string(sbyte),idx))
	raise Exception('[%s] not paired '%(ints_to_string(sbyte)))
	return rbyte,[]


def __parse_bracket(sbyte):
	rbyte = []
	if sbyte[0] != ord('('):
		raise Exception('[%s] not startwith [(]'%(ints_to_string(sbyte)))
	idx = 1
	rbyte = []
	while idx < len(sbyte):
		cbyte = sbyte[idx]
		if cbyte == ord('}'):
			idx += 1
			lbyte = []
			if idx < len(sbyte):
				lbyte = sbyte[idx:]
			return rbyte,lbyte
		elif cbyte == ord('('):
			crbyte , lbyte= __parse_lbrace(sbyte[idx:])
			rbyte.append(ord('('))
			rbyte.extend(crbyte)
			rbyte.append(ord(')'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('{'):
			crbyte, lbyte = __parse_bracket(sbyte[idx:])
			rbyte.append(ord('{'))
			rbyte.extend(crbyte)
			rbyte.append(ord('}'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('"'):
			crbyte, lbyte = __parse_raw_string(sbyte[idx:])
			rbyte.append(ord('"'))
			rbyte.extend(crbyte)
			rbyte.append(ord('"'))
		elif (idx + 1) < len(sbyte):
			nbyte = sbyte[(idx + 1)]
			if cbyte == ord('/') and nbyte == ord('/'):
				raise Exception('[%s]can not accept for the // comment'%(ints_to_string(sbyte)))
			elif cbyte == ord('/') and nbyte == ord('*'):
				crbyte, lbyte = __parse_comment(sbyte[idx:])
				idx = (len(sbyte) - len(lbyte))
			elif __is_common_char(cbyte):
				rbyte.append(cbyte)
				idx += 1
			else:
				raise Exception('[%s] not accept [%d]'%(ints_to_string(sbyte), idx))
		elif __is_common_char(cbyte):
			rbyte.append(cbyte)
			idx += 1
		elif __is_space_char(cbyte):
			idx += 1
		else:
			raise Exception('[%s] not accept [%d]'%(ints_to_string(sbyte),idx))
	raise Exception('[%s] not paired '%(ints_to_string(sbyte)))
	return rbyte,[]


def __parse_param(sbyte):
	idx = 0
	lbyte = sbyte
	if sbyte[0] != ord('('):
		raise Exception('param [%s] not [(] started '%(ints_to_string(sbyte)))
	params = []
	idx = 1
	curparam = []
	curname = []
	while idx < len(sbyte):
		cbyte = sbyte[idx]
		if cbyte == ord('('):
			rbyte, lbyte = __parse_lbrace(sbyte[idx:])
			curname.append(ord('('))
			curname.extend(rbyte)
			curname.append(ord(')'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('{'):
			rbyte, lbyte = __parse_bracke(sbyte[idx:])
			curname.append(ord('{'))
			curname.extend(rbyte)
			curname.append(ord('}'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord(')'):
			if len(curname) > 0:
				params.append(ints_to_string(curname))
				curname = []
			idx += 1
			lbytes = []
			if idx < len(sbyte):
				lbytes = sbyte[idx:]
			return params,lbytes
		elif cbyte == ord('"'):
			rbyte, lbyte = __parse_string(sbyte[idx:])
			curname.append(ord('"'))
			curname.extend(rbyte)
			curname.append(ord('"'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord(','):
			if len(curname) == 0:
				raise Exception('[%s] has empty param'%(ints_to_string(sbyte)))
			params.append(ints_to_string(curname))
			curname = []
			idx += 1
		elif cbyte == ord(' ') or \
			cbyte == ord('\t'):
			idx += 1
		elif (idx + 1) < len(sbyte) :
			nbyte = sbyte[(idx + 1)]
			if cbyte == ord('/') and nbyte == ord('/'):
				raise Exception('[%s]not accept comment'%(ints_to_string(sbyte)))
			elif cbyte == ord('/') and nbyte == ord('*'):
				rbyte , lbyte = __parse_comment(sbyte[idx:])
				idx = (len(sbyte) - len(lbyte))
			elif __is_common_char(cbyte):
				curname.append(cbyte)
				idx += 1
			else:
				raise Exception('[%s] on the [%d] not support [%s]'%())
		elif __is_common_char(cbyte):
			curname.append(cbyte)
			idx += 1
		else :
			raise Exception('[%s] on the [%d] not support [%s]'%())
	raise Exception('not handled [%s]'%(ints_to_string(sbyte)))
	return params,[]



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
