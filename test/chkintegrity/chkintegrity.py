#! /usr/bin/env python

import extargsparse
import sys
import os
import zlib
import hashlib
import sha3
import re

##importdebugstart
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..','src'))
from strparser import *
##importdebugend

def read_bytes(infile):
	data = b''
	with open(infile,'rb') as fin:
		data = fin.read()
	return data

def write_bytes(b, outfile):
	with open(outfile,'wb') as fout:
		fout.write(b)
	return

def crc32_calc(infile):
	crcval = zlib.crc32(read_bytes(infile))
	return crcval

def md5_calc(infile):
	m = hashlib.md5()
	m.update(read_bytes(infile))
	return m.hexdigest()

def sha256_calc(infile):
	m = hashlib.sha256()
	m.update(read_bytes(infile))
	return m.hexdigest()

def sha3_calc(infile):
	m = sha3.sha3_512()
	m.update(read_bytes(infile))
	return m.hexdigest()


def crc32_handler(args,parser):
	set_logging_level(args)
	for f in args.subnargs:
		crcval = crc32_calc(f)
		if crcval < 0:			
			crcval = crcval + 0xffffffff + 1
		sys.stdout.write('[%s] crc32 [0x%x:%d]\n'%(f,crcval,crcval))
	sys.exit(0)
	return

def md5_handler(args,parser):
	set_logging_level(args)
	for f in args.subnargs:
		sys.stdout.write('[%s] md5 %s\n'%(f, md5_calc(f)))
	sys.exit(0)
	return

def sha256_handler(args,parser):
	set_logging_level(args)
	for f in args.subnargs:
		sys.stdout.write('[%s] sha256 %s\n'%(f, sha256_calc(f)))
	sys.exit(0)
	return

def sha3_handler(args,parser):
	set_logging_level(args)
	for f in args.subnargs:
		sys.stdout.write('[%s] sha3 %s\n'%(f, sha3_calc(f)))
	sys.exit(0)
	return

def trans_bytes(infile):
	retb = b''
	with open(infile,'r') as fin:
		for l in fin:
			l = l.rstrip('\r\n')
			sarr = re.split(':',l)
			if len(sarr) < 2:
				continue				
			nsarr = re.split('\s{2,}', sarr[1])
			if len(nsarr) < 1:
				continue
			nsarr = re.split('\s+',nsarr[0])
			logging.info('nsarr %s'%(nsarr))
			for b in nsarr:
				if len(b) == 0:
					continue
				if b.startswith('0x') or \
					b.startswith('0X'):
					b = b[2:]
				elif b.startswith('x') or \
					b.startswith('X'):
					b = b[1:]
				curb = int(b,16)
				if sys.version[0] == '3':
					retb += curb.to_bytes(1,'little')
				else:
					retb += chr(curb)
	return retb

def dump_handler(args,parser):
	set_logging_level(args)
	b = trans_bytes(args.subnargs[0])
	write_bytes(b,args.subnargs[1])
	sys.exit(0)
	return

def main():
	commandline='''
	{
		"verbose|v" : "+",
		"crc32<crc32_handler>" : {
			"$" : "+"
		},
		"md5<md5_handler>" : {
			"$" : "+"
		},
		"sha256<sha256_handler>" : {
			"$" : "+"
		},
		"sha3<sha3_handler>" : {
			"$" : "+"
		},
		"dump<dump_handler>" : {
			"$" : 2
		}
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	args = parser.parse_command_line(None,parser)
	raise Exception('can not parse %s for [%s]'%(sys.argv[1:], args))
	return

if __name__ == '__main__':
	main()
