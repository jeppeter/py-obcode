#! /usr/bin/env python


import sys
import os
import logging

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
CHKVAL_STRUCT_NAMEXOR1_SIZE=64
CHKVAL_STRUCT_NAMEXOR2_SIZE=64
CHKVAL_STRUCT_SIZE_SIZE=8
CHKVAL_STRUCT_CRC32VAL_SIZE=8
CHKVAL_STRUCT_MD5VAL_SIZE=16
CHKVAL_STRUCT_SHA256VAL_SIZE=32
CHKVAL_STRUCT_SHA3VAL_SIZE=64

CHKVAL_RAW_DATA='rawdata'
CHKVAL_RDATA_DATAS='data'
CHKVAL_RDATA_RELOCS='relocs'

CHKVAL_OBJ_DATA='objdata'

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
##extractcode_end
