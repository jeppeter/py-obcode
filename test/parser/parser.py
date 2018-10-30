#! /usr/bin/env python

import extargsparse
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','src')))
from filehdl import *
from pyparser import *


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



def py_handler(args,parser):
	set_logging_level(args)
	for f in args.subnargs:
		m = get_import_names(f)
		idx = 0
		sys.stdout.write('[%s] import\n'%(f))
		while idx < len(m):
			sys.stdout.write('\tm [%s] fm [%s]\n'%(m[idx].frommodule,m[idx].module))
			idx += 1
	sys.exit(0)
	return

def filter_handler(args,parser):
	set_logging_level(args)
	for d in args.subnargs:
		fs = get_file_filter(d)
		idx = 0
		sys.stdout.write('[%s] has'%(d))
		while idx < len(fs):
			if (idx % 5) == 0:
				sys.stdout.write('\n\t')
			sys.stdout.write(' %s'%(fs[idx]))
			idx += 1
		sys.stdout.write('\n')
	sys.exit(0)
	return

def pack_handler(args,parser):
	set_logging_level(args)
	ims = []
	for f in args.subnargs:
		ims.extend(get_import_names(f))
	ims = packed_import(ims)
	idx = 0
	sys.stdout.write('get files:')
	for f in args.subnargs:
		if (idx % 5) == 0:
			sys.stdout.write('\n\t')
		sys.stdout.write(' %s'%(f))
		idx += 1
	sys.stdout.write('\n')
	sys.stdout.write('import files:\n')
	for im in ims:
		sys.stdout.write('%s\n'%(format_import(im)))
	sys.exit(0)
	return



def main():
	commandline='''
	{
		"verbose|v" : "+",
		"py<py_handler>##pyfile ... to parse python file##" : {
			"$" : "+"
		},
		"filter<filter_handler>##dir ... to get python file in the directory ##" : {
			"$" : "+"
		},
		"pack<pack_handler>##pyfiles... to pack out python file import##" : {
			"$" : "+"
		}
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	parser.parse_command_line(None,parser)
	raise Exception('can not run here')
	return


if __name__ == '__main__':
	main()
