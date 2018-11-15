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

##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from filehdl import *
from elfparser import *
from fmthdl import *
from cobattr import *
from cobfile import *
##importdebugend

REPLACE_IMPORT_LIB=1

REPLACE_STR_PARSER=1
REPLACE_FILE_HDL=1
REPLACE_ELF_PARSER=1
REPLACE_FMT_HDL=1
REPLACE_COB_ATTR=1
REPLACE_COB_FILE=1




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

FORMAT_FUNC_NAME_KEY='funcname'
FORMAT_FUNC_CODE_KEY='funccode'
FORMAT_FUNC_OFFSET_KEY='funcoff'
FORMAT_FUNC_XORS_KEY='xors'
FUNC_DATA_KEY='funcdata'
FUNC_DATA_RELOC_KEY='relocs'

def format_ob_patch_functions(objparser,jsondump,objname,funcname,formatname,times,debuglevel=0):
    rets = ''
    ftimes = times
    funcsize = objparser.func_size(funcname)
    funcoff = objparser.func_offset(funcname)
    funcdata = []
    funcvaddr = objparser.func_vaddr(funcname)
    validbytes = 0
    data = []
    data = objparser.get_data()
    for i in range(funcsize):
        if objparser.is_in_reloc((funcvaddr + i), funcname):
            funcdata.append(-1)
        else:
            funcdata.append(0)
            validbytes += 1
    if times == 0:
        # now to get the funcsize
        ftimes = int(validbytes / 2)
    if ftimes >= validbytes:
        ftimes = validbytes - 1

    rets += format_line('int %s(map_prot_func_t mapfunc)'%(formatname), 0)
    rets += format_line('{', 0)
    if objname not in jsondump.keys():
        jsondump[objname] = dict()
        logging.info('jsondump [%s]'%(objname))
    if funcname not in jsondump[objname].keys():
        jsondump[objname][funcname] = dict()
    if FORMAT_FUNC_XORS_KEY not in jsondump[objname][funcname].keys():
        jsondump[objname][funcname][FORMAT_FUNC_XORS_KEY] = dict()
    if FORMAT_FUNC_OFFSET_KEY not in jsondump[objname][funcname].keys():
        jsondump[objname][funcname][FORMAT_FUNC_OFFSET_KEY] = dict()
    jsondump[objname][funcname][FORMAT_FUNC_NAME_KEY] = formatname
    jsondump[objname][funcname][FUNC_DATA_RELOC_KEY] = []
    for i in range(funcsize):
        if objparser.is_in_reloc((funcvaddr+i), funcname):
            jsondump[objname][funcname][FUNC_DATA_RELOC_KEY].append(1)
        else:
            jsondump[objname][funcname][FUNC_DATA_RELOC_KEY].append(0)

    if ftimes > 0:
        i = 0
        rets += format_line('unsigned char* pbaseptr=(unsigned char*)&%s;'%(funcname),1)
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
            if funcdata[xoroff] > 0 or  (xoroff in  jsondump[objname][funcname][FORMAT_FUNC_OFFSET_KEY].keys() \
                and jsondump[objname][funcname][FORMAT_FUNC_OFFSET_KEY][xoroff] > 0):
                continue
            funcdata[xoroff] += 2
            rets += format_line('',1)
            rets += format_debug_line('%s[%d] = 0x%x ^ 0x%x = 0x%x'%(funcname, xoroff, data[funcoff + xoroff],xornum, (data[funcoff + xoroff]^xornum)), 1, debuglevel)
            rets += format_line('pcurptr = (pbaseptr + %d);'%(xoroff),1)
            rets += format_line('*pcurptr ^= %d;'%(xornum),1)
            jsondump[objname][funcname][FORMAT_FUNC_XORS_KEY][xoroff] = xornum
            jsondump[objname][funcname][FORMAT_FUNC_OFFSET_KEY][xoroff] = funcdata[xoroff]
            i += 1
        rets += format_line('if (mapfunc != NULL){',1)
        rets += format_line('ret = mapfunc(pbaseptr,%d,OB_MAP_READ|OB_MAP_EXEC);'%(funcsize),2)
        rets += format_line('if (ret < 0) {',2)
        rets += format_line('return -1;',3)
        rets += format_line('}',2)
        rets += format_line('}',1)

    rets += format_line('return 0;',1)
    rets += format_line('}',0)
    jsondump[objname][funcname][FORMAT_FUNC_CODE_KEY]= rets
    return jsondump

def patch_data(odict,objparser,objname,funcs,objdata):
    for f in funcs:
        foff = objparser.func_offset(f)
        if foff < 0 :
            raise Exception('can not find [%s]'%(f))
        fvaddr = objparser.func_vaddr(f)
        assert(fvaddr >= 0)
        for off in odict[objname][f][FORMAT_FUNC_XORS_KEY].keys():
            if odict[objname][f][FORMAT_FUNC_OFFSET_KEY][off] >= 2:
                # we change the xor data into
                objdata[(foff + off)] = objdata[(foff + off)] ^ odict[objname][f][FORMAT_FUNC_XORS_KEY][off]
    for f in funcs:
        foff = objparser.func_offset(f)      
        fsize = objparser.func_size(f)
        odict[objname][f][FUNC_DATA_KEY] = objdata[foff:(foff+ fsize)]
    return objdata

def elf_one_file(odict,objfile,funcs,times,verbose):
    elfparser = ElfParser(objfile)
    for funcname in funcs:
        nformatfunc = get_random_name(random.randint(5,20))
        odict = format_ob_patch_functions(elfparser,odict,objfile,funcname,nformatfunc,times,verbose)


    # now to give the change file
    objdata = elfparser.get_data()
    #logging.info('[%s] data\n%s'%(objfile,dump_ints(objdata)))
    logging.info('funcs %s'%(funcs))
    for f in funcs:
        foff = elfparser.func_offset(f)
        fsize = elfparser.func_size(f)
        logging.info('foff [%d]'%(foff))
        if foff < 0 :
            raise Exception('can not find [%s]'%(f))
        fvaddr = elfparser.func_vaddr(f)
        assert(fvaddr >= 0)
        for off in odict[objfile][f][FORMAT_FUNC_XORS_KEY].keys():            
            if odict[objfile][f][FORMAT_FUNC_OFFSET_KEY][off] >= 2:
                # we change the xor data into
                logging.info('[%s].[%s]foff [0x%x] + off [0x%x] [0x%02x] ^ [0x%02x] => [0x%02x]'%(objfile,f,\
                 foff, off,objdata[(foff + off)] ,\
                 odict[objfile][f][FORMAT_FUNC_XORS_KEY][off], \
                 objdata[(foff + off)] ^ odict[objfile][f][FORMAT_FUNC_XORS_KEY][off]))
                objdata[(foff + off)] = objdata[(foff + off)] ^ odict[objfile][f][FORMAT_FUNC_XORS_KEY][off]
        odict[objfile][f][FUNC_DATA_KEY] = objdata[foff:(foff+fsize)]
    elfparser.close()
    #logging.info('writeback [%s]\n%s'%(objfile,dump_ints(objdata)))
    write_file_ints(objdata,objfile)
    return odict

def obunpatchelf_handler(args,parser):
    set_logging_level(args)
    if len(args.subnargs) < 1:
        raise Exception('obunpackelf objectfile functions')
    jdict = dict()
    for a in args.subnargs:
        sarr = re.split(':',a)
        if len(sarr) < 2:
            continue
        carr = re.split(',',sarr[1])
        jdict[sarr[0]] = carr


    if args.dump is None or not os.path.exists(args.dump):
        odict = dict()
    else:
        with open(args.dump) as fin:
            odict = json.load(fin)
            odict = Utf8Encode(odict).get_val()
    rets = ''
    rets += format_line('#include <obcode.h>',0)
    rets += format_line('#include <stdio.h>',0)
    rets += format_line('#include <stdlib.h>',0)
    for s in args.includes:
        rets += format_line('#include <%s>'%(s),0)

    for s in args.includefiles:
        rets += format_line('#include "%s"'%(s),0)

    for f in jdict.keys():
        logging.info('f [%s] funcs %s'%(f,jdict[f]))
        elf_one_file(odict,f,jdict[f],args.times,args.verbose)

    for o in odict.keys():
        rets += format_debug_line('format file [%s]'%(o),0,args.verbose)
        for f in odict[o]:
            rets += format_line('',0)
            rets += format_debug_line('format for function [%s]'%(f),0,args.verbose)
            rets += odict[o][f][FORMAT_FUNC_CODE_KEY]

    rets += format_line('',0)
    rets += format_line('int %s(map_prot_func_t mapfunc)'%(args.obunpatchelf_funcname),0)
    rets += format_line('{',0)
    retout = 0
    for o in jdict.keys():
        if retout == 0:
            rets += format_line('int ret;',1)
            retout = 1
        for f in jdict[o]:
            rets += format_line('',1)
            rets += format_debug_line('format for %s'%(f),1,args.verbose)
            rets += format_line('ret = %s(mapfunc);'%(odict[o][f][FORMAT_FUNC_NAME_KEY]),1)
            rets += format_line('if (ret < 0) {', 1)
            rets += format_line('return ret;',2)
            rets += format_line('}',1)
    rets += format_line('return 0;',1)
    rets += format_line('}',0)

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
    sys.exit(0)
    return

def obpatchelf_handler(args,parser):
    set_logging_level(args)
    if args.dump is None:
        raise Exception('no dump file get')
    ofile = args.subnargs[0]
    with open(args.dump,'r') as fin:
        odict = json.load(fin)
        odict = Utf8Encode(odict).get_val()

    elfparser = ElfParser(ofile)
    alldatas = elfparser.get_data()
    for o in odict.keys():
        for f in odict[o].keys():
            rels = odict[o][f][FUNC_DATA_RELOC_KEY]
            #logging.info('rels\n%s'%(dump_ints(rels)))
            offsetk = odict[o][f][FORMAT_FUNC_OFFSET_KEY]
            data = odict[o][f][FUNC_DATA_KEY]
            reloff = elfparser.get_text_file_off(data,rels,f)
            xors = odict[o][f][FORMAT_FUNC_XORS_KEY]
            for k in xors.keys():
                if xors[k] <= 1:
                    ki = int(k)
                    logging.info('[%s].[%s] [+%d] [0x%02x] = [0x%02x] ^ [0x%02x]'%( o, f,ki,\
                        alldatas[(reloff + ki)] ^ offsetk[k], alldatas[(reloff + ki)], \
                        offsetk[k]))
                    alldatas[(reloff + ki)] = alldatas[(reloff + ki)] ^ offsetk[k]
                    xors[k] = 2
            odict[o][f][FORMAT_FUNC_XORS_KEY] = xors
    elfparser.close()
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
        "obunpatchelf<obunpatchelf_handler>##objfilename:func1,func2 ... to format unpatch elf file with func1##" : {
            "$" : "+",
            "funcname" : "unpatch_handler"
        },
        "obpatchelf<obpatchelf_handler>##inputfile to patch elf functions##" : {
            "$" : 1
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
from pyparser import *

def make_string_slash_ok(s):
    sarr = re.split('\n', s)
    rets = ''
    for l in sarr:
        l = l.rstrip('\r\n')
        cexpr = None
        if len(l) > 0 and l[-1] == '\\':
            cexpr = get_random_name(20)
            cont = True
            while cont:
                cont = False
                matchl = re.sub(cexpr, '', l)
                if matchl != l:
                    cont = True
                    cexpr = get_random_name(20)
            l = re.sub('\\$', cexpr, l)
        l = re.sub(r'\\', r'\\\\', l)
        if cexpr is not None:
            l = re.sub(cexpr, r'\\', l)
        rets += '%s\n'%(l)
    return rets

def get_import_file(fname):
    rets = ''
    started = False
    with open(fname,'r+b') as f:
        for l in f:
            if sys.version[0] == '3':
                l = l.decode('utf8')                
            l = l.rstrip('\r\n')
            if not started:
                if l.startswith('##extractcode_start'):
                    started = True
            else:
                if l.startswith('##extractcode_end'):
                    started = False
                else:
                    rets += l
                    rets += '\n'
    return rets

def make_filters_out(ims,files):
    cont = True
    jdx = 0
    idx = 0
    while cont:
        cont = False
        idx = 0
        while idx < len(ims) and not cont:
            jdx = 0
            while jdx < len(files) and not cont:
                if ims[idx].frommodule == files[jdx]:
                    cont = True
                    logging.info('del [%d] jdx [%d] [%s]'%(idx,jdx,ims[idx]))
                    del ims[idx]
                    logging.info('%s'%(ims))
                    break
                jdx += 1                
            idx += 1
    return ims

def fromat_ext_import_files():
    files = get_file_filter(os.path.abspath(os.path.dirname(__file__)),['.py'])
    curbase = re.sub('\.py$','',os.path.basename(__file__))
    allims = []
    for f in files:
        if len(f) == 0:
            continue
        if f == curbase:
            continue
        curf = os.path.abspath(os.path.join(os.path.dirname(__file__),'%s.py'%(f)))
        allims.extend(get_import_names(curf))

    curims= get_import_names(__file__)
    curims = packed_import(curims)
    curims = make_filters_out(curims, files)
    logging.info('curims %s'%(curims))
    allims = packed_import(allims)
    allims = make_filters_out(allims, files)
    logging.info('allims %s'%(allims))
    cont = True
    seccont = True
    while cont:
        cont = False
        idx = 0
        while idx < len(allims) :
            jdx = 0
            while jdx < len(curims) :
                if allims[idx].frommodule == curims[jdx].frommodule and \
                    allims[idx].module == curims[jdx].module:
                    cont = True
                    #logging.info('del [%d] %s'%(idx,allims[idx]))
                    del allims[idx]
                    break
                jdx += 1
            if cont:
                break
            idx += 1
    rets = ''
    for m in allims:
        rets += '%s\n'%(format_import(m))
    return rets

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
    strparser = os.path.abspath(os.path.join(curdir,'strparser.py'))
    filehdl = os.path.abspath(os.path.join(curdir,'filehdl.py'))
    fmthdl =os.path.abspath(os.path.join(curdir,'fmthdl.py'))
    cobattr = os.path.abspath(os.path.join(curdir,'cobattr.py'))
    cobfile = os.path.abspath(os.path.join(curdir,'cobfile.py'))
    elfparser = os.path.abspath(os.path.join(curdir,'elfparser.py'))
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
    strparser_c = get_import_file(strparser)
    filehdl_c = get_import_file(filehdl)
    fmthdl_c = get_import_file(fmthdl)
    cobattr_c = get_import_file(cobattr)
    cobfile_c = get_import_file(cobfile)
    elfparser_c = get_import_file(elfparser)
    #logging.info('str_c\n%s'%(strparser_c))
    sarr = re.split('\.',vernum)
    if len(sarr) != 3:
        raise Exception('version (%s) not format x.x.x'%(vernum))
    VERSIONNUMBER = vernum
    import_rets = fromat_ext_import_files()
    logging.info('import_rets\n%s'%(import_rets))
    repls = dict()
    repls[r'VERSION_RELACE_STRING'] = VERSIONNUMBER
    repls[r'debug_main'] = 'main'
    repls[r'REPLACE_STR_PARSER=1'] = make_string_slash_ok(strparser_c)
    repls[r'REPLACE_FILE_HDL=1']= make_string_slash_ok(filehdl_c)
    repls[r'REPLACE_FMT_HDL=1']= make_string_slash_ok(fmthdl_c)
    repls[r'REPLACE_COB_ATTR=1'] = make_string_slash_ok(cobattr_c)
    repls[r'REPLACE_COB_FILE=1'] = make_string_slash_ok(cobfile_c)
    repls[r'REPLACE_ELF_PARSER=1'] = make_string_slash_ok(elfparser_c)
    repls[r'REPLACE_IMPORT_LIB=1'] = make_string_slash_ok(import_rets)
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
