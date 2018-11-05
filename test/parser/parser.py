#! /usr/bin/env python

import extargsparse
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','src')))
from filehdl import *
from pyparser import *
from elfparser import *
from coffparser import *


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

def elfsym_handler(args,parser):
	set_logging_level(args)
	if len(args.subnargs) < 2:
		raise Exception('elffile symbol... needed')
	fname = args.subnargs[0]
	elffile = ElfParser(fname)
	for sym in args.subnargs[1:]:
		offset = elffile.func_offset(sym)
		reloff = elffile.func_vaddr(sym)
		size = elffile.func_size(sym)
		sys.stdout.write('[%s].[%s] fileoff[0x%x] offset[0x%x] size[0x%x]\n'%(fname,sym,offset,reloff,size))
		sys.stdout.write('relocation [%s]\n'%(sym))
		startaddr = None
		for i in range(size):
			vaddr = reloff + i
			if elffile.is_in_reloc(vaddr,sym):
				if startaddr is None:
					startaddr = vaddr
			else:
				if startaddr is not None:
					sys.stdout.write('[%s].[%s][0x%x] [+0x%x]reloc\n'%(fname,sym,startaddr, startaddr - reloff))
					startaddr = None
		if startaddr is not None:
			sys.stdout.write('[%s].[%s][0x%x] [+0x%x]reloc\n'%(fname,sym,startaddr, startaddr - reloff))
			startaddr = None
	sys.exit(0)
	return

def coffsym_handler(args,parser):
	set_logging_level(args)
	if len(args.subnargs) < 2:
		raise Exception('cofffile symbol... needed')
	fname = args.subnargs[0]
	cofffile = CoffParser(fname)
	for sym in args.subnargs[1:]:
		offset = cofffile.func_offset(sym)
		reloff = cofffile.func_vaddr(sym)
		size = cofffile.func_size(sym)
		sys.stdout.write('[%s].[%s] fileoff[0x%x] offset[0x%x] size[0x%x]\n'%(fname,sym,offset,reloff,size))
		sys.stdout.write('relocation [%s]\n'%(sym))
		startaddr = None
		for i in range(size):
			vaddr = reloff + i
			if cofffile.is_in_reloc(vaddr,sym):
				if startaddr is None:
					startaddr = vaddr
			else:
				if startaddr is not None:
					sys.stdout.write('[%s].[%s][0x%x] [+0x%x]reloc\n'%(fname,sym,startaddr, startaddr - reloff))
					startaddr = None
		if startaddr is not None:
			sys.stdout.write('[%s].[%s][0x%x] [+0x%x]reloc\n'%(fname,sym,startaddr, startaddr - reloff))
			startaddr = None
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
		},
		"elfsym<elfsym_handler>##elffile symbol... to extract symbol offset and get size##" : {
			"$" : "+"
		},
		"coffsym<coffsym_handler>##cofffile symbol... to extract symbol offset and get size##" : {
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
