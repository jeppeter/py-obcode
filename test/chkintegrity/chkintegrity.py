#! /usr/bin/env python

import extargsparse
import sys
import os
import zlib

##importdebugstart
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..','src'))
from strparser import *
##importdebugend

def crc32_calc(infile):
	fin = open(infile,'rb')
	data = fin.read()
	crcval = zlib.crc32(data)
	fin.close()
	fin = None
	return crcval

def crc32_handler(args,parser):
	set_logging_level(args)
	for f in args.subnargs:
		crcval = crc32_calc(f)
		if crcval < 0:			
			crcval = crcval + 0xffffffff + 1
		sys.stdout.write('[%s] crc32 [0x%x:%d]\n'%(f,crcval,crcval))
	sys.exit(0)
	return

def main():
	commandline='''
	{
		"verbose|v" : "+",
		"crc32<crc32_handler>" : {
			"$" : "+"
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
