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


def format_ob_patch_func_xors(objparser,jsondump,objname,funcname,formatname,times,win32mode):
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
            jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_XORS_KEY][xoroff] = xornum
            jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_OFFSET_KEY][xoroff] = funcdata[xoroff]
            i += 1
    return jsondump

def format_ob_patch_func_code(objparser,jsondump,objname,funcname,formatname,getfunccall,debuglevel=0,win32mode=False):
    rets = ''
    realf = funcname
    if win32mode:
        realf = '_%s'%(funcname)

    offsetk = jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_OFFSET_KEY]
    xors = jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_XORS_KEY]
    funcsize = objparser.func_size(realf)

    ftimes = 0    
    for k in offsetk.keys():
        assert(k in xors.keys())
        ftimes += 1
    rets += format_line('int %s(map_prot_func_t mapfunc)'%(formatname), 0)
    rets += format_line('{', 0)

    if ftimes > 0:
        data = objparser.get_data()
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
        funcdata = jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_OFFSET_KEY]
        funcoff = objparser.func_offset(realf)
        for xoroff in offsetk.keys():
            xornum = xors[xoroff]
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
    else:
        rets += format_line('mapfunc = mapfunc;', 1)
    rets += format_line('return 0;',1)
    rets += format_line('}',0)
    jsondump[PATCH_FUNC_KEY][objname][funcname][FORMAT_FUNC_CODE_KEY]= rets
    return jsondump

def format_ob_patch_functions(objparser,jsondump,objname,funcname,formatname,times, getfunccall,debuglevel=0,win32mode=False):
    jsondump = format_ob_patch_func_xors(objparser,jsondump,objname,funcname,formatname,times,win32mode)
    jsondump = format_ob_patch_func_code(objparser,jsondump,objname,funcname,formatname,getfunccall,debuglevel,win32mode)
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

def unpatch_one_file_func(objparser,odict,objfile,f,objdata,win32mode=False):
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
    for offi in odict[PATCH_FUNC_KEY][objfile][f][FORMAT_FUNC_XORS_KEY].keys():
        if odict[PATCH_FUNC_KEY][objfile][f][FORMAT_FUNC_OFFSET_KEY][offi] >= 2:
            # we change the xor data into
            off = int(offi)
            logging.info('[%s].[%s]foff [0x%x] + off [0x%x] [0x%02x] ^ [0x%02x] => [0x%02x]'%(objfile,f,\
                foff, off,objdata[(foff + off)] ,\
                odict[PATCH_FUNC_KEY][objfile][f][FORMAT_FUNC_XORS_KEY][offi], \
                objdata[(foff + off)] ^ odict[PATCH_FUNC_KEY][objfile][f][FORMAT_FUNC_XORS_KEY][offi]))
            objdata[(foff + off)] = objdata[(foff + off)] ^ odict[PATCH_FUNC_KEY][objfile][f][FORMAT_FUNC_XORS_KEY][offi]
    odict[PATCH_FUNC_KEY][objfile][f][FUNC_DATA_KEY] = objdata[foff:(foff+fsize)]
    return odict,objdata

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
    odict,objdata = unpatch_one_file_func(objparser,odict,objfile,f,objdata,win32mode)
    if win32mode:
        odict[PATCH_FUNC_KEY][objfile][f][WIN32_MODE_KEY] = True
    else:
        odict[PATCH_FUNC_KEY][objfile][f][WIN32_MODE_KEY] = False
    return odict,objdata

def call_object_parser(clsname,f):
    m = __import__(__name__)
    cls_ = getattr(m,clsname)
    if cls_ is None:
        raise Exception('cannot find [%s]'%(clsname))
    return cls_(f)


def object_one_file(objclsname,odict,objfile,funcs,times,verbose,win32mode=False):
    objparser = call_object_parser(objclsname,objfile)
    objdata = objparser.get_data()
    for funcname in funcs:
        odict, objdata = object_one_file_func(objparser, odict,objfile,funcname,objdata,times,verbose,win32mode)
    objparser.close()
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
        elif a.startswith('objfile;'):
            sarr = re.split(';',a)
            if len(sarr) > 1 and len(sarr[1]) > 0:
                args.objfile = sarr[1]
        else:
            sarr = re.split(';',a)
            if len(sarr) < 2:
                jdict[sarr[0]] = []
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
    for s in args.includes:
        rets += format_line('#include <%s>'%(s),0)

    for s in args.includefiles:
        rets += format_line('#include "%s"'%(s),0)
    return rets

def output_patch_function(args,prefix,patchfuncname,odict,files):
    staticvarname = '%s_%s'%(prefix,get_random_name(20))
    rets = ''
    rets += format_line('',0)
    rets += format_line('int %s(map_prot_func_t mapfunc)'%(patchfuncname),0)
    rets += format_line('{',0)
    retout = 0
    for o in files:
        if retout == 0:
            rets += format_line('int ret;',1)
            rets += format_line('static int %s=0;'%(staticvarname),1)
            rets += format_line('',1)
            rets += format_line('if (%s > 0) {'%(staticvarname), 1)
            rets += format_line('return 0;',2)
            rets += format_line('}',1)
            retout = 1
        for f in odict[PATCH_FUNC_KEY][o]:
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

def format_patch_funcions(args,odict,files,patchfuncname,prefix='prefix'):
    rets = format_includes(args)
    if PATCH_FUNC_KEY in odict.keys() and \
        GET_FUNC_ADDR in odict[PATCH_FUNC_KEY].keys():
        rets += odict[PATCH_FUNC_KEY][GET_FUNC_ADDR][FUNC_ADDR_CODE]
    if PATCH_FUNC_KEY in odict.keys():
        for o in files:
            rets += format_debug_line('format file [%s]'%(o),0,args.verbose)
            for f in odict[PATCH_FUNC_KEY][o].keys():
                rets += format_line('',0)
                rets += format_debug_line('format for function [%s]'%(f),0,args.verbose)
                rets += odict[PATCH_FUNC_KEY][o][f][FORMAT_FUNC_CODE_KEY]

    rets += output_patch_function(args,prefix,patchfuncname,odict,files)
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

def patch_objects(objparser,args,ofile,objs,odict,alldatas,force=False):
    if PATCH_FUNC_KEY in odict.keys():
        if ofile not in odict[PATCH_FUNC_KEY].keys():
            odict[PATCH_FUNC_KEY][ofile] = dict()
        for o in objs:
            if o not in odict[PATCH_FUNC_KEY].keys():
                #logging.error('[%s] not handled'%(o))
                continue
            if force or (o not in odict[PATCH_FUNC_KEY][ofile].keys() and o in odict[PATCH_FUNC_KEY].keys()):
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
                        if offsetk[k] <= 1 and offsetk[k] >= 0:
                            assert(k in xors.keys())
                            ki = int(k)
                            logging.info('[%s].[%s] [+0x%x:%d] [0x%02x] = [0x%02x] ^ [0x%02x]'%( o, f,ki,ki,\
                                alldatas[(reloff + ki)] ^ xors[k], alldatas[(reloff + ki)], \
                                xors[k]))
                            alldatas[(reloff + ki)] = alldatas[(reloff + ki)] ^ xors[k]
                            offsetk[k] = 2
                    odict[PATCH_FUNC_KEY][ofile][o][f][FORMAT_FUNC_OFFSET_KEY] = offsetk
                    odict[PATCH_FUNC_KEY][ofile][o][f][FUNC_DATA_KEY] = alldatas[reloff:(reloff + len(data))]
    return odict,alldatas

def _log_patch_function(args,odict,fname,funcname):
    rets = ''
    data = odict[FUNC_DATA_KEY]
    xors = odict[FORMAT_FUNC_XORS_KEY]
    i = 0
    lasti = 0
    xorlen = 0
    for k in xors.keys():
        xorlen += 1
    rets += 'format [%s].[%s] data[%d] xors[%d]'%(fname,funcname,len(data),xorlen)
    while i < len(data):
        if (i % 16) == 0:
            if i > 0:
                rets += ' ' * 4
                while lasti < i:
                    curval = data[lasti]
                    idx = '%d'%(lasti)
                    if idx in xors.keys():
                        curval = data[lasti] ^ xors[idx]
                    if curval >= ord(' ') and curval <= ord('~'):
                        rets += '%c'%(chr(curval))
                    else:
                        rets += '.'
                    lasti += 1
            rets += '\n0x%08x:'%(i)
        idx = '%d'%(i)
        if idx in xors.keys():
            rets += ' 0x%02x[0x%02x][0x%02x]'%(data[i] ^ xors[idx], data[i], xors[idx])
        else:
            rets += ' 0x%02x'%(data[i])
            rets += ' '* 12
        i += 1

    if i != lasti:
        while (i%16) != 0:
            rets += ' '* 17
            i += 1
        rets += '    '
        while lasti < len(data):
            curval = data[lasti]
            idx = '%d'%(lasti)
            if idx in xors.keys():
                curval = data[lasti] ^ xors[idx]
            if curval >= ord(' ') and curval <= ord('~'):
                rets += '%c'%(chr(curval))
            else:
                rets += '.'
            lasti += 1
        rets += '\n'
    return rets

def log_patch(args,odict,fname):
    rets = ''
    if PATCH_FUNC_KEY in odict.keys():
        if fname in odict[PATCH_FUNC_KEY].keys():
            for f in odict[PATCH_FUNC_KEY][fname].keys():
                for func in odict[PATCH_FUNC_KEY][fname][f].keys():
                    if len(rets) > 0:
                        rets += '\n'
                    rets += _log_patch_function(args,odict[PATCH_FUNC_KEY][fname][f][func],fname,func)
    return rets


def obunpatchelf_handler(args,parser):
    set_logging_level(args)
    if len(args.subnargs) < 1:
        raise Exception('obunpackelf objectfile functions')
    jdict , args = get_jdict(args)
    odict = get_odict(args,False)

    files = []
    for f in jdict.keys():
        logging.info('f [%s] funcs %s'%(f,jdict[f]))
        odict = object_one_file('ElfParser',odict,f,jdict[f],args.times,args.obunpatchelf_loglvl)
        files.append(f)
    rets = format_patch_funcions(args,odict,files,args.unpatchfunc)
    write_patch_output(args,rets,odict)
    sys.exit(0)
    return

def patch_objects_class(objclsname,args,ofile,objs,odict,force=False):
    objparser = call_object_parser(objclsname, ofile)
    alldatas = objparser.get_data()
    odict, alldatas =patch_objects(objparser,args,ofile,objs,odict,alldatas,force)
    objparser.close()
    write_file_ints(alldatas,ofile)
    return odict

def obpatchelf_handler(args,parser):
    set_logging_level(args)
    jdict, args = get_jdict(args)
    if args.dump is None:
        raise Exception('no dump file get')
    if args.output is None:
        raise Exception('must set output')
    with open(args.dump,'r') as fin:
        odict = json.load(fin)
        odict = Utf8Encode(odict).get_val()

    odict = patch_objects_class('ElfParser', args, args.output, args.subnargs, odict,False)
    with open(args.dump,'w+b') as fout:
        write_file_direct(json.dumps(odict,sort_keys=True,indent=4), fout)
    logging.info('log patch\n%s'%(log_patch(args,odict,args.output)))
    sys.exit(0)
    return


def obunpatchcoff_handler(args,parser):
    set_logging_level(args)
    if len(args.subnargs) < 1:
        raise Exception('obunpackelf objectfile functions')
    jdict ,args = get_jdict(args)
    odict = get_odict(args,False)

    files = []
    for f in jdict.keys():
        logging.info('f [%s] funcs %s'%(f,jdict[f]))
        odict = object_one_file('CoffParser',odict,f,jdict[f],args.times,args.obunpatchcoff_loglvl,args.win32)
        files.append(f)

    rets = format_patch_funcions(args,odict,files,args.unpatchfunc)
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

    odict = patch_objects_class('PEParser', args, args.output, args.subnargs, odict,False)
    with open(args.dump,'w+b') as fout:
        write_file_direct(json.dumps(odict,sort_keys=True,indent=4), fout)
    logging.info('log patch\n%s'%(log_patch(args,odict,args.output)))
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