#! /usr/bin/env python

import extargsparse
import json
import sys
import logging

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


class Utf8Encode(object):
    def __dict_utf8(self,val):
        newdict =dict()
        for k in val.keys():
            newk = self.__encode_utf8(k)
            newv = self.__encode_utf8(val[k])
            newdict[newk] = newv
        return newdict

    def __list_utf8(self,val):
        newlist = []
        for k in val:
            newk = self.__encode_utf8(k)
            newlist.append(newk)
        return newlist

    def __encode_utf8(self,val):
        retval = val

        if sys.version[0]=='2' and isinstance(val,unicode):
            retval = val.encode('utf8')
        elif isinstance(val,dict):
            retval = self.__dict_utf8(val)
        elif isinstance(val,list):
            retval = self.__list_utf8(val)
        return retval

    def __init__(self,val):
        self.__val = self.__encode_utf8(val)
        return

    def __str__(self):
        return self.__val

    def __repr__(self):
        return self.__val
    def get_val(self):
        return self.__val


def read_odict(infile=None):
	fin = sys.stdin
	if infile is not None:
		fin = open(infile,'r')
	odict = json.load(fin)
	if fin != sys.stdin:
		fin.close()
	fin = None
	return Utf8Encode(odict).get_val()

def write_odict(odict,outfile=None):
	fout = sys.stdout
	if outfile is not None:
		fout = open(outfile,'w')
	json.dump(odict,fout)
	if fout != sys.stdout:
		fout.close()
	fout = None
	return

def set_odict(odict,val,*path):
	curodict = odict
	idx = 0
	while idx < len(path) - 1:
		if path[idx] not in curodict.keys():
			curodict[path[idx]] = dict()
		curodict = curodict[path[idx]]
		idx += 1
	curodict[path[idx]] = val
	return odict

def get_odict(odict,*path):
	idx = 0
	curodict = odict
	while idx < (len(path) - 1):
		if path[idx] not in curodict.keys():
			return None
		curodict = curodict[path[idx]]
		idx += 1
	logging.info('%s [%d][%s]'%(curodict,idx, path[idx]))
	if path[idx] not in curodict.keys():
		return None
	return curodict[path[idx]]

def create_odict_is_none(odict,*path):
    if get_odict(odict,*path) is None:
        val = dict()
        return set_odict(odict,val, *path)
    return odict


def set_handler(args,parser):
	set_logging_level(args)
	if len(args.subnargs) < 2:
		raise Exception('need at least val path...')
	odict = read_odict(args.input)
	odict = set_odict(odict,args.subnargs[0],*args.subnargs[1:])
	write_odict(odict,args.output)
	return


def get_handler(args,parser):
	set_logging_level(args)
	odict = read_odict(args.input)
	val = get_odict(odict,*args.subnargs)
	sys.stdout.write('%s value [%s]\n'%(args.subnargs,val))
	return

def create_handler(args,parser):
	set_logging_level(args)
	odict = read_odict(args.input)
	odict = create_odict_is_none(odict,*args.subnargs)
	sys.stdout.write('%s\n'%(odict))
	return



def main():
	commandline='''
	{
		"verbose|v" : "+",
		"input|i" : null,
		"output|o" : null,
		"set<set_handler>##val path... set value##" : {
			"$" : "+"
		},
		"get<get_handler>##path... get value##" : {
			"$" : "+"
		},
		"create<create_handler>##path ... create dict when not exists##" : {
			"$" : "+"
		}
	}
	'''
	parser = extargsparse.ExtArgsParse()
	parser.load_command_line_string(commandline)
	parser.parse_command_line(None,parser)
	return
main()