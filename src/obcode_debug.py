#! /usr/bin/env python

import extargsparse
import sys
import re
import logging
import os
import shutil
import random
import json


##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from filehdl import *
from elfparser import *
from coffparser import *
from peparser import *
from fmthdl import *
from cobattr import *
from cobfile import *
from obmaklib import *
from extract_ob import *
##importdebugend

REPLACE_IMPORT_LIB=1

REPLACE_STR_PARSER=1
REPLACE_FILE_HDL=1
REPLACE_ELF_PARSER=1
REPLACE_COFF_PARSER=1
REPLACE_PE_PARSER=1
REPLACE_FMT_HDL=1
REPLACE_COB_ATTR=1
REPLACE_COB_FILE=1
REPLACE_OBMAK_LIB=1
REPLACE_EXTRACT_OB=1


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


FORMAT_FUNC_NAME_KEY='funcname'
FORMAT_FUNC_CODE_KEY='funccode'
FORMAT_FUNC_OFFSET_KEY='funcoff'
FORMAT_FUNC_XORS_KEY='xors'
FORMAT_FUNC_ORIG_KEY='origdata'
FUNC_DATA_KEY='funcdata'
FUNC_DATA_RELOC_KEY='relocs'
PATCH_FUNC_KEY='patchfunc'
WIN32_MODE_KEY='win32mode'


def format_ob_patch_functions(objparser,jsondump,objname,funcname,formatname,times,debuglevel=0,win32mode=False):
    global PATCH_FUNC_KEY
    rets = ''
    ftimes = times
    realf = funcname
    getfunccall = None
    if win32mode:
        realf = '_%s'%(funcname)
    funcsize = objparser.func_size(realf)
    funcoff = objparser.func_offset(realf)
    funcdata = []
    funcvaddr = objparser.func_vaddr(realf)
    validbytes = 0
    data = []
    data = objparser.get_data()
    for i in range(funcsize):
        if objparser.is_in_reloc((funcvaddr + i), realf):
            funcdata.append(-1)
        else:
            funcdata.append(0)
            validbytes += 1
    if times == 0:
        # now to get the funcsize
        ftimes = int(validbytes / 2)
    if ftimes >= validbytes:
        ftimes = validbytes - 1

    getfunccall = '%s'%(get_random_name(20))
    rets += format_debug_line('get function [%s] address in win32 mode'%(funcname), 0, debuglevel)
    rets += format_line('unsigned char* %s(unsigned char* p)'%(getfunccall), 0)
    rets += format_line('{',0)
    rets += format_line('unsigned char* pretp = p;',1)
    rets += format_line('signed int* pjmp;',1)
    rets += format_line('',1)
    rets += format_line('if (*pretp == 0xe9){',1)
    rets += format_line('pjmp = (signed int*)(pretp + 1);',2)
    rets += format_line('pretp += sizeof(*pjmp) + 1;', 2)
    rets += format_line('pretp += (*pjmp);',2)
    rets += format_line('}',1)
    rets += format_line('',1)
    rets += format_line('return pretp;',1)
    rets += format_line('}',0)
    rets += format_line('',0)


    rets += format_line('int %s(map_prot_func_t mapfunc)'%(formatname), 0)
    rets += format_line('{', 0)
    if PATCH_FUNC_KEY not in jsondump.keys():
        jsondump[PATCH_FUNC_KEY] = dict()
    if objname not in jsondump[PATCH_FUNC_KEY].keys():
        jsondump[PATCH_FUNC_KEY][objname] = dict()
        logging.info('jsondump [%s]'%(objname))
    if funcname not in jsondump[PATCH_FUNC_KEY][objname].keys():
        jsondump[PATCH_FUNC_KEY][objname][funcname] = dict()
    if FORMAT_FUNC_XORS_KEY not in jsondump[PATCH_FUNC_KEY][objname][funcname].keys():
        jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_XORS_KEY] = dict()
    if FORMAT_FUNC_OFFSET_KEY not in jsondump[PATCH_FUNC_KEY][objname][funcname].keys():
        jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_OFFSET_KEY] = dict()
    jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_NAME_KEY] = formatname
    jsondump[PATCH_FUNC_KEY][objname][funcname][FUNC_DATA_RELOC_KEY] = []
    for i in range(funcsize):
        if objparser.is_in_reloc((funcvaddr+i), realf):
            jsondump[PATCH_FUNC_KEY][objname][funcname][FUNC_DATA_RELOC_KEY].append(1)
        else:
            jsondump[PATCH_FUNC_KEY][objname][funcname][FUNC_DATA_RELOC_KEY].append(0)


    if ftimes > 0:
        i = 0
        rets += format_line('unsigned char* pbaseptr=(unsigned char*)%s((unsigned char*)%s);'%(getfunccall,funcname),1)
        rets += format_line('unsigned char* pcurptr;',1)
        rets += format_line('int ret;',1)
        rets += format_line('',1)
        rets += format_line('if (mapfunc != NULL){',1)
        rets += format_line('ret = mapfunc(pbaseptr,%d,OB_MAP_READ|OB_MAP_EXEC|OB_MAP_WRITE);'%(funcsize),2)
        rets += format_line('if (ret < 0) {',2)
        rets += format_line('return -1;',3)
        rets += format_line('}',2)
        rets += format_line('}',1)
        while i < ftimes:
            xornum = random.randint(0,255)
            xoroff = random.randint(0,funcsize - 1)
            if xornum == 0 :
                continue
            if funcdata[xoroff] > 0 or  (xoroff in  jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_OFFSET_KEY].keys() \
                and jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_OFFSET_KEY][xoroff] > 0):
                continue
            funcdata[xoroff] += 2
            rets += format_line('',1)
            if funcdata[xoroff] >= 2:
                rets += format_debug_line('%s[0x%x:%d] = 0x%x ^ 0x%x = 0x%x'%(funcname, xoroff, xoroff, data[funcoff + xoroff],xornum, (data[funcoff + xoroff]^xornum)), 1, debuglevel)
            else:
                rets += format_debug_line('%s[0x%x:%d] = ? ^ 0x%x = ?'%(funcname, xoroff, xoroff, xornum), 1, debuglevel)
            rets += format_line('pcurptr = (pbaseptr + %d);'%(xoroff),1)
            #rets += format_debug_line('printf("patch [%%p] [0x%%02x] = [0x%%02x] ^ [0x%02x]\\n", pcurptr, (*pcurptr ^ 0x%x), *pcurptr);'%(xornum,xornum),1,debuglevel)
            #rets += format_line('printf("patch [%%p] [0x%%02x] = [0x%%02x] ^ [0x%02x]\\n", pcurptr, (*pcurptr ^ 0x%x), *pcurptr);'%(xornum,xornum),1)
            rets += format_line('*pcurptr ^= %d;'%(xornum),1)
            logging.info('[%s].[%s] +[0x%x:%d] xornum [0x%x:%d] funcdata[%d]'%(objname,funcname,xoroff,xoroff,xornum,xornum,funcdata[xoroff]))
            jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_XORS_KEY][xoroff] = xornum
            jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_OFFSET_KEY][xoroff] = funcdata[xoroff]
            i += 1
        rets += format_line('if (mapfunc != NULL){',1)
        rets += format_line('ret = mapfunc(pbaseptr,%d,OB_MAP_READ|OB_MAP_EXEC);'%(funcsize),2)
        rets += format_line('if (ret < 0) {',2)
        rets += format_line('return -1;',3)
        rets += format_line('}',2)
        rets += format_line('}',1)

    rets += format_line('return 0;',1)
    rets += format_line('}',0)
    jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_CODE_KEY]= rets
    return jsondump

def object_one_file_func(objparser,odict,objfile,f,objdata, times,verbose,win32mode=False):    
    if PATCH_FUNC_KEY in odict.keys() and objfile in odict[PATCH_FUNC_KEY].keys() and \
        f in odict[PATCH_FUNC_KEY][objfile].keys():
        return odict,objdata
    if PATCH_FUNC_KEY not in odict.keys():
        odict[PATCH_FUNC_KEY] = dict()
    if objfile not in odict[PATCH_FUNC_KEY].keys():
        odict[PATCH_FUNC_KEY][objfile] = dict()
    if f not in odict[PATCH_FUNC_KEY][objfile].keys():
        odict[PATCH_FUNC_KEY][objfile][f] = dict()
    nformatfunc = get_random_name(random.randint(5,20))
    odict = format_ob_patch_functions(objparser,odict,objfile,f,nformatfunc,times,verbose,win32mode)
    realf = f
    if win32mode:
        realf = '_%s'%(f)
    foff = objparser.func_offset(realf)
    fsize = objparser.func_size(realf)
    logging.info('foff [0x%x:%d]'%(foff,foff))
    if foff < 0 :
        raise Exception('can not find [%s]'%(realf))
    fvaddr = objparser.func_vaddr(realf)
    assert(fvaddr >= 0)
    for off in odict[PATCH_FUNC_KEY][objfile][f][FORMAT_FUNC_XORS_KEY].keys():
        if odict[PATCH_FUNC_KEY][objfile][f][FORMAT_FUNC_OFFSET_KEY][off] >= 2:
            # we change the xor data into
            offi = int(off)
            logging.info('[%s].[%s]foff [0x%x] + off [0x%x] [0x%02x] ^ [0x%02x] => [0x%02x]'%(objfile,f,\
                foff, offi,objdata[(foff + offi)] ,\
                odict[PATCH_FUNC_KEY][objfile][f][FORMAT_FUNC_XORS_KEY][off], \
                objdata[(foff + offi)] ^ odict[PATCH_FUNC_KEY][objfile][f][FORMAT_FUNC_XORS_KEY][off]))
            objdata[(foff + offi)] = objdata[(foff + offi)] ^ odict[PATCH_FUNC_KEY][objfile][f][FORMAT_FUNC_XORS_KEY][off]
    odict[PATCH_FUNC_KEY][objfile][f][FUNC_DATA_KEY] = objdata[foff:(foff+fsize)]
    if win32mode:
        odict[PATCH_FUNC_KEY][objfile][f][WIN32_MODE_KEY] = True
    else:
        odict[PATCH_FUNC_KEY][objfile][f][WIN32_MODE_KEY] = False
    return odict,objdata


def object_one_file(objparser,odict,objfile,funcs,times,verbose,win32mode=False):
    objdata = objparser.get_data()
    for funcname in funcs:
        odict, objdata = object_one_file_func(objparser, odict,objfile,funcname,objdata,times,verbose,win32mode)
    return odict,objdata

def elf_one_file(odict,objfile,funcs,times,verbose):
    elfparser = ElfParser(objfile)
    odict, objdata = object_one_file(elfparser,odict,objfile,funcs,times,verbose)
    elfparser.close()
    #logging.info('writeback [%s]\n%s'%(objfile,dump_ints(objdata)))
    write_file_ints(objdata,objfile)
    return odict

def get_jdict(args):
    jdict = dict()
    win32 = False
    includes = []
    includefiles = []
    for a in args.subnargs:
        if a.startswith('includefiles;'):
            sarr = re.split(';',a)
            if len(sarr) > 1:
                includefiles.extend(sarr[1:])
        elif a.startswith('includes;'):
            sarr = re.split(';',a)
            if len(sarr) > 1:
                includes.extend(sarr[1:])
        elif a.startswith('win32;'):
            win32 = True
        else:
            sarr = re.split(';',a)
            if len(sarr) < 2:
                continue
            carr = re.split(',',sarr[1])
            jdict[sarr[0]] = carr
    return jdict,includefiles,includes,win32

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
    rets += format_line('#include <stdio.h>',0)
    rets += format_line('#include <stdlib.h>',0)
    for s in args.includes:
        rets += format_line('#include <%s>'%(s),0)

    for s in args.includefiles:
        rets += format_line('#include "%s"'%(s),0)
    return rets

def format_patch_funcions(args,odict,jdict,patchfuncname,prefix='prefix'):
    rets = format_includes(args)
    staticvarname = '%s_%s'%(prefix,get_random_name(20))
    if PATCH_FUNC_KEY in odict.keys():
        for o in jdict.keys():
            rets += format_debug_line('format file [%s]'%(o),0,args.verbose)
            for f in jdict[o]:
                rets += format_line('',0)
                rets += format_debug_line('format for function [%s]'%(f),0,args.verbose)
                rets += odict[PATCH_FUNC_KEY][o][f][FORMAT_FUNC_CODE_KEY]

    rets += format_line('',0)
    rets += format_line('int %s(map_prot_func_t mapfunc)'%(patchfuncname),0)
    rets += format_line('{',0)
    retout = 0
    for o in jdict.keys():
        if retout == 0:
            rets += format_line('int ret;',1)
            rets += format_line('static int %s=0;'%(staticvarname),1)
            rets += format_line('',1)
            rets += format_line('if (%s > 0) {'%(staticvarname), 1)
            rets += format_line('return 0;',2)
            rets += format_line('}',1)
            retout = 1
        for f in jdict[o]:
            rets += format_line('',1)
            rets += format_debug_line('format for %s'%(f),1,args.verbose)
            rets += format_line('ret = %s(mapfunc);'%(odict[PATCH_FUNC_KEY][o][f][FORMAT_FUNC_NAME_KEY]),1)
            rets += format_line('if (ret < 0) {', 1)
            rets += format_line('return ret;',2)
            rets += format_line('}',1)
    rets += format_line('%s=1;'%(staticvarname), 1)
    rets += format_line('return 0;',1)
    rets += format_line('}',0)
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

    if args.dump is None:
        fout = sys.stderr
    else:
        fout = open(args.dump,'w+b')
    write_file_direct(json.dumps(odict,sort_keys=True,indent=4), fout)
    if fout != sys.stderr:
        fout.close()
    else:
        fout.flush()
    fout = None
    return

def patch_objects(objparser,args,odict):
    alldatas = objparser.get_data()
    ofile = args.output
    if PATCH_FUNC_KEY in odict.keys():
        if ofile not in odict[PATCH_FUNC_KEY].keys():
            odict[PATCH_FUNC_KEY][ofile] = dict()
        for o in args.subnargs:
            if o not in odict[PATCH_FUNC_KEY][ofile].keys() and o in odict[PATCH_FUNC_KEY].keys():
                odict[PATCH_FUNC_KEY][ofile][o] = dict()
                odict[PATCH_FUNC_KEY][ofile][o] = Utf8Encode(odict[PATCH_FUNC_KEY][o]).get_val()
                for f in odict[PATCH_FUNC_KEY][ofile][o].keys():
                    rels = odict[PATCH_FUNC_KEY][ofile][o][f][FUNC_DATA_RELOC_KEY]
                    #logging.info('rels\n%s'%(dump_ints(rels)))
                    offsetk = odict[PATCH_FUNC_KEY][ofile][o][f][FORMAT_FUNC_OFFSET_KEY]
                    data = odict[PATCH_FUNC_KEY][ofile][o][f][FUNC_DATA_KEY]
                    reloff = objparser.get_text_file_off(data,rels,f)
                    xors = odict[PATCH_FUNC_KEY][ofile][o][f][FORMAT_FUNC_XORS_KEY]
                    for k in offsetk.keys():
                        logging.info('xors[%s]=%d'%(k,offsetk[k]))
                        if offsetk[k] <= 1:
                            ki = int(k)
                            logging.info('[%s].[%s] [+0x%x:%d] [0x%02x] = [0x%02x] ^ [0x%02x]'%( o, f,ki,ki,\
                                alldatas[(reloff + ki)] ^ offsetk[k], alldatas[(reloff + ki)], \
                                offsetk[k]))
                            alldatas[(reloff + ki)] = alldatas[(reloff + ki)] ^ xors[k]
                            xors[k] = 2
                    odict[PATCH_FUNC_KEY][ofile][o][f][FORMAT_FUNC_OFFSET_KEY] = offsetk
    return odict,alldatas


def obunpatchelf_handler(args,parser):
    set_logging_level(args)
    if len(args.subnargs) < 1:
        raise Exception('obunpackelf objectfile functions')
    jdict,includefiles,includes,win32 = get_jdict(args)
    args.includefiles.extend(includefiles)
    args.includes.extend(includes)
    if win32:
        args.win32 = True
    odict = get_odict(args,False)

    for f in jdict.keys():
        logging.info('f [%s] funcs %s'%(f,jdict[f]))
        elf_one_file(odict,f,jdict[f],args.times,args.obunpatchelf_loglvl)

    rets = format_patch_funcions(args,odict,jdict,args.obunpatchelf_funcname)
    write_patch_output(args,rets,odict)
    sys.exit(0)
    return

def obpatchelf_handler(args,parser):
    set_logging_level(args)
    if args.dump is None:
        raise Exception('no dump file get')
    if args.output is None:
        raise Exception('must set output')
    ofile = args.output
    with open(args.dump,'r') as fin:
        odict = json.load(fin)
        odict = Utf8Encode(odict).get_val()

    elfparser = ElfParser(ofile)
    odict,alldatas = patch_objects(elfparser,args,odict)
    elfparser.close()
    write_file_ints(alldatas,ofile)
    with open(args.dump,'w+b') as fout:
        write_file_direct(json.dumps(odict,sort_keys=True,indent=4), fout)

    sys.exit(0)
    return


def coff_one_file(odict,objfile,funcs,times,verbose,win32mode=False):
    coffparser = CoffParser(objfile)
    odict, objdata = object_one_file(coffparser,odict,objfile,funcs,times,verbose,win32mode)
    coffparser.close()
    #logging.info('writeback [%s]\n%s'%(objfile,dump_ints(objdata)))
    write_file_ints(objdata,objfile)
    return odict


def obunpatchcoff_handler(args,parser):
    set_logging_level(args)
    if len(args.subnargs) < 1:
        raise Exception('obunpackelf objectfile functions')
    jdict, includefiles, includes, win32 = get_jdict(args)
    args.includefiles.extend(includefiles)
    args.includes.extend(includes)
    if win32 :
        args.win32 = True
    odict = get_odict(args,False)

    for f in jdict.keys():
        logging.info('f [%s] funcs %s'%(f,jdict[f]))
        coff_one_file(odict,f,jdict[f],args.times,args.obunpatchcoff_loglvl,args.win32)

    rets = format_patch_funcions(args,odict,jdict,args.obunpatchcoff_funcname)
    write_patch_output(args,rets,odict)
    sys.exit(0)
    return


def obpatchpe_handler(args,parser):
    set_logging_level(args)
    if args.dump is None:
        raise Exception('no dump file get')
    if args.output is None:
        raise Exception('must set output')
    ofile = args.output
    with open(args.dump,'r') as fin:
        odict = json.load(fin)
        odict = Utf8Encode(odict).get_val()

    peparser = PEParser(ofile)
    odict,alldatas = patch_objects(peparser,args,odict)
    peparser.close()
    write_file_ints(alldatas,ofile)
    with open(args.dump,'w+b') as fout:
        write_file_direct(json.dumps(odict,sort_keys=True,indent=4), fout)
    sys.exit(0)
    return



def main():
    commandline_fmt='''
    {
        "verbose|v" : "+",
        "version|V" : false,
        "win32|W" : false,
        "output|o" : null,
        "times|T" : 0,
        "dump|D" : null,
        "includes|I" : [],
        "includefiles" : [],
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
        },
        "obunpatchelf<obunpatchelf_handler>##objfilename:func1,func2 ... to format unpatch elf file with func1 func2##" : {
            "$" : "+",
            "loglvl" : 3,
            "funcname" : "unpatch_handler"
        },
        "obpatchelf<obpatchelf_handler>##inputfile to patch elf functions##" : {
            "$" : "+"
        },
        "obunpatchcoff<obunpatchcoff_handler>##objfile:func1,func2 ... to format unpatch coff file with func1 func2##" : {
            "$" : "+",
            "loglvl" : 3,
            "funcname" : "unpatch_handler"
        },
        "obpatchpe<obpatchpe_handler>##inputfile to patch pe functions##" : {
            "$" : "+"
        },
        "obunfunc<obunfunc_handler>##funcs... to set obfuncs##" : {
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
from obrelease import *

def debug_release():
    if '-v' in sys.argv[1:]:
        #sys.stderr.write('will make verbose\n')
        loglvl =  logging.DEBUG
        if logging.root is not None and len(logging.root.handlers) > 0:
            logging.root.handlers = []
        logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    tofile= os.path.abspath(os.path.join(topdir,'obcode.py'))
    curdir = os.path.abspath(os.path.dirname(__file__))
    rlfiles = ReleaseFiles(__file__)
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'strparser.py')),r'REPLACE_STR_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'filehdl.py')), r'REPLACE_FILE_HDL=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'fmthdl.py')), r'REPLACE_FMT_HDL=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'cobattr.py')), r'REPLACE_COB_ATTR=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'cobfile.py')),r'REPLACE_COB_FILE=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'elfparser.py')),r'REPLACE_ELF_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'coffparser.py')),r'REPLACE_COFF_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'peparser.py')),r'REPLACE_PE_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'obmaklib.py')),r'REPLACE_OBMAK_LIB=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'extract_ob.py')),r'REPLACE_EXTRACT_OB=1')

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
    #logging.info('str_c\n%s'%(strparser_c))
    sarr = re.split('\.',vernum)
    if len(sarr) != 3:
        raise Exception('version (%s) not format x.x.x'%(vernum))
    VERSIONNUMBER = vernum
    import_rets = fromat_ext_import_files(__file__,rlfiles.get_includes())
    logging.info('import_rets\n%s'%(import_rets))
    rlfiles.add_repls(r'VERSION_RELACE_STRING',VERSIONNUMBER)
    rlfiles.add_repls(r'debug_main','main')
    rlfiles.add_repls(r'REPLACE_IMPORT_LIB=1',make_string_slash_ok(import_rets))
    #logging.info('repls %s'%(repls.keys()))
    disttools.release_file('__main__',tofile,[],[[r'##importdebugstart.*',r'##importdebugend.*']],[],rlfiles.get_repls())
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
