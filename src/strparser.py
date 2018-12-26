#! /usr/bin/env python

import sys
import logging
import random
import time


##extractcode_start

def set_logging_level(args):
    loglvl= logging.ERROR
    if args.verbose >= 3:
        loglvl = logging.DEBUG
    elif args.verbose >= 2:
        loglvl = logging.INFO
    if logging.root is not None and len(logging.root.handlers) > 0:
        logging.root.handlers = []
    logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    #logging.basicConfig(level=loglvl,format='%(funcName)s:%(lineno)d\t%(message)s')
    random.seed(time.time()*10000)
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


def get_bytes_hash(sbyte):
    hv = 0
    for v in sbyte:
        # 113 is primer
        hv *= 113
        hv += v
        # 104729 is the primer
        hv = hv % 104729
    return hv

def get_name_hash(s):
    sbyte = string_to_ints(s)
    return get_bytes_hash(sbyte)

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

def ints_to_bytes(sbyte):
    cb = b''
    if sys.version[0] == '3':
        for i in range(len(sbyte)):
            cb += sbyte[i].to_bytes(1,'little')
    else:
        for i in range(len(sbyte)):
            cb += chr(sbyte[i])
    return cb

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


def bytes_to_ints(sbyte):
    ints = []
    for c in sbyte:
        if sys.version[0] == '3':
            ints.append(int(c))
        else:
            ints.append(ord(c))
    return ints


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
    #logging.info('ri %s'%(ri))
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

GL_VAR_NAME_VARS=''
GL_VAR_NAME_STARTS=''
for i in range(26):
    GL_VAR_NAME_VARS += chr(ord('a')+i)
    GL_VAR_NAME_STARTS += chr(ord('a')+i)

for i in range(26):
    GL_VAR_NAME_VARS += chr(ord('A') + i)
    GL_VAR_NAME_STARTS += chr(ord('A')+i)

for i in range(10):
    GL_VAR_NAME_VARS += chr(ord('0')+i)


GL_RANDOM_NAMES=[]

def get_random_name(num=10):
    global GL_VAR_NAME_VARS
    global GL_VAR_NAME_STARTS
    global GL_RANDOM_NAMES
    retval = True
    while retval:
        retval = False
        retstr = ''
        idx = 0
        while idx < num:
            if idx == 0:
                rnd = random.randint(0,len(GL_VAR_NAME_STARTS)-1)
                retstr += GL_VAR_NAME_STARTS[rnd]
            else:
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

def get_random_bytes(num):
    sarr = []
    i = 0
    while i < num:
        sarr.append(random.randint(0,255))
        i += 1
    return sarr

def format_bytes_c(sarr):
    rets = ''
    i = 0
    while i < len(sarr):
        if i > 0:
            rets += ','
        rets += '0x%02x'%(sarr[i])
        i += 1
    return rets

def zero_bytes(num):
    sarr = []
    for i in range(num):
        sarr.append(0)
    return sarr

def format_bytes(hexstr,size,bigendian=False):
    sarr = zero_bytes(size)
    fillsize = int((len(hexstr)+1)/2)
    if fillsize > size:
        raise Exception('filled size [%d] > size[%d]'%(fillsize,size))
    if bigendian:
        idx = size - 1
    else:
        idx = 0
    chstr = hexstr
    while len(chstr) > 0:
        if len(chstr) > 1:
            cch = chstr[-2:]
            chstr = chstr[:-2]
        else:
            cch = chstr
            chstr = ''
        sarr[idx] = int(cch,16)
        if bigendian:
            idx -= 1
        else:
            idx += 1
    return sarr

def set_data_bytes(alldata,data,foff,note=''):
    assert((foff+ len(data))<= len(alldata))
    #logging.debug('[%s].[0x%x:%d][0x%x:%d] %s'%(note,foff,foff,len(data),len(data),format_bytes_c(data)))
    idx = 0
    while idx < len(data):
        alldata[(foff + idx)] = data[idx]
        idx += 1

    return alldata

def format_bytes_debug(data,note=''):
    rets = ''
    if len(note) > 0:
        rets += note
    rets += 'data [0x%x:%d]'%(len(data),len(data))
    idx = 0
    lastidx = 0
    while idx < len(data):
        if (idx % 16) == 0:
            if lastidx != idx:
                rets += ' ' * 4
            while lastidx != idx:
                if data[lastidx] >= ord(' ') and \
                    data[lastidx] <= ord('~'):
                    rets += '%c'%(chr(data[lastidx]))
                else:
                    rets += '.'
                lastidx += 1
            rets += '\n0x%08x:'%(idx)
        rets += ' 0x%02x'%(data[idx])
        idx += 1
    if idx != lastidx:
        while (idx % 16) != 0:
            rets += ' ' * 5
            idx += 1
        rets += ' ' * 4
        while lastidx < len(data):
            if data[lastidx] >= ord(' ') and \
                data[lastidx] <= ord('~'):
                rets += '%c'%(chr(data[lastidx]))
            else:
                rets += '.'
            lastidx += 1
        rets += '\n'
    return rets

def output_list(files,fout=None,withquote=False):
    if fout is None:
        fout = sys.stdout
    idx = 0
    for f in files:
        if idx > 0:
            fout.write(' ')
        if withquote:
            fout.write('"%s"'%(quote_string(f)))
        else:
            fout.write('%s'%(f))
        idx += 1
    fout.write('\n')
    fout.flush()
    return


##extractcode_end