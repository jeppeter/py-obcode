#! /usr/bin/env python

import sys
import logging



##extractcode_start
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


def string_to_uni16(s):
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

def uni16_to_string(sbyte):
    s = ''  
    if len(sbyte) >= 2 and sbyte[-1] == 0 and sbyte[-2] == 0:
        sbyte = sbyte[:-2]
    nbyte = []
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

def string_to_uni32(s):
    sbyte = []
    ri = []
    if sys.version[0] == '3':
        rb = s.encode('utf-32-le')
    else:       
        rc = s.decode('utf8')   
        rb = rc.encode('utf-32-le')
    for i in range(len(rb)):
        if sys.version[0] == '3':
            ri.append(int(rb[i]))
        else:
            ri.append(ord(rb[i]))
    # to add null for unicode
    ri.append(0)
    ri.append(0)
    ri.append(0)
    ri.append(0)
    logging.info('ri %s'%(ri))
    return ri

def uni32_to_string(sbyte):
    s = ''  
    if len(sbyte) >= 4 and sbyte[-1] == 0 and sbyte[-2] == 0 and sbyte[-3] == 0 and sbyte[-4] == 0:
        sbyte = sbyte[:-4]
    nbyte = []
    nbyte.extend(sbyte)
    if sys.version[0] == '3':
        cb = b''
        for i in range(len(nbyte)):
            cb += nbyte[i].to_bytes(1,'little')
        return cb.decode('utf-32-le')
    else:
        cb = b''
        for i in range(len(nbyte)):
            cb += chr(nbyte[i])
        cs = cb.decode('utf-32-le')
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
##extractcode_end