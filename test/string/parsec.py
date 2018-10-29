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

def uni16_handler(args,parser):
    set_logging_level(args)
    for c in args.subnargs:
        ints = strparser.string_to_uni16(c)
        cb = strparser.uni16_to_string(ints)
        sys.stdout.write('[%s] %s ret[%s]\n'%(c,ints,cb))
    sys.exit(0)
    return

def uni32_handler(args,parser):
    set_logging_level(args)
    for c in args.subnargs:
        ints = strparser.string_to_uni32(c)
        cb = strparser.uni32_to_string(ints)
        sys.stdout.write('[%s] %s ret[%s]\n'%(c,ints,cb))
    sys.exit(0)
    return


def getbit_handler(args,parser):
    set_logging_level(args)
    c = int(args.subnargs[0])
    bit = int(args.subnargs[1])
    rnum = strparser.get_bit(c,bit)
    sys.stdout.write('[%d:0x%x] get [%d] = [%d:0x%x]\n'%(c,c,bit,rnum,rnum))
    sys.exit(0)
    return

def clearbit_handler(args,parser):
    set_logging_level(args)
    c = int(args.subnargs[0])
    bit = int(args.subnargs[1])
    rnum = strparser.clear_bit(c,bit)
    sys.stdout.write('[%d:0x%x] clear [%d] = [%d:0x%x]\n'%(c,c,bit,rnum,rnum))
    sys.exit(0)
    return

def expandbit_handler(args,parser):
    set_logging_level(args)
    c = int(args.subnargs[0])
    bit = int(args.subnargs[1])
    rnum = strparser.expand_bit(c,bit)
    sys.stdout.write('[%d:0x%x] expand [%d] = [%d:0x%x]\n'%(c,c,bit,rnum,rnum))
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
