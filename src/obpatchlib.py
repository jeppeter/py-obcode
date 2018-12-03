#! /usr/bin/env python

import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from objparser import *
from elfparser import *
from coffparser import *

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


def format_ob_patch_functions(objparser,jsondump,objname,funcname,formatname,times, getfunccall,debuglevel=0,win32mode=False):
    global PATCH_FUNC_KEY
    rets = ''
    ftimes = times
    realf = funcname
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
        val = objparser.is_in_reloc((funcvaddr + i), realf)
        if val == OBJ_RELOC_NONE:
            funcdata.append(0)
            validbytes += 1
        elif val == OBJ_RELOC_ON:
            funcdata.append(-1)
        elif val == OBJ_RELOC_FORBID:
            funcdata.append(-10)
        else:
            raise Exception('not valid value [%d]'%(val))
    if times == 0:
        # now to get the funcsize
        ftimes = int(funcsize / 2)
    if ftimes >= validbytes:
        ftimes = validbytes - 1

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
        jsondump[PATCH_FUNC_KEY][objname][funcname][FUNC_DATA_RELOC_KEY].append(objparser.is_in_reloc((funcvaddr+i), realf))


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
            if funcdata[xoroff] < -1:
                # it is forbid to set the value ,so we do not use it
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
            #rets += format_line('printf("[%%s:%%d] patch [%s].[+0x%x:%d] [%%p] [0x%%02x] = [0x%%02x] ^ [0x%02x]\\n",__FILE__,__LINE__, pcurptr, (*pcurptr ^ 0x%x), *pcurptr);'%(funcname,xoroff,xoroff,xornum,xornum),1)
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
    else:
        rets += format_line('mapfunc = mapfunc;',1)


    rets += format_line('return 0;',1)
    rets += format_line('}',0)
    jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_CODE_KEY]= rets
    return jsondump

def format_get_func_addr(debuglevel=0):
    funcallname = get_random_name(20)
    rets = ''

    rets += format_line('',0)
    rets += format_debug_line('get function address in win32 mode', 0, debuglevel)
    rets += format_line('unsigned char* %s(unsigned char* p)'%(funcallname), 0)
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
    return rets , funcallname

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
    getfunccall = None
    if GET_FUNC_ADDR not in odict[PATCH_FUNC_KEY].keys():
        odict[PATCH_FUNC_KEY][GET_FUNC_ADDR] = dict()
        code , name = format_get_func_addr(verbose)
        odict[PATCH_FUNC_KEY][GET_FUNC_ADDR][FUNC_ADDR_NAME] = name
        odict[PATCH_FUNC_KEY][GET_FUNC_ADDR][FUNC_ADDR_CODE] = code
    getfunccall = odict[PATCH_FUNC_KEY][GET_FUNC_ADDR][FUNC_ADDR_NAME]
    nformatfunc = get_random_name(random.randint(5,20))
    odict = format_ob_patch_functions(objparser,odict,objfile,f,nformatfunc,times, getfunccall,verbose,win32mode)
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
        else:
            sarr = re.split(';',a)
            if len(sarr) < 2:
                continue
            carr = re.split(',',sarr[1])
            jdict[sarr[0]] = carr
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
    rets += format_line('#include <stdio.h>',0)
    rets += format_line('#include <stdlib.h>',0)
    for s in args.includes:
        rets += format_line('#include <%s>'%(s),0)

    for s in args.includefiles:
        rets += format_line('#include "%s"'%(s),0)
    return rets

def format_patch_funcions(args,odict,jdict,patchfuncname,prefix='prefix'):
    rets = format_includes(args)
    if PATCH_FUNC_KEY in odict.keys() and \
        GET_FUNC_ADDR in odict[PATCH_FUNC_KEY].keys():
        rets += odict[PATCH_FUNC_KEY][GET_FUNC_ADDR][FUNC_ADDR_CODE]
    if PATCH_FUNC_KEY in odict.keys():
        for o in jdict.keys():
            rets += format_debug_line('format file [%s]'%(o),0,args.verbose)
            for f in jdict[o]:
                rets += format_line('',0)
                rets += format_debug_line('format for function [%s]'%(f),0,args.verbose)
                rets += odict[PATCH_FUNC_KEY][o][f][FORMAT_FUNC_CODE_KEY]

    staticvarname = '%s_%s'%(prefix,get_random_name(20))
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
    jdict , args = get_jdict(args)
    odict = get_odict(args,False)

    for f in jdict.keys():
        logging.info('f [%s] funcs %s'%(f,jdict[f]))
        elf_one_file(odict,f,jdict[f],args.times,args.obunpatchelf_loglvl)

    rets = format_patch_funcions(args,odict,jdict,args.unpatchfunc)
    write_patch_output(args,rets,odict)
    sys.exit(0)
    return

def obpatchelf_handler(args,parser):
    set_logging_level(args)
    jdict, args = get_jdict(args)
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
    jdict ,args = get_jdict(args)
    odict = get_odict(args,False)

    for f in jdict.keys():
        logging.info('f [%s] funcs %s'%(f,jdict[f]))
        coff_one_file(odict,f,jdict[f],args.times,args.obunpatchcoff_loglvl,args.win32)

    rets = format_patch_funcions(args,odict,jdict,args.unpatchfunc)
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

def obpatchelfforge_handler(args,parser):
    set_logging_level(args)
    sys.exit(0)
    return

def obunpatchelfforge_handler(args,parser):
    set_logging_level(args)
    jdict , args = get_jdict(args)
    odict = dict()
    rets = ''
    rets += format_includes(args)
    rets += format_line('int %s(map_prot_func_t mapfunc)'%(args.unpatchfunc),0)
    rets += format_line('{',0)
    rets += format_line('mapfunc = mapfunc;', 1)
    rets += format_line('return 0;',1)
    rets += format_line('}',0)
    write_patch_output(args,rets,odict)
    sys.exit(0)
    return

##extractcode_end