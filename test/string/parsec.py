#! /usr/bin/env python

import extargsparse
import logging
import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),'..','..','src'))
from strparser import *
from extract_ob import *

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

def uni16_handler(args,parser):
    set_logging_level(args)
    for c in args.subnargs:
        ints = string_to_uni16(c)
        cb = uni16_to_string(ints)
        sys.stdout.write('[%s] %s ret[%s]\n'%(c,ints,cb))
    sys.exit(0)
    return

def uni32_handler(args,parser):
    set_logging_level(args)
    for c in args.subnargs:
        ints = string_to_uni32(c)
        cb = uni32_to_string(ints)
        sys.stdout.write('[%s] %s ret[%s]\n'%(c,ints,cb))
    sys.exit(0)
    return


def getbit_handler(args,parser):
    set_logging_level(args)
    c = int(args.subnargs[0])
    bit = int(args.subnargs[1])
    rnum = get_bit(c,bit)
    sys.stdout.write('[%d:0x%x] get [%d] = [%d:0x%x]\n'%(c,c,bit,rnum,rnum))
    sys.exit(0)
    return

def clearbit_handler(args,parser):
    set_logging_level(args)
    c = int(args.subnargs[0])
    bit = int(args.subnargs[1])
    rnum = clear_bit(c,bit)
    sys.stdout.write('[%d:0x%x] clear [%d] = [%d:0x%x]\n'%(c,c,bit,rnum,rnum))
    sys.exit(0)
    return

def expandbit_handler(args,parser):
    set_logging_level(args)
    c = int(args.subnargs[0])
    bit = int(args.subnargs[1])
    rnum = expand_bit(c,bit)
    sys.stdout.write('[%d:0x%x] expand [%d] = [%d:0x%x]\n'%(c,c,bit,rnum,rnum))
    sys.exit(0)
    return

def dump_ints(ints):
    rets = ''
    idx = 0
    curidx = 0
    for c in ints:
        if (idx % 16) == 0:
            if idx > 0:
                rets += '\n'
            rets += '0x%08x'%(idx)
        rets += ' 0x%02x'%(c)
        idx += 1
    rets += '\n'
    return rets

def readint_handler(args,parser):
    set_logging_level(args)
    for f in args.subnargs:
        sbyte = b''
        with open(f,'rb') as fin:
            sbyte = fin.read()
        ints = bytes_to_ints(sbyte)
        sys.stdout.write('read [%s]\n%s'%(f,dump_ints(ints)))
    sys.exit(0)
    return


def obfunc_handler(args,parser):
    set_logging_level(args)
    exob = ExtractOb(args.input)
    odict = exob.get_ob_funcs(args.subnargs)
    for k in odict.keys():
        sys.stdout.write('[%s]=[%s]\n'%(k,odict[k]))
    sys.exit(0)
    return

def main():
    commandline='''
    {
        "verbose|v" : "+",
        "input|i" : null,
        "string<string_handler>##str... to parse string handler##" : {
            "$" : "+"
        },
        "param<param_handler>##str... to parse param handler##" : {
            "$" : "+"
        },
        "uni16<uni16_handler>##str... to parse unicode 16 le handler##" : {
            "$" : "+"
        },
        "uni32<uni32_handler>##str... to parse unicode 32 le handler##" : {
            "$" : "+"
        },
        "getbit<getbit_handler>##number bits to get the bit number##" : {
            "$" : 2
        },
        "clearbit<clearbit_handler>##number bits to clear the bit and number##" : {
            "$" : 2
        },
        "expandbit<expandbit_handler>##number bits to expand the bit for number##" : {
            "$" : 2
        },
        "readint<readint_handler>##files... to dump file int##" : {
            "$" : "+"
        },
        "obfunc<obfunc_handler>##funcs... to get funcname##" : {
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
