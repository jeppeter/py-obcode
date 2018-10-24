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



def parse_string(sbyte):
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

def parse_raw_string(sbyte):
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

def parse_single_quote(sbyte):
	if sbyte[0] != ord('\''):
		raise Exception('[%s] not startswith [\']'%(ints_to_string(sbyte)))
	idx = 1
	retbyte= []
	lbyte = []
	while idx < len(sbyte):
		cbyte = sbyte[idx]
		if cbyte == ord('\''):
			idx += 1
			if idx < len(sbyte):
				lbyte = sbyte[idx:]
			return retbyte,lbyte
		elif cbyte == '\\':
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
	raise Exception('not closed single quote [%s]'%(ints_to_string(sbyte)))
	return retbyte,[]

def parse_raw_single_quote(sbyte):
	if sbyte[0] != ord('\''):
		raise Exception('[%s] not startswith [\']'%(ints_to_string(sbyte)))
	idx = 1
	retbyte= []
	lbyte = []
	while idx < len(sbyte):
		cbyte = sbyte[idx]
		if cbyte == ord('\''):
			idx += 1
			if idx < len(sbyte):
				lbyte = sbyte[idx:]
			return retbyte,lbyte
		elif cbyte == '\\':
			idx += 1
			if idx >= len(sbyte):
				break
			nbyte = sbyte[idx]
			retbyte.append(cbyte)
			retbyte.append(nbyte)
		else:
			retbyte.append(cbyte)
		idx += 1
	raise Exception('not closed single quote [%s]'%(ints_to_string(sbyte)))
	return retbyte,[]

def is_common_char(c):
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
	if c == ord('|') or c == ord('&') or c == ord('^') or \
		c == ord('%') or c == ord('!') or c == ord('~') or \
		c == ord('.') or c == ord('[') or c == ord(']') :
		return True
	return False

def is_space_char(c):
	if c == ord(' ') or c == ord('\t'):
		return True
	return False

def parse_lbrace(sbyte):
	if sbyte[0] != ord('\x28'):
		raise Exception('[%s] not startwith [\x28]'%(ints_to_string(sbyte)))
	idx = 1
	rbyte = []
	lbyte = []
	while idx < len(sbyte):
		cbyte = sbyte[idx]
		if cbyte == ord('\x29'):
			idx += 1
			lbyte = []
			if idx < len(sbyte):
				lbyte = sbyte[idx:]
			return rbyte,lbyte
		elif cbyte == ord('\x28'):
			crbyte , lbyte= parse_lbrace(sbyte[idx:])
			rbyte.append(ord('\x28'))
			rbyte.extend(crbyte)
			rbyte.append(ord('\x29'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('{'):
			crbyte, lbyte = parse_bracket(sbyte[idx:])
			rbyte.append(ord('{'))
			rbyte.extend(crbyte)
			rbyte.append(ord('}'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('"'):
			crbyte, lbyte = parse_raw_string(sbyte[idx:])
			rbyte.append(ord('"'))
			rbyte.extend(crbyte)
			rbyte.append(ord('"'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('\''):
			crbyte , lbyte = parse_raw_single_quote(sbyte[idx:])
			rbyte.append(ord('\''))
			rbyte.extend(crbyte)
			rbyte.append(ord('\''))
			idx = (len(sbyte) - len(lbyte))
		elif (idx + 1) < len(sbyte):
			nbyte = sbyte[(idx + 1)]
			if cbyte == ord('/') and nbyte == ord('/'):
				raise Exception('[%s]can not accept for the // comment'%(ints_to_string(sbyte)))
			elif cbyte == ord('/') and nbyte == ord('*'):
				crbyte, lbyte = parse_comment(sbyte[idx:])
				idx = (len(sbyte) - len(lbyte))
			elif is_common_char(cbyte) or is_space_char(cbyte) or cbyte == ord(','):
				rbyte.append(cbyte)
				idx += 1
			else:
				raise Exception('[%s] not accept [%d]'%(ints_to_string(sbyte), idx))
		elif is_common_char(cbyte) or cbyte == ord(','):
			rbyte.append(cbyte)
			idx += 1
		elif is_space_char(cbyte):
			rbyte.append(cbyte)
			idx += 1
		else:
			raise Exception('[%s] not accept [%d]'%(ints_to_string(sbyte),idx))
	raise Exception('[%s] not paired '%(ints_to_string(sbyte)))
	return rbyte,[]


def parse_bracket(sbyte):
	if sbyte[0] != ord('{'):
		raise Exception('[%s] not startwith [{]'%(ints_to_string(sbyte)))
	idx = 1
	rbyte = []
	lbyte = []
	while idx < len(sbyte):
		cbyte = sbyte[idx]
		if cbyte == ord('}'):
			idx += 1
			lbyte = []
			if idx < len(sbyte):
				lbyte = sbyte[idx:]
			return rbyte,lbyte
		elif cbyte == ord('\x28'):
			crbyte , lbyte= parse_lbrace(sbyte[idx:])
			rbyte.append(ord('\x28'))
			rbyte.extend(crbyte)
			rbyte.append(ord('\x28'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('{'):
			crbyte, lbyte = parse_bracket(sbyte[idx:])
			rbyte.append(ord('{'))
			rbyte.extend(crbyte)
			rbyte.append(ord('}'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('"'):
			crbyte, lbyte = parse_raw_string(sbyte[idx:])
			rbyte.append(ord('"'))
			rbyte.extend(crbyte)
			rbyte.append(ord('"'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('\''):
			crbyte , lbyte = parse_raw_single_quote(sbyte[idx:])
			rbyte.append(ord('\''))
			rbyte.extend(crbyte)
			rbyte.append(ord('\''))
			idx = (len(sbyte) - len(lbyte))
		elif (idx + 1) < len(sbyte):
			nbyte = sbyte[(idx + 1)]
			if cbyte == ord('/') and nbyte == ord('/'):
				raise Exception('[%s]can not accept for the // comment'%(ints_to_string(sbyte)))
			elif cbyte == ord('/') and nbyte == ord('*'):
				crbyte, lbyte = parse_comment(sbyte[idx:])
				idx = (len(sbyte) - len(lbyte))
			elif is_common_char(cbyte) or is_space_char(cbyte) or cbyte == ord(','):
				rbyte.append(cbyte)
				idx += 1
			else:
				raise Exception('[%s] not accept [%d]'%(ints_to_string(sbyte), idx))
		elif is_common_char(cbyte) or cbyte == ord(','):
			rbyte.append(cbyte)
			idx += 1
		elif is_space_char(cbyte):
			rbyte.append(crbyte)
			idx += 1
		else:
			raise Exception('[%s] not accept [%d]'%(ints_to_string(sbyte),idx))
	raise Exception('[%s] not paired '%(ints_to_string(sbyte)))
	return rbyte,[]


def parse_param(sbyte):
	idx = 0
	lbyte = sbyte
	if sbyte[0] != ord('\x28'):
		raise Exception('param [%s] not [\x28] started '%(ints_to_string(sbyte)))
	params = []
	idx = 1
	curparam = []
	curname = []
	while idx < len(sbyte):
		cbyte = sbyte[idx]
		if cbyte == ord('\x28'):
			rbyte, lbyte = parse_lbrace(sbyte[idx:])
			curname.append(ord('\x28'))
			curname.extend(rbyte)
			curname.append(ord('\x29'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('{'):
			rbyte, lbyte = parse_bracket(sbyte[idx:])
			curname.append(ord('{'))
			curname.extend(rbyte)
			curname.append(ord('}'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord('\x29'):
			if len(curname) > 0:
				params.append(ints_to_string(curname))
				curname = []
			idx += 1
			lbytes = []
			if idx < len(sbyte):
				lbytes = sbyte[idx:]
			return params,lbytes
		elif cbyte == ord('"'):
			rbyte, lbyte = parse_raw_string(sbyte[idx:])
			curname.append(ord('"'))
			curname.extend(rbyte)
			curname.append(ord('"'))
			idx = (len(sbyte) - len(lbyte))
		elif cbyte == ord(','):
			if len(curname) == 0:
				raise Exception('[%s] has empty param [%s]'%(ints_to_string(sbyte), ints_to_string(sbyte[idx:])))
			params.append(ints_to_string(curname))
			curname = []
			idx += 1
		elif is_space_char(cbyte):
			idx += 1
		elif (idx + 1) < len(sbyte) :
			nbyte = sbyte[(idx + 1)]
			if cbyte == ord('/') and nbyte == ord('/'):
				raise Exception('[%s]not accept comment'%(ints_to_string(sbyte)))
			elif cbyte == ord('/') and nbyte == ord('*'):
				rbyte , lbyte = parse_comment(sbyte[idx:])
				idx = (len(sbyte) - len(lbyte))
			elif is_common_char(cbyte):
				curname.append(cbyte)
				idx += 1
			elif is_space_char(cbyte):
				idx += 1
			else:
				raise Exception('[%s] on the [%d] not support [%s]'%())
		elif is_common_char(cbyte):
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
		cbyte,lbyte = parse_string(sbyte)
		logging.info('cbyte [%s] lbyte [%s]'%(cbyte,lbyte))
		cs = ints_to_string(cbyte)
		ls = ints_to_string(lbyte)
		sys.stdout.write('cbyte [%s] lbyte [%s]\n'%(cs,ls))
	sys.exit(0)	
	return

def param_handler(args,parser):
	set_logging_level(args)
	idx = 0
	for s in args.subnargs:
		sbyte = string_to_ints(s)
		startidx=0
		while startidx < len(sbyte):
			if sbyte[startidx] == ord('\x28'):				
				break
			startidx += 1
		params, lbyte = parse_param(sbyte[startidx:])
		ls = ints_to_string(lbyte)
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
