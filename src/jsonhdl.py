#! /usr/bin/env python


import sys
import os
import logging
import re
import json

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from fmthdl import *
from elfparser import *
from coffparser import *
from peparser import *


##extractcode_start
FORMAT_FUNC_NAME_KEY='funcname'
FORMAT_FUNC_CODE_KEY='funccode'
FORMAT_FUNC_OFFSET_KEY='funcoff'
FORMAT_FUNC_XORS_KEY='xors'
FORMAT_FUNC_ORIG_KEY='origdata'
FUNC_DATA_KEY='funcdata'
FUNC_DATA_RELOC_KEY='relocs'
PATCH_FUNC_KEY='patchfunc'
WIN32_MODE_KEY='win32mode'
GET_FUNC_ADDR='getfuncaddr'
FUNC_ADDR_NAME='funcaddrname'
FUNC_ADDR_CODE='funcaddrcode'


CHKVAL_KEY='chkval'

RANDOM_VARIABLE='variable'
CHKVAL_START_FUNCTION_NAME='crc32_calc'
CHKVAL_END_FUNCTION_NAME='check_end_func'
CHKVAL_BASE_FUNCTION_NAME='check_value_func'


CHKVAL_RANDOM_VALUE='rndval'
CHKVAL_FUNC_CHECKS_START='func_checks_start'
CHKVAL_FUNC_CHECKS='func_checks'
CHKVAL_FUNC_CHECKS_END='func_checks_end'
CHKVAL_VALUE_CHECKS='value_checks'
CHKVAL_VALUE_CHECKS_DICT='idx'
CHKVAL_VALUE_CHECKS_TOTAL_END='value_checks_total_end'
CHKVAL_FUNC_CHECK_CRC32_FUNC='check_crc32_value'
CHKVAL_FUNC_CHECK_MD5_FUNC='check_md5_value'
CHKVAL_FUNC_CHECK_SHA256_FUNC='check_sha256_value'
CHKVAL_FUNC_CHECK_SHA3_FUNC='check_sha3_value'
CHKVAL_FUNC_CHECK_CHKVAL_VALUE='check_chkval_value'

CHKVAL_STRUCT_OFFSET='m_offset'
CHKVAL_STRUCT_NAMEXOR1='m_namexor1'
CHKVAL_STRUCT_NAMEXOR2='m_namexor2'
CHKVAL_STRUCT_SIZE='m_size'
CHKVAL_STRUCT_CRC32VAL='m_crc32val'
CHKVAL_STRUCT_MD5VAL='m_md5val'
CHKVAL_STRUCT_SHA256VAL='m_sha256val'
CHKVAL_STRUCT_SHA3VAL='m_sha3val'
CHKVAL_STRUCT_LASTONE='LAST_STRUCT_MEMBER'

CHKVAL_STRUCT_OFFSET_SIZE=8
CHKVAL_STRUCT_SIZE_SIZE=8
CHKVAL_STRUCT_CRC32VAL_SIZE=16
CHKVAL_STRUCT_SHA256VAL_SIZE=32
CHKVAL_STRUCT_NAMEXOR1_SIZE=64
CHKVAL_STRUCT_NAMEXOR2_SIZE=64
CHKVAL_STRUCT_SHA3VAL_SIZE=64
CHKVAL_STRUCT_MD5VAL_SIZE=32

CALC_CRC32_SIZE=4
CALC_MD5_SIZE=16
CALC_SHA256_SIZE=32
CALC_SHA3_SIZE=64
CALC_SIZE_SIZE=8
CALC_OFFSET_SIZE=8

CHKVAL_RAW_DATA='rawdata'
CHKVAL_RDATA_DATAS='data'
CHKVAL_RDATA_RELOCS='relocs'

CHKVAL_OBJ_DATA='objdata'

CHKVAL_AES_KEY_SIZE=32
CHKVAL_AES_IV_SIZE=16

CHKVAL_EXIT_HANDLER_FILES='exit_handler_files'
CHKVAL_DATA_FILES='data_files'

def set_odict_value(odict,val,*path):
    curodict = odict
    idx = 0
    while idx < len(path) - 1:
        if path[idx] not in curodict.keys():
            curodict[path[idx]] = dict()
        curodict = curodict[path[idx]]
        idx += 1
    curodict[path[idx]] = val
    return odict    

def get_odict_value(odict,*path):
    idx = 0
    curodict = odict
    while idx < (len(path) - 1):
        if path[idx] not in curodict.keys():
            return None
        curodict = curodict[path[idx]]
        idx += 1
    if path[idx] not in curodict.keys():
        return None
    return curodict[path[idx]]

def append_odict_value(odict,val,*path):
    nval = get_odict_value(odict,*path)
    if nval is None:
        nval = []
    nval.append(val)
    return set_odict_value(odict,nval,*path)

def create_odict_is_none(odict,*path):
    if get_odict_value(odict,*path) is None:
        val = dict()
        return set_odict_value(odict,val, *path)
    return odict

def write_json(odict,outfile=None):
    if outfile is None:
        fout = sys.stderr
    else:
        fout = open(outfile,'w+b')
    write_file_direct(json.dumps(odict,sort_keys=True,indent=4), fout)
    if fout != sys.stderr:
        fout.close()
    else:
        fout.flush()
    fout = None
    return

def get_jdict(args):
    jdict = dict()
    win32 = False
    includes = []
    includefiles = []
    for a in args.subnargs:
        if a.startswith('includefiles;'):
            sarr = re.split(';',a)
            if len(sarr) > 1 and len(sarr[1]) > 0:
                sarr = re.split(',', sarr[1])
                if args.includefiles is None:
                    args.includefiles = []
                args.includefiles.extend(sarr)
        elif a.startswith('includes;'):
            sarr = re.split(';',a)
            if len(sarr) > 1 and len(sarr[1]) > 0:
                sarr = re.split(',', sarr[1])
                if args.includes is None:
                    args.includes = []
                args.includes.extend(sarr)
        elif a.startswith('win32;'):
            args.win32 = True
        elif a.startswith('verbose;'):
            sarr = re.split(';',a)
            if len(sarr) > 1 and len(sarr[1]) > 0:
                args.verbose = int(sarr[1])
        elif a.startswith('output;'):
            sarr = re.split(';',a)
            if len(sarr) > 1 and len(sarr[1]) > 0:
                args.output = sarr[1]
        elif a.startswith('dump;'):
            sarr = re.split(';',a)
            if len(sarr) > 1 and len(sarr[1]) > 0:
                args.dump = sarr[1]
        elif a.startswith('unpatchfunc;'):
            sarr = re.split(';',a)
            if len(sarr) > 1 and len(sarr[1]) > 0:
                args.unpatchfunc = sarr[1]
        elif a.startswith('objfile;'):
            sarr = re.split(';',a)
            if len(sarr) > 1 and len(sarr[1]) > 0:
                args.objfile = sarr[1]
        elif a.startswith('objsuffix;'):
            sarr = re.split(';',a)
            if len(sarr) > 1 and len(sarr[1]) > 0:
                args.objsuffix = sarr[1]
        elif a.startswith('csuffix;'):
            sarr = re.split(';',a)
            if len(sarr) > 1 and len(sarr[1]) > 0:
                args.csuffix = sarr[1]
        else:
            sarr = re.split(';',a)
            if len(sarr) < 2:
                jdict[sarr[0]] = []
                continue
            carr = re.split(',',sarr[1])
            f = os.path.abspath(sarr[0])
            jdict[f] = carr
    return jdict , args

def get_odict(args,force):
    if args.dump is None or (not os.path.exists(args.dump) and not force):
        odict = dict()
    else:
        with open(args.dump) as fin:
            odict = json.load(fin)
            odict = Utf8Encode(odict).get_val()
    return odict

def format_includes(args):
    rets = ''
    rets += format_line('#include <obcode.h>',0)
    for s in args.includes:
        rets += format_line('#include <%s>'%(s),0)

    for s in args.includefiles:
        rets += format_line('#include "%s"'%(s),0)
    return rets

def write_patch_output(args,rets,odict):
    if args.output is None:
        fout = sys.stdout
    else:
        fout = open(args.output,'w+b')

    write_file_direct(rets,fout)
    if fout != sys.stdout:
        fout.close()
    else:
        fout.flush()
    fout = None

    write_json(odict,args.dump)
    return

def call_object_parser(clsname,f):
    m = __import__(__name__)
    cls_ = getattr(m,clsname)
    if cls_ is None:
        raise Exception('cannot find [%s]'%(clsname))
    return cls_(f)
##extractcode_end
