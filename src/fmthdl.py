#! /usr/bin/env python

import random
import json
import logging
import re
import sys
import os

##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
##importdebugend


##extractcode_start
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
            elif c == '\r':
                rets += '\\r'
            elif c == '\n':
                rets += '\\n'
            elif c == '\t':
                rets += '\\t'
            elif c == '\b':
                rets += '\\b'
            else:
                rets += c
    return rets

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

def format_printf_func(l,tabs):
    #return format_line(l,tabs)
    return ''
    
def format_bytes_set_function(sbyte,nameprefix='prefix', namelen=10, numturns=30, tabs=0,debug=0,line=None):
    funcname = '%s_%s'%(nameprefix,get_random_name(namelen))
    funcstr = ''
    funcstr += format_line('int %s(unsigned char* pbuf, int size)'%(funcname),tabs)
    funcstr += format_line('{', tabs)
    funcstr += format_printf_func('int i;', tabs + 1)
    if line is not None:
        funcstr += format_debug_line('first at line [%d]'%(line), tabs + 1 , debug)
    funcstr += format_debug_line('variable:nameprefix %s variable:namelen %d variable:numturns %d length(%d)'%(nameprefix,namelen,numturns,len(sbyte)), tabs + 1, debug)
    ss = ''
    for c in sbyte:
        if len(ss) > 0:
            ss += ',0x%02x'%(c)
        else:
            ss += 'sbyte [0x%02x'%(c)
    ss += ']'
    funcstr += format_debug_line('%s'%(ss), tabs + 1, debug)
    funcstr += format_printf_func('for (i=0;i<size;i++){', tabs + 1)
    funcstr += format_printf_func('printf("[%d]=[%d:0x%x]\\n",i,pbuf[i],pbuf[i]);', tabs + 2)
    funcstr += format_printf_func('}', tabs + 1)

    clbits = []
    leastmask = []
    for i in range(len(sbyte)):
        clbits.append(random.randint(0,255))
        leastmask.append(0)

    ss = ''
    for c in clbits:
        if len(ss) > 0:
            ss += ',0x%x:%d'%(c,c)
        else:
            ss += 'clbits [0x%x:%d'%(c,c)
    ss += ']'
    funcstr += format_printf_func('/* %s */'%(ss), tabs+1)

    for i in range(len(sbyte)):
        curnum = clear_bit(sbyte[i], clbits[i])
        funcstr += format_line('',tabs+1)
        funcstr += format_debug_line('pbuf[%d] & 0x%x ?=> 0x%x'%(i,curnum,sbyte[i]), tabs + 1, debug)
        funcstr += format_line('if (size > %d){'%(i), tabs + 1)
        funcstr += format_printf_func('printf("[%d][%%d:0x%%x] & [%%d:0x%%x] = [%%d:0x%%x] [target:0x%x:%d]\\n",pbuf[%d], pbuf[%d], %d,%d, (pbuf[%d] & %d), (pbuf[%d] & %d));'%(i,sbyte[i],sbyte[i],i,i,curnum,curnum,i,curnum,i,curnum), tabs+2)
        funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] & 0x%x);'%(i,i,curnum), tabs + 2)
        funcstr += format_line('}',tabs + 1)

    # we need not to set the number directly ,but just used
    for i in range(numturns):
        cidx = random.randint(0, len(sbyte) - 1)
        cbit = random.randint(0, 255)
        if random.randint(0,1) == 1:
            cnum = clear_bit(sbyte[cidx], cbit)
            leastmask[cidx] = leastmask[cidx] | cnum
            funcstr += format_line('', tabs + 1)
            funcstr += format_line('if ( size > %d){'%(cidx), tabs + 1)
            funcstr += format_printf_func('printf("||[%d][%%d:0x%%x] | [%%d:0x%%x] = [%%d:0x%%x] [target:0x%x:%d]\\n",pbuf[%d],pbuf[%d],%d,%d,(pbuf[%d] | %d), (pbuf[%d] | %d));'%(cidx,sbyte[cidx],sbyte[cidx],cidx,cidx,cnum,cnum,cidx,cnum,cidx,cnum), tabs + 2)
            funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] | 0x%x);'%(cidx,cidx, cnum), tabs + 2)
            funcstr += format_line('}', tabs + 1)
        else:
            cnum = expand_bit(sbyte[cidx], cbit)
            funcstr += format_line('', tabs + 1)
            funcstr += format_line('if ( size > %d){'%(cidx), tabs + 1)
            funcstr += format_printf_func('printf("&&[%d][%%d:0x%%x] & [%%d:0x%%x] = [%%d:0x%%x] [target:0x%x:%d]\\n",pbuf[%d],pbuf[%d],%d,%d,(pbuf[%d] & %d), (pbuf[%d] & %d));'%(cidx,sbyte[cidx],sbyte[cidx],cidx,cidx,cnum,cnum,cidx,cnum,cidx,cnum), tabs + 2)
            funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] & 0x%x);'%(cidx,cidx, cnum), tabs + 2)
            funcstr += format_line('}', tabs + 1)

    # now we should filled the number
    for i in range(len(sbyte)):
        cnum = sbyte[i] & (~leastmask[i])
        if cnum > 0:
            funcstr += format_line('',tabs+1)
            funcstr += format_debug_line('pbuf[%d] | 0x%x ?=> 0x%x'%(i,cnum, sbyte[i]), tabs + 1, debug)
            funcstr += format_line('if (size > %d){'%(i), tabs + 1)
            funcstr += format_printf_func('printf("[%d] [%%d:0x%%x] | [%%d:0x%%x] = [%%d:0x%%x] [target:0x%x:%d]\\n", pbuf[%d], pbuf[%d], %d ,%d , (pbuf[%d] | %d), (pbuf[%d] | %d));'%(i,sbyte[i],sbyte[i],i,i,cnum,cnum,i,cnum,i,cnum), tabs + 2)
            funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] | 0x%x);'%(i,i,cnum), tabs + 2)
            funcstr += format_line('}',tabs + 1)

    funcstr += format_line('', tabs + 1)
    funcstr += format_line('return size;', tabs + 1)
    funcstr += format_line('}', tabs)
    return funcstr,funcname


def format_bytes_xor_function(sbyte,abyte,abytefunc,bbyte,bbytefunc,nameprefix='prefix', namelen=10, numturns=30, tabs=0,debug=0, line=None):
    assert(len(sbyte) == len(abyte))
    assert(len(abyte) == len(bbyte))
    funcname = '%s_%s'%(nameprefix,get_random_name(namelen))
    bname = '%s_%s'%(nameprefix, get_random_name(namelen))
    retname = '%s_%s'%(nameprefix, get_random_name(namelen))
    funcstr = ''
    funcstr += format_line('int %s(unsigned char* pbuf, int size)'%(funcname),tabs)
    funcstr += format_line('{', tabs)
    if line is not None:
        funcstr += format_debug_line('first at line [%d]'%(line),tabs + 1, debug)    
    funcstr += format_debug_line('variable:nameprefix %s variable:namelen %d variable:numturns %d length(%d)'%(nameprefix,namelen,numturns,len(sbyte)), tabs + 1, debug)
    ss = ''
    for c in sbyte:
        if len(ss) > 0:
            ss += ',0x%x'%(c)
        else:
            ss += 'sbyte [0x%x'%(c)
    if len(ss) > 0:
        ss += ']'
    funcstr += format_debug_line('%s'%(ss), tabs + 1, debug)
    if  len(sbyte) >= 4 and sbyte[-1] == 0 and sbyte[-2] == 0 and sbyte[-3] == 0 and sbyte[-4] == 0:
        funcstr += format_debug_line('var wstring:[%s]'%(quote_string(uni32_to_string(sbyte))), tabs + 1, debug)    
    elif len(sbyte) >= 2 and sbyte[-1] == 0 and sbyte[-2] == 0:
        funcstr += format_debug_line('var wstring:[%s]'%(quote_string(uni16_to_string(sbyte))), tabs + 1, debug)
    else:
        funcstr += format_debug_line('var string:[%s]'%(quote_string(ints_to_string(sbyte))), tabs + 1, debug)
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
    for i in range(numturns):
        cidx = random.randint(0, len(sbyte) - 1)
        didx = random.randint(0, len(sbyte) - 1)
        hdl = random.randint(0, 5)
        funcstr += format_line('', tabs + 1)
        if hdl == 0:
            # to make abyte[cidx] = abyte[cidx] & bbyte[didx]
            funcstr += format_debug_line('abyte[%d] = abyte[%d] & bbyte[%d]'%(cidx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x & 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] & bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] & %s[%d]);'%(cidx, cidx, bname, didx), tabs + 2)
            funcstr += format_line('}', tabs + 1)
            abyte[cidx] = abyte[cidx] & bbyte[didx]
        elif hdl == 1:
            # to make abyte[cidx] = abyte[cidx] | bbyte[didx]
            funcstr += format_debug_line('abyte[%d] = abyte[%d] | bbyte[%d]'%(cidx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x | 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] | bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] | %s[%d]);'%(cidx, cidx, bname, didx), tabs + 2)
            funcstr += format_line('}', tabs + 1)
            abyte[cidx] = abyte[cidx] | bbyte[didx]
        elif hdl == 2:
            # to make bbyte[didx] = abyte[cidx] & bbyte[didx]
            funcstr += format_debug_line('bbyte[%d] = abyte[%d] & bbyte[%d]'%(didx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x & 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] & bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('%s[%d] = (unsigned char)(pbuf[%d] & %s[%d]);'%(bname,didx, cidx, bname, didx), tabs + 2)
            funcstr += format_line('}', tabs + 1)
            bbyte[didx] = abyte[cidx] & bbyte[didx]
        elif hdl == 3:
            # to make bbyte[didx] = abyte[cidx] | bbyte[didx]
            funcstr += format_debug_line('bbyte[%d] = abyte[%d] | bbyte[%d]'%(didx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x & 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] | bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('%s[%d] = (unsigned char)(pbuf[%d] | %s[%d]);'%(bname,didx, cidx, bname, didx), tabs + 2)
            funcstr += format_line('}', tabs + 1)
            bbyte[didx] = abyte[cidx] | bbyte[didx]
        elif hdl == 4:
            # to make abyte[cidx] = abyte[cidx] ^ bbyte[didx]
            funcstr += format_debug_line('abyte[%d] = abyte[%d] ^ bbyte[%d]'%(cidx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x ^ 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] ^ bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] ^ %s[%d]);'%(cidx, cidx, bname, didx), tabs + 2)
            funcstr += format_line('}', tabs + 1)
            abyte[cidx] = abyte[cidx] ^ bbyte[didx]
        elif hdl == 5:
            # to make bbyte[didx] = abyte[cidx] ^ bbyte[didx]
            funcstr += format_debug_line('bbyte[%d] = abyte[%d] ^ bbyte[%d]'%(didx,cidx,didx), tabs + 1, debug)
            funcstr += format_debug_line('0x%x ^ 0x%x = 0x%0x'%(abyte[cidx],bbyte[didx], (abyte[cidx] ^ bbyte[didx])), tabs + 1, debug)
            funcstr += format_line('if ( %d < size && %d < size ) {'%(cidx, didx), tabs + 1 )
            funcstr += format_line('%s[%d] = (unsigned char)(pbuf[%d] ^ %s[%d]);'%(bname,didx, cidx, bname, didx), tabs + 2)
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
            funcstr += format_line('pbuf[%d] = (unsigned char)(pbuf[%d] ^ 0x%x);'%(i,i,cnum),tabs + 2)
            funcstr += format_line('}',tabs + 1)
        elif hdl == 1:
            cnum = sbyte[i] ^ bbyte[i]
            funcstr += format_debug_line('pbuf[%d] = (bbyte[%d])0x%x ^ 0x%x'%(i,i,bbyte[i], cnum),tabs + 1, debug)
            funcstr += format_line('if (%d < size){'%(i), tabs + 1)
            funcstr += format_line('pbuf[%d] = (unsigned char)(%s[%d] ^ 0x%x);'%(i,bname,i,cnum),tabs + 2)
            funcstr += format_line('}',tabs + 1)
        else:
            raise Exception('unexpected random valud [%d]'%(hdl))

    funcstr += format_line('',tabs + 1)
    funcstr += format_line('return size;', tabs + 1)
    funcstr += format_line('}',tabs)
    return funcstr, funcname
##extractcode_end