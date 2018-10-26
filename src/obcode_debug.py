#! /usr/bin/env python

import extargsparse
import sys
import re
import logging
import os
import shutil
import random
import json


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
    # this is the end of the file
    ri.append(0)
    return ri


def ints_to_string(sbyte):
    if len(sbyte) >= 1 and sbyte[-1] == 0:
        sbyte = sbyte[:-1]
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

def string_to_uniints(s):
    sbyte = []
    ri = []
    if sys.version[0] == '3':
        rb = s.encode('utf-16-le')
    else:       
        rc = s.decode('utf8')   
        rb = rc.encode('utf-16-le')
    for i in range(len(rb)):
        if sys.version[0] == '3':
            ri.append(int(rb[i]))
        else:
            ri.append(ord(rb[i]))
    # to add null for unicode
    ri.append(0)
    ri.append(0)
    return ri

def uniints_to_string(sbyte):
    s = ''  
    if len(sbyte) >= 2 and sbyte[-1] == 0 and sbyte[-2] == 0:
        sbyte = sbyte[:-2]
    nbyte = []
    nbyte.append(255)
    nbyte.append(254)
    nbyte.extend(sbyte)
    if sys.version[0] == '3':
        cb = b''
        for i in range(len(nbyte)):
            cb += nbyte[i].to_bytes(1,'little')
        return cb.decode('utf-16-le')
    else:
        cb = b''
        for i in range(len(nbyte)):
            cb += chr(nbyte[i])
        cs = cb.decode('utf-16-le')
        return cs.encode('utf8')


def is_normal_char(cbyte):
    if cbyte >= ord('0') and cbyte <= ord('9'):
        return True
    if cbyte >= ord('a') and cbyte <= ord('z'):
        return True
    if cbyte >= ord('A') and cbyte <= ord('Z'):
        return True
    if cbyte >= ord('_'):
        return True

    return False

def is_decimal_char(cbyte):
    if cbyte >= ord('0') and cbyte <= ord('9'):
        return True
    return False


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

def string_to_uniints(s):
    c = []
    uni = s.encode('utf-16')
    for i in range(len(uni)):
        if i > 1:
            if sys.version[0] == '3':
                c.append(int(uni[i]))
            else:
                c.append(ord(uni[i]))
    return c

def uniints_to_string(sbyte):
    nbyte = [255,254]
    s = ''
    nbyte.extend(sbyte)
    cb = b''
    if sys.version[0] == '3':
        for i in range(len(nbyte)):
            cb += nbyte[i].to_bytes(1,'little')
        return cb.decode('utf-16')

    for i in range(len(nbyte)):
        cb += chr(nbyte[i])
    return cb.decode('utf-16')

def get_bits(num):
    bits = 0
    fnum = num
    while fnum > 0:
        if fnum & 1:
            bits += 1
        fnum >>= 1
    return bits

def clear_bit(num,nbit):
    num = num & 0xff
    bits = get_bits(num)
    if bits == 0:
        return 0
    needbit = (nbit % bits)
    needbit += 1
    cnum = 1
    fnum = num
    curbit = 0
    while curbit < needbit:
        if fnum & cnum:
            curbit += 1
            if curbit == needbit:
                fnum = fnum & (~cnum)
                return fnum
        cnum <<= 1
    return fnum

def get_bit(num, nbit):
    num = num & 0xff
    bits = get_bits(num)
    if bits == 0:
        return 0
    needbit = (nbit % bits)
    needbit += 1
    cnum = 1
    fnum = num
    curbit = 0
    while curbit < needbit:
        if fnum & cnum:
            curbit += 1
            if curbit == needbit:
                return cnum
        cnum <<= 1
    return fnum

def expand_bit(num,nbit):
    num = num & 0xff
    bits = get_bits(num)
    maxbits = (8 - bits)
    # if all is expand bit ,so we just return 0xff
    if maxbits == 0:
        return 0xff
    needbit = (nbit % maxbits)
    needbit += 1
    curbit = 0
    cnum = 1
    fnum = num
    while curbit < needbit:
        if (fnum & cnum)== 0:
            # this is the not set ,so just set for it
            curbit += 1
            if curbit == needbit:
                fnum = fnum | cnum
                return fnum
        cnum <<= 1
    return fnum


def read_file(infile=None):
    fin = sys.stdin
    if infile is not None:
        fin = open(infile,'rb')
    rets = ''
    for l in fin:
        s = l
        if 'b' in fin.mode:
            if sys.version[0] == '3':
                s = l.decode('utf-8')
        rets += s

    if fin != sys.stdin:
        fin.close()
    fin = None
    return rets

def write_file(s,outfile=None):
    fout = sys.stdout
    if outfile is not None:
        fout = open(outfile, 'w+b')
    outs = s
    if 'b' in fout.mode:
        outs = s.encode('utf-8')
    fout.write(outs)
    if fout != sys.stdout:
        fout.close()
    fout = None
    return 

def append_file(s,outfile=None):
    fout = sys.stdout
    if outfile is not None:
        fout = open(outfile, 'a+b')
    outs = s
    if 'b' in fout.mode:
        outs = s.encode('utf-8')
    fout.write(outs)
    if fout != sys.stdout:
        fout.close()
    fout = None
    return 


def format_object_string(odict,tabs):
    s = json.dumps(odict,indent=4)
    logging.info('s\n%s'%(s))
    sarr = re.split('\n', s)
    idx = 1
    rets = ''
    while idx < (len(sarr) - 1):
        curs = sarr[idx]
        curs = curs.rstrip('\r\n')
        if idx == (len(sarr) - 2):
            rets += format_tabs(tabs)
            rets += '%s'%(curs)
        else:
            rets += format_line('%s'%(curs), tabs)
        idx += 1    
    return rets


def get_file_lines(sfile=None):
    rets = read_file(sfile)
    retsarr = []
    sarr = re.split('\n', rets)
    for c in sarr:
        c = c.rstrip('\r\n')
        retsarr.append(c)
    return retsarr

def format_comment_line(l):
    s = ''
    idx = 0
    while idx < len(l):
        if l[idx] == '*':
            s += '\\*'
        elif l[idx] == '/':
            s += '\\/'
        else:
            s += l[idx]
        idx += 1
    return s

def count_tabs(l):
    tabs = 0
    idx =0
    curspace = 0
    while idx < len(l):
        c = l[idx]
        if c == ' ':
            curspace += 1
            if curspace == 4:
                tabs += 1
                curspace = 0
        elif c == '\t':
            tabs += 1
        else:
            break
        idx += 1
    return tabs


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

GL_VAR_NAME_VARS=''
for i in range(26):
    GL_VAR_NAME_VARS += chr(ord('a')+i)

for i in range(26):
    GL_VAR_NAME_VARS += chr(ord('A') + i)

for i in range(10):
    GL_VAR_NAME_VARS += chr(ord('0')+i)

GL_RANDOM_NAMES=[]

def get_random_name(num=10):
    global GL_VAR_NAME_VARS
    global GL_RANDOM_NAMES
    retval = True
    while retval:
        retval = False
        retstr = ''
        idx = 0
        while idx < num:
            rnd = random.randint(0, len(GL_VAR_NAME_VARS)-1)
            retstr += GL_VAR_NAME_VARS[rnd]
            idx = idx +1 
        if retstr in GL_RANDOM_NAMES:
            retval = True
        else:
            GL_RANDOM_NAMES.append(retstr)

    return retstr

def clear_random_name():
    global GL_ADD_NAMES
    GL_ADD_NAMES=[]
    return
def format_tabs(tabs=0):
    rets = ''
    for i in range(tabs):
        rets += '    '
    return rets

def format_line(l, tab=0):
    retstr = ''
    retstr += format_tabs(tab)
    retstr += '%s\n'%(l)
    return retstr

def quote_string(l):
    rets = ''
    if l is not None:
        for c in l:
            if c == '\\':
                rets += '\\\\'
            elif c == '"':
                rets += '\\"'
            else:
                rets += c
    return rets

def format_debug_line(l,tab=0,debug=0):
    rets = ''
    if debug >= 3:
        rets += format_line('/* %s */'%(format_comment_line(l)), tab)
    return rets

def format_xor_encode_function(nameprefix='prefix',namelen=10,tabs=0,debug=0):
    funcstr = ''
    funcname = '%s_%s'%(nameprefix,get_random_name(namelen))
    if debug >= 3:
        funcstr += format_line('/*********************************************',tabs)
        funcstr += format_line('* to make xor encoded functions', tabs)
        funcstr += format_line('* it will be simple ,may be it will give more complex', tabs)
        funcstr += format_line('*********************************************/',tabs)
    funcstr += format_debug_line('variable:namelen %d variable:prefix [%s]'%(namelen,nameprefix), tabs,debug)
    funcstr += format_line('int %s(unsigned char* pbuf,int size,unsigned char* pxorcode, int xorsize)'%(funcname),tabs)
    funcstr += format_line('{',tabs)
    funcstr += format_line('int i,curi;',tabs+1)
    funcstr += format_line('',tabs)
    funcstr += format_line('for (i=0;i<size;i++){', tabs + 1)
    funcstr += format_line('curi = (i % xorsize);',tabs + 2)
    funcstr += format_line('pbuf[i] = (unsigned char)(pbuf[i] ^ pxorcode[curi]);', tabs + 2)
    funcstr += format_line('}', tabs + 1)
    funcstr += format_line('', tabs)
    funcstr += format_line('return size;',tabs + 1)
    funcstr += format_line('}',tabs)
    return funcstr,funcname

def format_xor_decode_function(nameprefix='prefix_',namelen=10, tabs=0, debug=0):
    funcstr = ''
    funcname = '%s_%s'%(nameprefix,get_random_name(namelen))
    if debug >= 3:
        funcstr += format_line('/*********************************************',tabs)
        funcstr += format_line('* to make xor decoded functions', tabs)
        funcstr += format_line('* it will be simple ,may be it will give more complex', tabs)
        funcstr += format_line('*********************************************/',tabs)
    funcstr += format_debug_line('variable:namelen %d variable:prefix [%s]'%(namelen,nameprefix), tabs,debug)
    funcstr += format_line('int %s(unsigned char* pbuf,int size,unsigned char* pxorcode, int xorsize)'%(funcname),tabs)
    funcstr += format_line('{',tabs)
    funcstr += format_line('int i,curi;',tabs+1)
    funcstr += format_line('',tabs)
    funcstr += format_line('for (i=0;i<size;i++){', tabs + 1)
    funcstr += format_line('curi = (i % xorsize);',tabs + 2)
    funcstr += format_line('pbuf[i] = (unsigned char)(pbuf[i] ^ pxorcode[curi]);', tabs + 2)
    funcstr += format_line('}', tabs + 1)
    funcstr += format_line('', tabs)
    funcstr += format_line('return size;',tabs + 1)
    funcstr += format_line('}',tabs)
    return funcstr,funcname


def get_xor_code(cnum=16):
    xorcode = []
    for i in range(cnum):
        xorcode.append(random.randint(0,255))
    return xorcode

    

def format_key_ctr_function(xorcode,nameprefix='prefix', namelen=10, numturns=30, tabs=0,debug=0):
    funcstr = ''
    funcname = '%s_%s'%(nameprefix,get_random_name(namelen))
    presentxor = []
    funcstr += format_line('int %s(unsigned char* pbuf,int size)'%(funcname),tabs)
    funcstr += format_line('{',tabs)
    codestr = ''
    for i in range(len(xorcode)):
        if i > 0:
            codestr  += ','
        codestr += '0x%02x'%(xorcode[i])
    funcstr += format_debug_line('keys %s  size %d'%(codestr,len(xorcode)), tabs + 1 , debug)
    funcstr += format_line('',tabs)    
    for i in range(len(xorcode)):
        if (i%5) == 0:
            funcstr += format_line('',tabs)
        curnum = random.randint(0, 255)
        funcstr += format_line('if ( %d < size) {'%(i), tabs + 1)
        funcstr += format_line('pbuf[%d] = %d;'%(i,curnum), tabs + 2)
        funcstr += format_line('}',tabs + 1)
        presentxor.append(curnum)

    funcstr += format_line('',tabs)
    funcstr += format_debug_line('variable:numturns %d'%(numturns), tabs + 1, debug)
    for i in range(numturns):
        if (i%5) == 0 and i > 0:
            funcstr += format_line('',tabs)
        curi = random.randint(0, len(xorcode)-1)
        curj = random.randint(0, len(xorcode)-1)
        funcstr += format_line('if (%d < size && %d < size){'%(curi,curj), tabs + 1)
        funcstr += format_debug_line('%d = %d ^ %d'%((presentxor[curi] ^ presentxor[curj]) & 0xff, presentxor[curi],presentxor[curj]), tabs + 2,debug)
        presentxor[curi] = (presentxor[curi] ^ presentxor[curj]) & 0xff
        funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] ^ pbuf[%d]);'%(curi, curi, curj),tabs + 2)
        funcstr += format_line('}', tabs + 1)

    for i in range(len(xorcode)):
        if (i%3) == 0:
            funcstr += format_line('', tabs)
        curi = random.randint(0, len(xorcode)-1)
        curv = presentxor[i] ^ presentxor[curi]
        curv = xorcode[i] ^ curv
        funcstr += format_line('if (%d < size){'%(curi), tabs + 1)
        funcstr += format_debug_line('%d = %d ^ %d'%((presentxor[curi] ^ presentxor[curj]) & 0xff, presentxor[curi],presentxor[curj]), tabs + 2,debug)
        presentxor[i] = (presentxor[i] ^ presentxor[curi]) & 0xff
        funcstr += format_debug_line('%d = %d ^ %d'%((presentxor[i] ^ curv) & 0xff, presentxor[curi],curv), tabs + 2,debug)
        presentxor[i] = (presentxor[i] ^ curv) & 0xff
        assert(presentxor[i] == xorcode[i])
        funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] ^ pbuf[%d]);'%(i ,i,curi), tabs+2)
        funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] ^ %d);'%(i,i,curv), tabs+2)
        funcstr += format_line('}', tabs + 1)

    funcstr += format_line('',tabs)
    funcstr += format_line('return %d < size ? %d : size;'%(len(xorcode),len(xorcode)), tabs+1)
    funcstr += format_line('}',tabs)
    return funcstr,funcname

def format_key_dtr_function(xorcode,nameprefix='prefix', namelen=10, numturns=30, tabs=0,debug=0):
    funcstr = ''
    funcname = '%s_%s'%(nameprefix,get_random_name(namelen))
    funcstr += format_line('void %s(unsigned char* pbuf,int size)'%(funcname),tabs)
    funcstr += format_line('{',tabs)
    funcstr += format_debug_line('variable:nameprefix %s variable:namelen %d variable:numturns %d'%(nameprefix,namelen,numturns), tabs+1,debug)
    funcstr += format_line('',tabs)
    storecode = []
    for x in xorcode:
        storecode.append(x)
    for i in range(numturns):
        if (i%5) == 0:
            funcstr += format_line('',tabs)
        curi = random.randint(0, len(xorcode)-1)
        curj = random.randint(0, len(xorcode)-1)
        funcstr += format_line('if (%d < size && %d < size){'%(curi,curj), tabs+1)
        funcstr += format_debug_line('%d = %d ^ %d'%((storecode[curi] ^ storecode[curj]),storecode[curi],storecode[curj]), tabs + 2, debug)
        funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] ^ pbuf[%d]);'%(curi, curi, curj),tabs + 2)
        funcstr += format_line('}',tabs + 1)


    funcstr += format_line('',tabs)
    funcstr += format_line('return;',tabs + 1)
    funcstr += format_line('}',tabs)
    return funcstr,funcname

def format_bytes_set_function(sbyte,nameprefix='prefix', namelen=10, numturns=30, tabs=0,debug=0):
    funcname = '%s_%s'%(nameprefix,get_random_name(namelen))
    funcstr = ''
    funcstr += format_line('int %s(unsigned char* pbuf, int size)'%(funcname),tabs)
    funcstr += format_line('{', tabs)
    funcstr += format_debug_line('variable:nameprefix %s variable:namelen %d variable:numturns %d'%(nameprefix,namelen,numturns), tabs + 1, debug)
    ss = ''
    for c in sbyte:
        if len(ss) > 0:
            ss += ',0x%02x'%(c)
        else:
            ss += 'sbyte [0x%02x'%(c)
    ss += ']'
    funcstr += format_debug_line('%s'%(ss), tabs + 1, debug)
    clbits = []
    for i in range(len(sbyte)):
        clbits.append(random.randint(0,255))

    for i in range(len(sbyte)):
        curnum = clear_bit(sbyte[i], clbits[i])
        funcstr += format_line('',tabs+1)
        funcstr += format_debug_line('0x%x = 0x%x & 0x%x'%(sbyte[i],curnum), tabs + 1, debug)
        funcstr += format_line('if (size > %d){'%(i), tabs + 1)
        funcstr += format_line('pbuf[%d] = pbuf[%d] & 0x%x;'%(i,i,curnum), tabs + 2)
        funcstr += format_line('}',tabs + 1)

    # we need not to set the number directly ,but just used
    for i in range(numturns):
        cidx = random.randint(0, len(sbyte) - 1)
        cbit = random.randint(0, 255)
        if random.randint(0,1) == 1:
            cnum = clear_bit(sbyte[cidx], cbit)
            funcstr += format_line('', tabs + 1)
            funcstr += format_line('if ( size > %d){'%(cidx), tabs + 1)
            funcstr += format_line('pbuf[%d] = pbuf[%d] | 0x%x;'%(cidx,cidx, cnum), tabs + 2)
            funcstr += format_line('}', tabs + 1)
        else:
            cnum = expand_bit(sbyte[cidx], cbit)
            funcstr += format_line('', tabs + 1)
            funcstr += format_line('if ( size > %d){'%(cidx), tabs + 1)
            funcstr += format_line('pbuf[%d] = pbuf[%d] & 0x%x;'%(cidx,cidx, cnum), tabs + 2)
            funcstr += format_line('}', tabs + 1)

    # now we should filled the number
    for i in range(len(sbyte)):
        cnum = get_bit(sbyte[i], clbits[i])
        funcstr += format_line('',tabs+1)
        funcstr += format_debug_line('0x%x = 0x%x & 0x%x'%(sbyte[i],curnum), tabs + 1, debug)
        funcstr += format_line('if (size > %d){'%(i), tabs + 1)
        funcstr += format_line('pbuf[%d] = pbuf[%d] | 0x%x;'%(i,i,cnum), tabs + 2)
        funcstr += format_line('}',tabs + 1)

    funcstr += format_line('', tabs + 1)
    funcstr += format_line('return size;', tabs + 1)
    funcstr += format_line('}', tabs)
    return funcstr,funcname


def format_bytes_xor_function(sbyte,abyte,abytefunc,bbyte,bbytefunc,nameprefix='prefix', namelen=10, numturns=30, tabs=0,debug=0):
    assert(len(sbyte) == len(abyte))
    assert(len(abyte) == len(bbyte))
    funcname = '%s_%s'%(nameprefix,get_random_name(namelen))
    bname = '%s_%s'%(nameprefix, get_random_name(namelen))
    retname = '%s_%s'%(nameprefix, get_random_name(namelen))
    funcstr = ''
    funcstr += format_line('int %s(unsigned char* pbuf, int size)'%(funcname),tabs)
    funcstr += format_line('{', tabs)
    funcstr += format_debug_line('variable:nameprefix %s variable:namelen %d variable:numturns %d'%(nameprefix,namelen,numturns), tabs + 1, debug)
    if len(sbyte) >= 2 and sbyte[-1] == 0 and sbyte[-2] == 0:
        funcstr += format_debug_line('var string:%s'%(uniints_to_string(sbyte)), tabs + 1, debug)
    else:
        funcstr += format_debug_line('var string:%s'%(ints_to_string(sbyte)), tabs + 1, debug)
    funcstr += format_line('unsigned char %s[%d];'%(bname, len(sbyte)), tabs + 1)
    funcstr += format_line('int ret;', tabs + 1)

    funcstr += format_line('', tabs + 1)
    funcstr += format_line('ret = %s(pbuf,size);'%(abytefunc), tabs + 1)
    funcstr += format_line('if ( ret < 0) {' , tabs + 1)
    funcstr += format_line('return ret;', tabs + 2)
    funcstr += format_line('}', tabs + 1)

    funcstr += format_line('', tabs + 1)
    funcstr += format_line('ret = %s(%s,%d);'%(bbytefunc, bname, len(sbyte)), tabs + 1)
    funcstr += format_line('if ( ret < 0) {' , tabs + 1)
    funcstr += format_line('return ret;', tabs + 2)
    funcstr += format_line('}', tabs + 1)

    # now to give the value
    for in in range(numturns):
        cidx = random.randint(0, len(sbyte) - 1)
        didx = random.randint(0, len(sbyte) - 1)
        hdl = random.randint(0, 5)
        funcstr += format_line('', tabs + 1)
        if hdl == 0:
            # to make abyte[cidx] = abyte[cidx] & bbyte[didx]
            funcstr += format_debug_line('abyte[%d] = abyte[%d] & bbyte[%d]'%(cidx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x & 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] & bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('pbuf[%d] = pbuf[%d] & %s[%d];'%(cidx, cidx, bname, didx), tabs + 2)
            funcstr += format_line('}', tabs + 1)
            abyte[cidx] = abyte[cidx] & bbyte[didx]
        elif hdl == 1:
            # to make abyte[cidx] = abyte[cidx] | bbyte[didx]
            funcstr += format_debug_line('abyte[%d] = abyte[%d] | bbyte[%d]'%(cidx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x | 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] | bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('pbuf[%d] = pbuf[%d] | %s[%d];'%(cidx, cidx, bname, didx), tabs + 2)
            funcstr += format_line('}', tabs + 1)
            abyte[cidx] = abyte[cidx] | bbyte[didx]
        elif hdl == 2:
            # to make bbyte[didx] = abyte[cidx] & bbyte[didx]
            funcstr += format_debug_line('bbyte[%d] = abyte[%d] & bbyte[%d]'%(didx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x & 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] & bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('%s[%d] = pbuf[%d] & %s[%d];'%(bname,didx, cidx, bname, didx), tabs + 2)
            funcstr += format_line('}', tabs + 1)
            bbyte[didx] = abyte[cidx] & bbyte[didx]
        elif hdl == 3:
            # to make bbyte[didx] = abyte[cidx] | bbyte[didx]
            funcstr += format_debug_line('bbyte[%d] = abyte[%d] | bbyte[%d]'%(didx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x & 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] | bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('%s[%d] = pbuf[%d] | %s[%d];'%(bname,didx, cidx, bname, didx), tabs + 2)
            funcstr += format_line('}', tabs + 1)
            bbyte[didx] = abyte[cidx] | bbyte[didx]
        elif hdl == 4:
            # to make abyte[cidx] = abyte[cidx] ^ bbyte[didx]
            funcstr += format_debug_line('abyte[%d] = abyte[%d] ^ bbyte[%d]'%(cidx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x ^ 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] ^ bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('pbuf[%d] = pbuf[%d] ^ %s[%d];'%(cidx, cidx, bname, didx), tabs + 2)
            funcstr += format_line('}', tabs + 1)
            abyte[cidx] = abyte[cidx] ^ bbyte[didx]
        elif hdl == 5:
            # to make bbyte[didx] = abyte[cidx] ^ bbyte[didx]
            funcstr += format_debug_line('bbyte[%d] = abyte[%d] ^ bbyte[%d]'%(didx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x ^ 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] ^ bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('%s[%d] = pbuf[%d] ^ %s[%d];'%(bname,didx, cidx, bname, didx), tabs + 2)
            funcstr += format_line('}', tabs + 1)
            bbyte[didx] = abyte[cidx] ^ bbyte[didx]
        else:
            raise Exception('unexpected random valud [%d]'%(hdl))

    for i in range(len(sbyte)):
        hdl = random.randint(0, 1)
        funcstr += format_line('',tabs + 1)
        if hdl == 0:
            cnum = sbyte[i] ^ abyte[i]
            funcstr += format_debug_line('pbuf[%d] = (abyte[%d])0x%x ^ 0x%x'%(i,i,abyte[i], cnum),tabs + 1, debug)
            funcstr += format_line('if (%d < size){'%(i), tabs + 1)
            funcstr += format_line('pbuf[%d] = pbuf[%d] ^ 0x%x;'%(i,i,cnum),tabs + 2)
            funcstr += format_line('',tabs + 1)
        elif hdl == 1:
            cnum = sbyte[i] ^ bbyte[i]
            funcstr += format_debug_line('pbuf[%d] = (bbyte[%d])0x%x ^ 0x%x'%(i,i,bbyte[i], cnum),tabs + 1, debug)
            funcstr += format_line('if (%d < size){'%(i), tabs + 1)
            funcstr += format_line('pbuf[%d] = %s[%d] ^ 0x%x;'%(i,bname,i,cnum),tabs + 2)
            funcstr += format_line('',tabs + 1)
        else:
            raise Exception('unexpected random valud [%d]'%(hdl))

    funcstr += format_line('',tabs + 1)
    funcstr += format_line('return size;', tabs + 1)
    funcstr += format_line('}',tabs)
    return funcstr, funcname




class MixedString(object):

    def __get_bytes(self,size):
        rb = []
        for i in range(size):
            rb.append(random.randint(0,255))
        return rb

    def __get_func(self,sbyte):
        return format_bytes_set_function(sbyte,self.__cfg.prefix, \
                random.randint(self.__cfg.namemin,self.__cfg.namemax), \
                random.randint(self.__cfg.funcmin,self.__cfg.funcmax), \
                0,self.__cfg.debug)

    def __init__(self,sbyte,cfg):
        self.__sbyte = sbyte
        self.__iswide = False
        self.__cfg = cfg
        if len(sbyte) >= 2 and sbyte[-1] == 0 and sbyte[-2] == 0:
            self.__iswide = True
        self.__abyte = self.__get_bytes(len(sbyte))
        self.__bbyte = self.__get_bytes(len(sbyte))
        self.__afuncstr ,self.__afuncname = self.__get_func(self.__abyte)
        self.__bfuncstr , self.__bfuncname = self.__get_func(self.__bbyte)
        self.__sfuncstr , self.__sfuncname = format_bytes_xor_function(sbyte, \
                self.__abyte, self.__afuncname, \
                self.__bbyte, self.__bfuncname, \
                self.__cfg.prefix, \
                random.randint(self.__cfg.namemin,self.__cfg.namemax), \
                random.randint(self.__cfg.funcmin,self.__cfg.funcmax), \
                0,self.__cfg.debug)
        return

    def __get_hash(self,sbyte):
        cval = 0
        for s in sbyte:
            cval += s
            # 113 is the prime number
            cval *= 113
            # 104729 is the prime number
            cval = cval % 104729
        return cval

    def __getattr__(self,keyname):
        if keyname == 'sbyte':
            return self.__sbyte
        elif keyname == 'iswide':
            return self.__iswide
        elif keyname == 'afunc':
            return self.__afuncstr
        elif keyname == 'bfunc':
            return self.__bfuncstr
        elif keyname == 'func':
            return self.__sfuncstr
        elif keyname == 'funcname':
            return self.__sfuncname
        elif keyname == 'hash':
            return self.__get_hash(self.__sbyte)
        else:
            if keyname in self.__dict__.keys():
                return self.__dict__[keyname]
            else:
                raise Exception('not support [%s]'%(keyname))

    def hash_number(self,sbyte):
        return self.__get_hash(sbyte)


GL_INIT_ATTR={
    'prefix' : 'prefix',
    'namemin' : 5,
    'namemax' : 20,
    'funcmin' : 3,
    'funcmax' : 30,
    'xorsize' : 16,
    'maxround': 32,
    'debug' : 0,
    'noline' : 0
}

GL_DEFAULT_ATTR={}

class COBAttr(object):
    def __trans_number(self,vstr):
        retv = vstr
        if self.__float_expr.match(vstr):
            retv = float(vstr)
        elif self.__dec_expr.match(vstr):
            retv = int(vstr)
        return retv

    def __prepare_attr(self,attrs=None):
        v = attrs
        if attrs is not None and isinstance(attrs, str):
            sarr = re.split(',', attrs)
            v = dict()
            for c in sarr:
                varr = re.split('=', c)
                if len(varr) > 1:
                    v[varr[0]] = self.__trans_number(varr[1])
                else:
                    v[varr[0]] = None
        elif attrs is not None and not isinstance(attrs, dict):
            raise Exception('attrs [%s] not valid type'%(attrs))
        if v is not None:
            for k in v.keys():
                if k not in self.__obj.keys():
                    self.__obj[k] = v[k]
        return

    def __check_value(self):
        if self.namemin > self.namemax:
            raise Exception('namemin [%d] > namemax [%d]'%(self.namemin,self.namemax))
        if self.xorsize <= 0:
            raise Exception('xorsize [%s] < 0'%(self.xorsize))

        if self.maxround <= 0:
            raise Exception('maxround [%d] < 0'%(self.maxround))

        if len(self.prefix) == 0:
            raise Exception('prefix [] empty')
        logging.info('funcmin [%s] funcmax [%s]'%(self.funcmin,self.funcmax))
        if self.funcmin > self.funcmax or self.funcmin < 0 or self.funcmax <= 0:
            raise Exception('funcmin [%d] or funcmax [%d] not valid'%(self.funcmin, self.funcmax))
        return

    def format_values(self):
        global GL_INIT_ATTR
        s = ''
        for k in GL_INIT_ATTR.keys():
            if len(s) > 0:
                s += ','
            s += '%s=%s'%(k,GL_INIT_ATTR[k])
        return s


    def __init__(self,attrs=None,news=None):
        global GL_DEFAULT_ATTR
        self.__obj = dict()
        self.__dec_expr = re.compile('^[-+]?[0-9]+$')
        self.__float_expr = re.compile('^[-+]?[0-9]\.[0-9]+$')
        self.__prepare_attr(attrs)
        self.__prepare_attr(news)
        self.__prepare_attr(GL_DEFAULT_ATTR)
        self.__check_value()
        return

    def __getattr__(self,k):
        if k in self.__obj.keys():
            return self.__obj[k]
        return None


class CompoundAttr(COBAttr):
    def __inc_prefix(self):
        self.__basic_inc += 1
        s = '%s_%d'%(self.__basic_prefix,self.__basic_inc)
        logging.info('prefix [%s]'%(s))
        return s

    def __init__(self,attrs=None):
        self.__basiccfg = COBAttr(attrs,None)
        self.__filecfg = None
        self.__basic_prefix = '%s'%(self.__basiccfg.prefix)
        self.__basic_inc = 0
        d = dict()
        d['prefix'] = self.__inc_prefix()
        self.__basiccfg = COBAttr(attrs,d)
        return

    def __getattr__(self,k):
        return self.__basiccfg.__getattr__(k)

    def load_file(self,f):
        retval = False
        try:
            s = read_file(f)
            # now to pass 
            d = json.loads(s)
            self.__filecfg = Utf8Encode(d).get_val()
            self.__filecfg = d
            retval = True
        except:
            pass
        return retval

    def get_file_config(self,name):
        retval = None
        logging.info('id <%s>'%(self))
        if self.__filecfg is not None and \
            name in self.__filecfg.keys():
            retval = COBAttr(self.__filecfg[name],None)
        elif isinstance(name,str):
            retval = COBAttr(name,None)
        else:
            retval = COBAttr(None,None)
        return retval

    def load_new_prefix(self):
        self.__inc_prefix()
        d = dict()
        d['prefix'] = '%s_%d'%(self.__basic_prefix,self.__basic_inc)
        s = self.__basiccfg.format_values()
        self.__basiccfg = COBAttr(s,d)
        return self

    def get_count(self):
        return self.__basic_inc


class COBFile(object):
    def __get_filter_expr_not_defined(self,l,expr1):
        m = expr1.findall(l)
        if m is not None and len(m) > 0:
            filtered = False
            for expr in self.__define_expr:
                m = expr.findall(l)
                if m is not None and len(m) > 0:
                    logging.info('[match] %s'%(m[0]))
                    filtered = True
                    break
            if not filtered:
                return True
        return False

    def __should_expand_ob_code(self):
        self.__cur_line = 0
        for l in self.__in_lines:
            self.__cur_line += 1
            if self.__get_filter_expr_not_defined(l,self.__ob_code_expr):
                return True
            if self.__get_filter_expr_not_defined(l, self.__ob_code_spec_expr):
                return True
        return False

    def __prepare_config(self):
        self.__cur_line = 0
        for l in self.__in_lines:
            self.__cur_line += 1
            if self.__get_filter_expr_not_defined(l, self.__ob_config_expr):
                m = self.__ob_config_expr.findall(l)
                assert(len(m) == 1)
                assert(len(m[0]) > 1)
                sbyte = string_to_ints(m[0][1])
                params , lbyte = parse_param(sbyte)
                if len(params) != 1 :
                    raise Exception('[%d][%s]no params in OB_CONFIG'%(self.__cur_line, l))
                sbyte = string_to_ints(params[0])
                rbyte , lbyte = parse_raw_string(sbyte)
                self.__cfg = CompoundAttr(ints_to_string(rbyte))
            if self.__get_filter_expr_not_defined(l, self.__ob_insert_expr):
                self.__insert_line = self.__cur_line
        return

    def __prepare_mixed_str_funcs_inner(self,l,cfg,before,after,sbyte):
        return

    def __prepare_mixed_str_funcs(self,l):
        cfg , params, before, after = self.__get_variables(l, self.__ob_mixed_str_expr)
        assert(len(params) == 1)
        sbyte = parse_raw_string(params[0])
        self.__prepare_mixed_str_funcs_inner(l, cfg, before, after, sbyte)
        return

    def __prepare_mixed_str_spec_funcs(self,l):
        cfg ,params, before , after = self.__get_spec_config_variables(l, self.__ob_mixed_str_spec_expr)
        assert(len(params) == 1)
        sbyte = parse_raw_string(params[0])
        self.__prepare_mixed_str_funcs_inner(l, cfg, before, after, sbyte)
        return

    def __prepare_mixed_wstr_funcs_inner(self,l,cfg,before,after,sbyte):
        return

    def __prepare_mixed_wstr_funcs(self,l):
        cfg , params, before , after = self.__get_variables(l, self.__ob_mixed_wstr_expr)
        assert(len(params) == 1)
        cbyte = string_to_ints(params[0])
        assert(len(cbyte) >= 3)
        assert(cbyte[0] == ord('L'))
        cs = ints_to_string(cbyte[1:])
        rs = parse_raw_string(cs)
        sbyte = string_to_uniints(rs)
        self.__prepare_mixed_wstr_funcs_inner(l, cfg, before, after, sbyte)
        return

    def __prepare_mixed_wstr_spec_funcs(self,l):
        cfg ,params , before , after = self.__get_spec_config_variables(l, self.__ob_mixed_wstr_spec_expr)
        assert(len(params) == 1)
        cbyte = string_to_ints(params[0])
        assert(len(cbyte) >= 3)
        assert(cbyte[0] == ord('L'))
        cs = ints_to_string(cbyte[1:])
        rs = parse_raw_string(cs)
        sbyte = string_to_uniints(rs)
        self.__prepare_mixed_wstr_funcs_inner(l, cfg, before, after, sbyte)
        return

    def __prepare_mixstr(self):
        self.__cur_line = 0
        for l in self.__in_lines:
            self.__cur_line += 1
            if self.__get_filter_expr_not_defined(l, self.__ob_mixed_str_expr):
                self.__prepare_mixed_str_funcs(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_mixed_str_spec_expr):
                self.__prepare_mixed_str_spec_funcs(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_mixed_wstr_expr):
                self.__prepare_mixed_wstr_funcs(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_mixed_wstr_spec_expr):
                self.__prepare_mixed_wstr_spec_funcs(l)

        return

    def __prepare(self):
        self.__prepare_config()
        self.__prepare_mixstr()
        if self.__should_expand_ob_code():
            funcstr, funcname = format_xor_encode_function(self.__cfg.prefix,random.randint(self.__cfg.namemin,self.__cfg.namemax),0, self.__cfg.debug)
            self.__xor_enc_functions[funcname] = funcstr
            funcstr, funcname = format_xor_decode_function(self.__cfg.prefix, random.randint(self.__cfg.namemin,self.__cfg.namemax),0, self.__cfg.debug)
            self.__xor_dec_functions[funcname] = funcstr


            cnt = random.randint(self.__cfg.funcmin, self.__cfg.funcmax)
            idx = 0
            while idx < cnt:
                curdict = dict()
                xorcode = get_xor_code(self.__cfg.xorsize)
                funcstr,funcname = format_key_ctr_function(xorcode,self.__cfg.prefix,random.randint(self.__cfg.namemin,self.__cfg.namemax),self.__cfg.maxround,0,self.__cfg.debug)
                curdict['code'] = xorcode
                curdict['ctr']  = funcstr
                curdict['ctr_name'] = funcname                
                funcstr,funcname = format_key_dtr_function(xorcode,self.__cfg.prefix,random.randint(self.__cfg.namemin,self.__cfg.namemax),self.__cfg.maxround,0,self.__cfg.debug)
                curdict['dtr'] = funcstr
                curdict['dtr_name'] = funcname
                self.__xor_codes.append(curdict)                
                idx = idx + 1
        return
        
    def __append_define_expr(self,exprstr):
        expr = re.compile(exprstr)
        self.__define_expr.append(expr)
        return

    def __init__(self,sfile,dfile=None,cfg=None):
        self.__xor_enc_functions = dict()
        self.__xor_dec_functions = dict()
        self.__var_replace = dict()
        self.__var_decl_replace = dict()
        self.__func_replace = dict()
        self.__xor_codes = []
        self.__srcfile = sfile
        self.__dstfile = dfile
        self.__cfg = COBAttr()
        self.__insert_line = -1
        if cfg is not None:
            self.__cfg = cfg

        # we change the ( to \x28 ) \x29 for it will give error on shell in make file
        self.__ob_code_expr = re.compile('\s+(OB_CODE\s*(\\\x28.*))$')
        self.__ob_code_spec_expr = re.compile('\s+(OB_CODE_SPEC\s*(\\\x28.*))$')
        self.__ob_func_expr = re.compile('\s+OB_FUNC\s+([a-zA-Z0-9_]+)\s*\\\x28')
        self.__ob_func_spec_expr = re.compile('\s+(OB_FUNC_SPEC\s*(\\\x28.*)).*$')
        self.__ob_var_expr = re.compile('[\\*\\\x28\\\x29\s]+(OB_VAR\s*(\\\x28.*))$')
        self.__ob_var_spec_expr = re.compile('[\\*\\\x28\\\x29\s]+(OB_VAR_SPEC\s*(\\\x28.*))$')
        self.__ob_decl_var_expr = re.compile('[\\*\\\x28\\\x29\s]+(OB_DECL_VAR\s*(\\\x28.*))$')
        self.__ob_decl_var_spec_expr = re.compile('[\\*\\\x28\\\x29\s]+(OB_DECL_VAR_SPEC\s*(\\\x28.*))$')
        self.__ob_insert_expr = re.compile('^[\s]*(OB_INSERT\s*\\\x28\\\x29)')
        self.__ob_constant_str_expr = re.compile('.*(OB_CONSTANT_STR\s*(\\\x28.*))$')
        self.__ob_constant_wstr_expr = re.compile('.*(OB_CONSTANT_WSTR\s*(\\\x28.*))$')
        self.__ob_constant_str_spec_expr = re.compile('.*(OB_CONSTANT_STR_SPEC\s*(\\\x28.*))$')
        self.__ob_constant_wstr_spec_expr = re.compile('.*(OB_CONSTANT_WSTR_SPEC\s*(\\\x28.*))$')
        self.__ob_mixed_str_expr = re.compile('.*(OB_MIXED_STR\s*(\\\x28.*))$')
        self.__ob_mixed_str_spec_expr = re.compile('.*(OB_MIXED_STR_SPEC\s*(\\\x28.*))$')
        self.__ob_mixed_wstr_expr = re.compile('.*(OB_MIXED_WSTR\s*(\\\x28.*))$')
        self.__ob_mixed_wstr_spec_expr = re.compile('.*(OB_MIXED_WSTR_SPEC\s*(\\\x28.*))$')

        self.__ob_config_expr = re.compile('^\W*(OB_CONFIG(\\\x28.*))$')


        self.__quote_expr = re.compile('"([^"]*)"')
        self.__include_expr = re.compile('^\s*\#\s*include\s+["<]')

        self.__define_expr = []
        self.__append_define_expr('^\s*\#\s*define\s+')
        self.__append_define_expr('^\s*\#\s*undef\s+')
        self.__append_define_expr('^\s*\#\s*if\s+')
        self.__append_define_expr('^\s*\#\s*ifdef\s+')
        self.__append_define_expr('^\s*\#\s*ifndef\s+')
        self.__append_define_expr('^\s*\#\s*endif\s+')
        self.__append_define_expr('^\s*\#\s*else\s+')
        self.__append_define_expr('^\s*\#\s*elif\s+')
        self.__in_lines = get_file_lines(sfile)
        self.__prepare()
        return

    def __get_variables(self,l,expr1):
        variables = expr1.findall(l)
        # we do this on the increment
        assert(len(variables) == 1)
        assert(len(variables[0]) > 1)
        cfgattr = self.__cfg
        sbyte = string_to_ints(variables[0][1])
        params, lbyte = parse_param(sbyte)
        before = l.replace(variables[0][0],'',1)
        return cfgattr,params,before,ints_to_string(lbyte)

    def __get_spec_config_variables(self,l,expr1):
        leftvars = []
        cfgattr = None
        variables = expr1.findall(l)
        assert(len(variables) == 1)
        assert(len(variables[0]) > 1)
        sbyte = string_to_ints(variables[0][1])
        params,lbyte = parse_param(sbyte)
        if len(params) < 1:
            raise Exception('at [%d] line [%s] not valid for specific'%(self.__cur_line,l))
        after = ints_to_string(lbyte)
        cfgstr,lbyte = parse_raw_string(string_to_ints(params[0]))
        cfgstr = ints_to_string(cfgstr)
        logging.info('cfgstr [%s]'%(cfgstr))
        cfgattr = self.__cfg.get_file_config(cfgstr)
        retparams = []
        if len(params) > 1:
            retparams = params[1:]
        before = l.replace(variables[0][0],'',1)
        return cfgattr,retparams, before,after


    def __format_ob_code_inner(self,varsarr,cfg,tabs=0):
        s = ''
        assert(len(varsarr) > 0)
        vcnames = []
        ptrnames = []
        varcodes = dict()
        for i in varsarr:
            vcnames.append('%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax))))
            ptrnames.append('%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax))))
        s += format_line('do {',tabs)
        s += format_debug_line('variables:prefix %s variables:namemax %d'%(cfg.prefix,random.randint(cfg.namemin,cfg.namemax)), tabs + 1 , cfg.debug)
        for i in range(len(varsarr)):
            s += format_line('void* %s = (void*)&(%s);'%(ptrnames[i], varsarr[i]), tabs + 1)
            s += format_line('unsigned long long %s = (unsigned long long)((OB_ADDR)(%s));'%(vcnames[i], ptrnames[i]), tabs+1)
        bufname = '%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        sizename = '%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        lenname = '%s_%s'%(cfg.prefix, get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        s += format_line('unsigned char %s[%d];'%(bufname,self.__cfg.xorsize),tabs + 1)
        s += format_line('int %s=%d;'%(sizename,self.__cfg.xorsize), tabs + 1)
        s += format_line('int %s;'%(lenname),tabs + 1)
        s += format_line('',tabs + 1)
        for k in self.__xor_enc_functions.keys():
            encname = k
            break
        pair_dict = []
        ctimes = random.randint(cfg.funcmin, cfg.funcmax)
        for i in range(ctimes):
            curi = random.randint(0, len(self.__xor_codes)-1)
            curxor = self.__xor_codes[curi]
            s += format_line('', tabs + 1)
            s += format_line('%s = %s(%s,%s);'%(lenname,curxor['ctr_name'],bufname,sizename), tabs+1)
            curj = random.randint(0, len(varsarr) - 1)
            s += format_line('%s(((unsigned char*)&%s),sizeof(%s),%s,%s);'%(encname, vcnames[curj], vcnames[curj], bufname,lenname), tabs+1)
            s += format_line('%s(%s,%s);'%(curxor['dtr_name'], bufname,lenname), tabs + 1)
            d = dict()
            d['xor_idx'] = curi
            d['var_idx'] = curj
            pair_dict.append(d)

        s += format_debug_line('format [%d] times'%(ctimes),tabs + 1,cfg.debug)

        for k in self.__xor_dec_functions.keys():
            decname = k
            break
        while len(pair_dict)>0:
            curi = random.randint(0, len(pair_dict)-1)
            d = pair_dict[curi]
            xor_idx = d['xor_idx']
            var_idx = d['var_idx']
            del pair_dict[curi]
            curxor = self.__xor_codes[xor_idx]
            s += format_line('',tabs + 1)
            s += format_line('%s = %s(%s,%s);'%(lenname,curxor['ctr_name'],bufname, sizename), tabs + 1)
            s += format_line('%s(((unsigned char*)&%s),sizeof(%s), %s,%s);'%(decname,vcnames[var_idx], vcnames[var_idx], bufname,lenname), tabs + 1)
            s += format_line('%s(%s,%s);'%(curxor['dtr_name'], bufname, lenname), tabs + 1)

        s += format_line('',tabs+1)
        for i in range(len(varsarr)):
            s += format_line('%s = (void*)((OB_ADDR)(%s));'%(ptrnames[i],vcnames[i]), tabs + 1)

        s += format_line('',tabs+1)
        for i in range(len(varsarr)):
            s += format_line('%s = (OB_TYPEOF(%s)) *(((OB_TYPEOF(%s)*)(%s)));'%(varsarr[i], varsarr[i], varsarr[i], ptrnames[i]), tabs+ 1)
        s += format_line('} while(0);',tabs)        
        if cfg.noline == 0:
            s += format_line('#line %d "%s"'%(self.__cur_line+1,quote_string(self.__srcfile)),0)
        return s

    def __output_ob_header_comment(self,l,cfg,tabs):
        s = ''
        if cfg.noline == 0:
            s += format_line('/*#lineno:%d*/'%(self.__cur_line), tabs)
            s += format_line('/*[%s]*/'%(format_comment_line(l)), tabs)
        return s

    def __format_ob_code_spec(self,l):
        s = ''
        curcfg, cvars, before, after = self.__get_spec_config_variables(l,self.__ob_code_spec_expr)
        if len(cvars) == 0:
            raise Exception('[%d][%s] not valid code'%(self.__cur_line,l))
        tabs = count_tabs(l)
        s += format_line('',tabs)
        s += self.__output_ob_header_comment(l,curcfg,tabs)
        s += self.__format_ob_code_inner(cvars,curcfg, tabs)
        return s

    def __format_ob_code(self,l):
        s = ''
        cfg , varsarr, before,after = self.__get_variables(l, self.__ob_code_expr)
        tabs = count_tabs(l)
        s += format_line('',tabs)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_code_inner(varsarr, cfg,tabs)
        return s

    def __format_ob_func_inner(self,l,funcname,cfg,tabs,isspec):
        s = ''
        replacename = '%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        s += format_line('#define %s %s'%(funcname, replacename), tabs)
        s += format_line('#line %d "%s"'%(self.__cur_line,quote_string(self.__srcfile)),0)
        s += format_line('%s'%(l), 0)
        self.__func_replace[funcname] = replacename
        return s

    def __format_ob_func(self,l):
        s = ''
        m = self.__ob_func_expr.findall(l)
        funcname = m[0]
        tabs = count_tabs(l)
        cfg = self.__cfg
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_func_inner(l,funcname,cfg,tabs,False)
        return s

    def __format_ob_func_spec(self,l):
        s = ''
        m = self.__ob_func_spec_expr.findall(l)
        assert(m is not None)
        assert(len(m) == 1)
        assert(len(m[0]) > 1)
        sbyte = string_to_ints(m[0][1])
        params , lbyte = parse_param(sbyte)
        if len(params) != 1:
            raise Exception('[%d][%s] not valid OB_FUNC_SPEC'%(self.__cur_line,l))
        cfgstr = params[0]
        # now to get the left
        funcbyte = []
        start = 0
        idx = 0
        while idx < len(lbyte):
            cbyte = lbyte[idx]
            idx += 1
            if  start == 0:
                if is_space_char(cbyte):
                    continue
                else:
                    if is_normal_char(cbyte):
                        if is_decimal_char(cbyte):
                            raise Exception('[%d][%s]function name [%s] not valid'%(self.__cur_line,l,ints_to_string(lbyte)))
                        start += 1
                        funcbyte.append(cbyte)
                    else:
                        raise Exception('[%d][%s]not valid function name [%s]'%(self.__cur_line,l,ints_to_string(lbyte)))
            else:
                if is_normal_char(cbyte):
                    funcbyte.append(cbyte)
                else:
                    break
        funcname = ints_to_string(funcbyte)
        sbyte = string_to_ints(cfgstr)
        cfgbyte , lbyte = parse_raw_string(sbyte)
        cfgstr = ints_to_string(cfgbyte)
        cfg = self.__cfg.get_file_config(cfgstr)
        tabs = count_tabs(l)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_func_inner(l, funcname, cfg, tabs,True)
        return s

    def __format_ob_var_inner(self,l,cfg,leftvars,isspec,tabs):
        s = ''
        if len(leftvars) != 1:
            raise Exception('[%d][%s] not valid '%(self.__cur_line,l))
        replacename = '%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        #if isspec:
        #    s += format_line('#undef OB_VAR_SPEC',tabs)
        #    s += format_line('#define OB_VAR_SPEC(a,x) %s'%(replacename), tabs)            
        #else:
        #    s += format_line('#undef OB_VAR', tabs)
        #    s += format_line('#define OB_VAR(x) %s'%(replacename), tabs)
        s += format_line('#define %s %s'%(leftvars[0],replacename), tabs)
        if cfg.noline == 0:
            s += format_line('#line %d "%s"'%(self.__cur_line,quote_string(self.__srcfile)),0)
        s += format_line('%s'%(l),0)
        self.__var_replace[leftvars[0]] = replacename
        return s

    def __format_ob_var_spec(self,l):
        s = ''
        cfg, leftvars, before,after = self.__get_spec_config_variables(l, self.__ob_var_spec_expr)
        tabs = count_tabs(l)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_var_inner(l,cfg,leftvars,True,tabs)
        return s

    def __format_ob_var(self,l):
        s = ''
        cfg ,leftvars, before, after = self.__get_variables(l, self.__ob_var_expr)
        tabs = count_tabs(l)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_var_inner(l,cfg,leftvars,False,tabs)
        return s

    def __format_ob_decl_var_inner(self,l,cfg,leftvars,isspec,tabs):
        s = ''
        if len(leftvars) != 1:
            raise Exception('[%d][%s] not valid '%(self.__cur_line,l))
        replacename = '%s_%s'%(cfg.prefix,get_random_name(random.randint(cfg.namemin,cfg.namemax)))
        #if isspec:
        #    s += format_line('#undef OB_DECL_VAR_SPEC',tabs)
        #    s += format_line('#define OB_DECL_VAR_SPEC(a,x) %s'%(replacename), tabs)
        #else:
        #    s += format_line('#undef OB_DECL_VAR', tabs)
        #    s += format_line('#define OB_DECL_VAR(x) %s'%(replacename), tabs)
        s += format_line('#define %s %s'%(leftvars[0],replacename),tabs)
        if cfg.noline == 0:
            s += format_line('#line %d "%s"'%(self.__cur_line,quote_string(self.__srcfile)),0)
        s += format_line('%s'%(l),0)
        self.__var_decl_replace[leftvars[0]] = replacename
        return s


    def __format_ob_decl_var(self,l):
        s = ''
        cfg, leftvars, before, after = self.__get_variables(l, self.__ob_decl_var_expr)
        tabs = count_tabs(l)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_decl_var_inner(l,cfg,leftvars,False,tabs)
        return s

    def __format_ob_decl_var_spec(self,l):
        s = ''
        cfg, leftvars, before ,after = self.__get_spec_config_variables(l, self.__ob_decl_var_spec_expr)
        tabs = count_tabs(l)
        s += self.__output_ob_header_comment(l, cfg, tabs)
        s += self.__format_ob_decl_var_inner(l,cfg,leftvars,True,tabs)
        return s

    def __format_ob_constant_str_inner(self,l,cfg,before,after,tabs):
        s = ''
        s += format_line('/*[%s]*/'%(format_comment_line(l)),tabs)
        if cfg.noline == 0:
            s += format_line('#line %d "%s"'%(self.__cur_line,quote_string(self.__srcfile)),0)        
        s += '%s"[%%s:%%d]\\n",__FILE__,__LINE__%s\n'%(before,after)
        return s

    def __format_ob_constant_str(self,l):
        s = ''
        cfg , leftvars, before , after = self.__get_variables(l, self.__ob_constant_str_expr)
        tabs = count_tabs(l)
        s += self.__format_ob_constant_str_inner(l,cfg,before,after,tabs)
        return s

    def __format_ob_constant_str_spec(self,l):
        s = ''
        cfg , leftvars, before , after = self.__get_spec_config_variables(l, self.__ob_constant_str_spec_expr)
        tabs = count_tabs(l)
        s += self.__format_ob_constant_str_inner(l,cfg,before,after,tabs)
        return s


    def __format_ob_constant_wstr_inner(self,l,cfg,before,after,tabs):
        s = ''
        s += format_line('/*[%s]*/'%(format_comment_line(l)),tabs)
        if cfg.noline == 0:
            s += format_line('#line %d "%s"'%(self.__cur_line,quote_string(self.__srcfile)),0)        
        s += '%sL"[%%hs:%%d]\\n",__FILE__,__LINE__%s\n'%(before,after)
        return s


    def __format_ob_constant_wstr(self,l):
        s = ''
        cfg , leftvars , before , after = self.__get_variables(l, self.__ob_constant_wstr_expr)
        tabs = count_tabs(l)
        s += self.__format_ob_constant_wstr_inner(l,cfg,before,after,tabs)
        return s

    def __format_ob_constant_wstr_spec(self,l):
        s = ''
        cfg , leftvars , before , after = self.__get_spec_config_variables(l, self.__ob_constant_wstr_spec_expr)
        tabs = count_tabs(l)
        s += self.__format_ob_constant_wstr_inner(l,cfg,before,after,tabs)
        return s


    def __output_pre_functions(self,cfg):
        rets = ''
        # now to put the get include function
        for k in self.__xor_enc_functions.keys():
            rets += format_line('',0)
            rets += format_line('',0)
            rets += self.__xor_enc_functions[k]

        for k in self.__xor_dec_functions.keys():
            rets += format_line('',0)
            rets += format_line('',0)
            rets += self.__xor_dec_functions[k]

        # now we should give the include
        idx = 0
        while idx < len(self.__xor_codes):
            rets += format_line('',0)
            rets += format_line('',0)
            curdict = self.__xor_codes[idx]
            rets += curdict['ctr']
            rets += format_line('',0)
            rets += format_line('',0)
            rets += curdict['dtr']
            idx = idx + 1

        if idx > 0:
            rets += format_line('',0)
            rets += format_line('',0)
        if len(rets) > 0 and cfg.noline == 0:
            rets += format_line('#line %d "%s"'%(self.__cur_line,quote_string(self.__srcfile)),0)

        return rets


    def out_str(self):
        rets = ''
        self.__cur_line = 0
        startinclude = 0
        if self.__insert_line >= 0:
            startinclude = 2
        for l in self.__in_lines:
            self.__cur_line += 1
            #logging.info('[%d][%s]'%(self.__cur_line, l))
            if  startinclude == 0:
                m = self.__include_expr.findall(l)
                rets += format_line('%s'%(l),0)
                if m is not None and len(m) > 0:
                    startinclude = 1
                continue
            elif startinclude == 1:
                ls = l.rstrip(' \t')
                ls = ls.strip(' \t')
                if len(ls) == 0:
                    rets += self.__output_pre_functions(self.__cfg)
                    startinclude = 2
                else:
                    rets += format_line('%s'%(l),0)
                    continue

            if self.__insert_line >= 0 and self.__insert_line == self.__cur_line:
                rets += self.__output_pre_functions(self.__cfg)
                rets += format_line('%s'%(l), 0)
                continue

            if self.__get_filter_expr_not_defined(l, self.__ob_code_expr):
                logging.info('')
                rets += self.__format_ob_code(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_code_spec_expr):
                logging.info('')
                rets += self.__format_ob_code_spec(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_func_expr):
                logging.info('')
                rets += self.__format_ob_func(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_func_spec_expr):
                logging.info('')
                rets += self.__format_ob_func_spec(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_var_expr):
                logging.info('')
                rets += self.__format_ob_var(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_var_spec_expr):
                logging.info('')
                rets += self.__format_ob_var_spec(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_decl_var_expr):
                logging.info('')
                rets += self.__format_ob_decl_var(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_decl_var_spec_expr):
                logging.info('')
                rets += self.__format_ob_decl_var_spec(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_constant_str_expr):
                logging.info('')
                rets += self.__format_ob_constant_str(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_constant_wstr_expr):
                logging.info('l [%s]'%(l))
                rets += self.__format_ob_constant_wstr(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_constant_str_spec_expr):
                logging.info('')
                rets += self.__format_ob_constant_str_spec(l)
            elif self.__get_filter_expr_not_defined(l, self.__ob_constant_wstr_spec_expr):
                logging.info('l [%s]'%(l))
                rets += self.__format_ob_constant_wstr_spec(l)
            else:
                rets += format_line('%s'%(l),0)
        return rets

    def get_replace_json(self):
        d = dict()
        encname = ''
        for k in self.__xor_enc_functions.keys():
            encname = k
            break
        d['encode_function'] = encname
        decname = ''
        for k in self.__xor_dec_functions.keys():
            decname = k
            break
        d['decode_function'] = decname
        d['xorcodes'] = []
        for k in self.__xor_codes:
            c = dict()
            c['ctr_name'] = k['ctr_name']
            c['dtr_name'] = k['dtr_name']
            c['code'] = k['code']
            d['xorcodes'].append(c)
        d['functions'] = self.__func_replace
        d['vars'] = self.__var_replace
        d['vars_decl'] = self.__var_decl_replace
        odict = dict()
        odict[self.__srcfile] = d
        return odict


class cobparam(object):
    def __init__(self,srcdir,dstdir,configfile=None):
        self.srcdir = srcdir
        self.dstdir = dstdir
        self.__handle_exprs = []
        self.__filter_exprs = []
        self.__handle_strs = []
        self.__filter_strs = []
        self.config=CompoundAttr()
        if configfile is not None:
            self.config.load_file(configfile)
        return

    def append_handle(self,instr):
        expr = re.compile(instr)
        self.__handle_exprs.append(expr)
        self.__handle_strs.append(instr)
        return

    def append_filter(self,instr):
        expr = re.compile(instr)
        self.__filter_exprs.append(expr)
        self.__filter_strs.append(instr)
        return

    def is_in_filter(self,sfile):
        news = '%r'%(self.srcdir)
        patstr = re.sub(news, '', sfile)
        if os.sep == '/':
            patsarr = re.split('/', patstr)
        elif os.sep == '\\':
            patsarr = re.split('\\\\', patstr)
        idx = 0
        while idx < len(self.__filter_exprs):
            c = self.__filter_exprs[idx]
            for cl in patsarr:
                if len(cl) > 0:
                    if c.match(cl):
                        #logging.info('patstr [%s] filted [%s]'%(patstr, self.__filter_strs[idx]))
                        return True
            idx = idx + 1
        return False

    def is_in_handle(self,sfile):
        news = '%r'%(self.srcdir)
        patstr = re.sub(news,'',sfile)
        idx = 0
        while idx < len(self.__handle_exprs):
            c = self.__handle_exprs[idx]
            m = c.findall(patstr)
            if m is not None and len(m) > 0:
                #logging.info('[%s] match [%s]'%(patstr, self.__handle_strs[idx]))
                return True
            idx = idx + 1
        return False


def make_dir_safe(ddir):
    try:
        os.makedirs(ddir)
    except Exception as e:
        if os.path.isdir(ddir):
            return
        raise e
    return

def raw_copy(sfile,dfile):
    make_dir_safe(os.path.dirname(dfile))
    #logging.info('[%s] => [%s]'%(sfile,dfile))
    shutil.copy2(sfile, dfile)
    return


def handle_c_file(sfile,dfile,args,param):
    logging.info('c file [%s] => [%s]'%(sfile, dfile))
    clear_random_name()
    if dfile is not None:
        make_dir_safe(os.path.dirname(dfile))    
    cob = COBFile(sfile,dfile,param.config.load_new_prefix())
    s = cob.out_str()
    write_file(s,dfile)
    if args.cob_dump is not None:
        odict = cob.get_replace_json()
        s = format_object_string(odict, 1)
        if param.config.get_count() > 1:
            s = ',\n%s'%(s)
        append_file(s,args.cob_dump)
    return


def cob_copy_file(sfile,dfile,args,params):
    if params.is_in_filter(sfile):
        #logging.info('skip [%s]'%(sfile))
        return

    if params.is_in_handle(sfile):
        handle_c_file(sfile, dfile, args, params)
    else:
        if dfile is not None:
            raw_copy(sfile,dfile)
        else:
            logging.info('dump [%s]'%(sfile))
            s = read_file(sfile)
            write_file(s,None)

    return

def ob_walk_path(srcdir,dstdir,opthdl,args,params):
    for root,dirs, files in os.walk(srcdir):
        for c in files:
            sfile = os.path.join(root,c)
            nsfile = sfile.replace(srcdir, '', 1)
            if os.sep == '/':
                nsfile = re.sub(r'^[/]+','', nsfile)
            elif os.sep == '\\':
                nsfile = re.sub(r'^[\\]+', '', nsfile)
            dfile = os.path.join(dstdir,nsfile)
            #logging.info('sfile %s dfile %s'%(sfile, dfile))
            opthdl(sfile, dfile, args, params)
    return

def set_default_cob_attr(args):
    global GL_DEFAULT_ATTR
    global GL_INIT_ATTR
    for k in GL_INIT_ATTR.keys():
        nk = 'cob_%s'%(k)
        v = args.__getattr__(nk)
        GL_DEFAULT_ATTR[k] = v
    return


def format_cob_config(tabs):
    global GL_INIT_ATTR
    return format_object_string(GL_INIT_ATTR, tabs)


def cob_handler(args,parser):
    set_logging_level(args)
    set_default_cob_attr(args)
    srcdir = args.subnargs[0]
    srcdir = os.path.abspath(srcdir)
    dstdir = None
    logging.info('subnargs [%s]'%(args.subnargs))
    if len(args.subnargs) > 1:
        dstdir = args.subnargs[1]
        dstdir = os.path.abspath(dstdir)
    logging.info('dstdir [%s]'%(dstdir))
    if os.path.isdir(srcdir):
        if dstdir is None:
            logging.info(' ')
            dstdir = os.path.abspath('.')
        param = cobparam(srcdir, dstdir,args.cob_config)
    elif os.path.islink(srcdir) and os.path.isdir(os.path.realpath(srcdir)):
        if dstdir is None:
            logging.info(' ')
            dstdir = os.path.abspath('.')
        param = cobparam(srcdir, dstdir,args.cob_config)
    elif (os.path.islink(srcdir) and os.path.isfile(os.path.realpath(srcdir))) or os.path.isfile(srcdir):
        param = cobparam(os.path.dirname(srcdir), dstdir,args.cob_config)
    else:
        raise Exception('unknown type [%s]'%(args.subnargs[0]))
    if args.cob_dump is not None:
        write_file('{\n', args.cob_dump)
    for c in args.cob_handles:
        param.append_handle(c)
    for c in args.cob_filters:
        param.append_filter(c)
    if os.path.isdir(srcdir):
        ob_walk_path(srcdir, dstdir, cob_copy_file, args, param)
    elif os.path.islink(srcdir):
        realsrc = os.path.realpath(srcdir)
        if os.path.isdir(realsrc):
            ob_walk_path(srcdir, dstdir, cob_copy_file, args, param)
        elif os.path.isfile(realsrc):
            cob_copy_file(srcdir, dstdir, args, params)
        else:
            raise Exception('unknown type [%s]'%(args.subnargs[0]))
    elif os.path.isfile(srcdir):
        cob_copy_file(srcdir, dstdir, args, param)
    else:
        raise Exception('unknown type [%s]'%(args.subnargs[0]))
    if args.cob_dump is not None:
        append_file('\n}', args.cob_dump)
    sys.exit(0)
    return

GL_MAKOB_FILE_VAR='MAKOB_FILE'

def get_makeob_file(fname,makeobfile,args):
    retf = ''
    cdict = dict()
    if os.path.exists(makeobfile):
        s = read_file(makeobfile)
        try:
            cdict = json.loads(s)
            cdict = Utf8Encode(cdict).get_val()
        except:
            cdict = dict()
    # now to get the code
    fdict = dict()
    if 'files' in cdict.keys():
        fdict = cdict['files']
    if fname in fdict.keys():
        retf = fdict[fname]
    else:
        valid = False
        while not valid :
            valid = True
            retf = os.path.join(os.path.dirname(fname),get_random_name(random.randint(args.makob_namemin,args.makob_namemax)))
            fc, extf = os.path.splitext(fname)
            retf += extf
            for k in fdict.keys():
                if fdict[k] == retf:
                    valid = False
        # now to write back
        fdict[fname] = retf
        cdict['files'] = fdict
        write_file(json.dumps(cdict, indent=4), makeobfile)
    # if exists fname and not exists retf just copy
    if os.path.exists(fname) and not os.path.exists(retf):
        shutil.copy2(fname, retf)
    return retf

def makob_handler(args,parser):
    global GL_MAKOB_FILE_VAR
    set_logging_level(args)
    makeobfile = os.path.join(os.getcwd(),'makob.json')
    if GL_MAKOB_FILE_VAR in os.environ.keys():
        makeobfile = os.environ[GL_MAKOB_FILE_VAR]
    rets = ''
    for c in args.subnargs:
        c = os.path.abspath(c)
        retf = get_makeob_file(c,makeobfile,args)
        if len(rets) > 0:
            rets += ' '
        rets += retf
    sys.stdout.write('%s\n'%(rets))
    sys.exit(0)
    return

def obtrans_file_inner(fname,args):
    cdict = dict()
    if os.path.exists(fname):
        s = read_file(fname)
        try:
            cdict = json.loads(s)
            cdict = Utf8Encode(cdict).get_val()
        except:
            cdict = dict()
    # now to get the code
    if 'files' in cdict.keys():
        fdict = cdict['files']
        sortkeys = sorted(fdict.keys())
        idx = 0
        while idx < len(sortkeys):
            ok = sortkeys[idx]
            ov = fdict[ok]
            k = re.sub(args.obtrans_srcdir, args.obtrans_dstdir, ok)
            v = re.sub(args.obtrans_srcdir, args.obtrans_dstdir, ov)
            k = os.path.abspath(k)
            v = os.path.abspath(v)
            fdict[k] = v
            del fdict[ok]
            idx += 1
        # now rewrite back to files
        cdict['files'] = fdict
        write_file(json.dumps(cdict,indent=4), fname)
    return

def obtrans_handler(args,parser):
    set_logging_level(args)
    for c in args.subnargs:
        obtrans_file_inner(c, args)
    sys.exit(0)
    return

def get_unmakob_file(fname,makeobfile,args):
    retf = fname
    cdict = dict()
    if os.path.exists(makeobfile):
        s = read_file(makeobfile)
        try:
            cdict = json.loads(s)
            cdict = Utf8Encode(cdict).get_val()
        except:
            cdict = dict()
    # now to get the code
    fdict = dict()
    if 'files' in cdict.keys():
        fdict = cdict['files']
    if fname in fdict.values():
        for k in fdict.keys():
            if fdict[k] == fname:
                retf = k
                break
    if args.unmakob_short:
        retf = os.path.basename(retf)
    return retf


def unmakob_handler(args,parser):
    global GL_MAKOB_FILE_VAR
    set_logging_level(args)
    makeobfile = os.path.join(os.getcwd(),'makob.json')
    if GL_MAKOB_FILE_VAR in os.environ.keys():
        makeobfile = os.environ[GL_MAKOB_FILE_VAR]
    s = ''
    for c in args.subnargs:
        c = os.path.abspath(c)
        rets = get_unmakob_file(c,makeobfile,args)
        if len(s) > 0:
            s += ' '
        s += rets
    sys.stdout.write('%s\n'%(s))
    sys.exit(0)
    return

def basename_handler(args,parser):
    set_logging_level(args)
    s = ''
    for c in args.subnargs:
        c = os.path.abspath(c)
        rets = os.path.basename(c)
        if len(s) > 0:
            s += ' '
        s += rets
    sys.stdout.write('%s\n'%(s))
    sys.exit(0)
    return

def get_ob_list(fname,args,parser):
    rets = ''
    cdict = dict()
    with open(fname) as fin:
        try:
            cdict = json.load(fin)
        except:
            cdict = dict()
    if 'files' in cdict.keys():
        fdict = cdict['files']
        for k in fdict.keys():
            rets += '%s\n'%(fdict[k])
    return rets

def oblist_handler(args,parser):
    global GL_MAKOB_FILE_VAR
    set_logging_level(args)
    if len(args.subnargs) == 0:
        makobfile = os.path.join(os.getcwd(),'makob.json')
        if GL_MAKOB_FILE_VAR in os.environ.keys():
            makobfile = os.environ[GL_MAKOB_FILE_VAR]
        rets = get_ob_list(makobfile, args, parser)
        sys.stdout.write('%s'%(rets))
    else:
        for c in args.subnargs:
            rets = get_ob_list(c, args, parser)
            sys.stdout.write('%s'%(rets))
    sys.exit(0)
    return

def obuntrans_inner(fname,makobfile,args):
    rets= ''
    ins = read_file(fname)
    sarr = re.split('\n', ins)
    cdict = dict()
    with open(makobfile) as fin:
        try:
            cdict = json.load(fin)
            cdict = Utf8Encode(cdict).get_val()
        except:
            cdict = dict()
    fdict = dict()
    if 'files' in cdict.keys():
        fdict = cdict['files']

    for l in sarr:
        l = l.rstrip('\r\n')
        for k in fdict.keys():
            v = fdict[k]
            ck = os.path.basename(k)
            cv = os.path.basename(v)
            logging.info('ck [%s] cv [%s]'%(ck,cv))
            l = re.sub(cv, ck, l)
            s1 = re.split('\.', ck)
            ok = s1[0]
            s2 = re.split('\.', cv)
            ov = s2[0]
            l = re.sub(ov, ok, l)
        rets += '%s\n'%(l)

    return rets

def obuntrans_handler(args,parser):
    global GL_MAKOB_FILE_VAR
    set_logging_level(args)
    if len(args.subnargs) < 1:
        raise Exception('need at least one put file')

    fname = args.subnargs[0]
    outfile = None
    if len(args.subnargs) > 1:
        outfile = args.subnargs[1]
    makobfile = os.path.join(os.getcwd(),'makob.json')
    if GL_MAKOB_FILE_VAR in os.environ.keys():
        makobfile = os.environ[GL_MAKOB_FILE_VAR]
    rets = obuntrans_inner(fname, makobfile, args)
    write_file(rets,outfile)
    sys.exit(0)
    return

def main():
    commandline_fmt='''
    {
        "verbose|v" : "+",
        "version|V" : false,
        "cob<cob_handler>##srcdir dstdir to obfuscated code in c mode##" : {
            "handles" : ["\\\\.c$","\\\\.h$","\\\\.cpp$","\\\\.cxx$"],
            "filters" : ["\\\\.git$"],
            "config" : null,
            "dump" : null,
            %s,
            "$" : "+"
        },
        "makob<makob_handler>##srcfile to give the other code file ,this need environment variable MAKOB_FILE to get the default (makob.json)##" : {
            "namemin" : 5,
            "namemax" : 20,
            "$" : "+"
        },
        "unmakob<unmakob_handler>##dstfile to give the origin ,this need environment variable MAKOB_FILE to get the default (makob.json)##" : {
            "short" : false,
            "$" : "+"
        },
        "basename<basename_handler>##to make basename##" : {
            "$" : "+"
        },
        "obtrans<obtrans_handler>##translate the srcdir to dstdir in makob file##" : {
            "srcdir" : "",
            "dstdir" : "",
            "$" : "+"
        },
        "oblist<oblist_handler>##to list files ob files##" : {
            "$" : "*"
        },
        "obuntrans<obuntrans_handler>##inputfile [outputfile] to trans file from MAKOB_FILE##" : {
            "$" : "+"
        }
    }
    '''
    commandline = commandline_fmt%(format_cob_config(4))
    d = dict()
    d['version'] = "VERSION_RELACE_STRING"
    options = extargsparse.ExtArgsOptions(d)
    parser = extargsparse.ExtArgsParse(options)
    parser.load_command_line_string(commandline)
    args = parser.parse_command_line(None,parser)
    if args.version:
        sys.stdout.write('%s\n'%(options.version))
        sys.exit(0)
    raise Exception('can not support command [%s]'%(args.subcommand))
    return

##importdebugstart
import disttools



def debug_release():
    if '-v' in sys.argv[1:]:
        #sys.stderr.write('will make verbose\n')
        loglvl =  logging.DEBUG
        logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    tofile= os.path.abspath(os.path.join(topdir,'obcode.py'))
    if len(sys.argv) > 2:
        for k in sys.argv[1:]:
            if not k.startswith('-'):
                tofile = k
                break
    versionfile = os.path.abspath(os.path.join(topdir,'VERSION'))
    if not os.path.exists(versionfile):
        raise Exception('can not find VERSION file')
    with open(versionfile,'r') as f:
        for l in f:
            l = l.rstrip('\r\n')
            vernum = l
            break
    sarr = re.split('\.',vernum)
    if len(sarr) != 3:
        raise Exception('version (%s) not format x.x.x'%(vernum))
    VERSIONNUMBER = vernum
    repls = dict()
    repls[r'VERSION_RELACE_STRING'] = VERSIONNUMBER
    repls[r'debug_main'] = 'main'
    #logging.info('repls %s'%(repls.keys()))
    disttools.release_file('__main__',tofile,[],[[r'##importdebugstart.*',r'##importdebugend.*']],[],repls)
    return

def test_main():
    sys.argv[1:] = sys.argv[2:]
    unittest.main()
    return

def debug_main():
    if '--release' in sys.argv[1:]:
        debug_release()
        return
    main()
    return

##importdebugend

if __name__ == '__main__':
    debug_main()
