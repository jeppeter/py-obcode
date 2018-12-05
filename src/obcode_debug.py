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
from objparser import *
from elfparser import *
from coffparser import *
from peparser import *
from fmthdl import *
from cobattr import *
from cobfile import *
from obmaklib import *
from extract_ob import *
from obpatchlib import *
##importdebugend

REPLACE_IMPORT_LIB=1

REPLACE_STR_PARSER=1
REPLACE_FILE_HDL=1
REPLACE_OBJ_PARSER=1
REPLACE_ELF_PARSER=1
REPLACE_COFF_PARSER=1
REPLACE_PE_PARSER=1
REPLACE_FMT_HDL=1
REPLACE_COB_ATTR=1
REPLACE_COB_FILE=1
REPLACE_OBMAK_LIB=1
REPLACE_EXTRACT_OB=1
REPLACE_OB_PATCH_LIB=1


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

REUNPATCH_HANDLER_KEY='reunpatchhandle'

def obj_reunpatch_one_function(objparser, alldatas,args,odict,fname,funcname):
    relocs = odict[PATCH_FUNC_KEY][fname][funcname][FUNC_DATA_RELOC_KEY]
    win32mode = odict[PATCH_FUNC_KEY][fname]
    realf = funcname
    if win32mode:
        realf = '_%s'%(funcname)
    funcsize = objparser.func_size(realf)
    if funcsize != len(relocs):
        raise Exception('[%s].[%s] funcsize [%d] != relocs[%d]'%(fname, funcname,funcsize, len(relocs)))
    idx = 0
    funcaddr = objparser.func_addr(realf)
    while idx < len(relocs):
        getval = objparser.is_in_reloc(funcaddr + idx)
        if getval != relocs[idx]:
            raise Exception('[%s].[%s].[%d] reloc[%d] != stored relocs[%d]'%(fname,funcname, idx,getval, relocs[idx]))
        idx += 1
    funcoffs = odict[PATCH_FUNC_KEY][fname][funcname][FORMAT_FUNC_OFFSET_KEY]    
    xors = odict[PATCH_FUNC_KEY][fname][funcname][FORMAT_FUNC_XORS_KEY]
    funcoff = objparser.func_offset(realf)
    for offk in funcoffs.keys():
        off = int(offk)
        if funcoffs[offk] >= 2:
            # this is to change the value
            assert(offk in xors.keys())
            alldatas[(funcoff+off)] = alldatas[(funcoff + off)] ^ xors[offk]
    odict[PATCH_FUNC_KEY][fname][funcname][FUNC_DATA_KEY] = alldatas[(funcoff):(funcoff+funcsize)]
    return odict,alldatas


def obj_reunpatch_one_file(objparser,alldatas,args,odict,fname):
    if PATCH_FUNC_KEY not in odict.keys():
        raise Exception('no [%s] in PATCH_FUNC_KEY'%(PATCH_FUNC_KEY))
    if fname not in odict[PATCH_FUNC_KEY].keys():
        raise Exception('no [%s] in [%s]'%(fname,PATCH_FUNC_KEY))
    for f in odict[PATCH_FUNC_KEY][fname].keys():
        if REUNPATCH_HANDLER_KEY not in odict[PATCH_FUNC_KEY][fname][f].keys():
            odict, alldatas = obj_reunpatch_one_function(objparser,args,odict,fname,f)
            odict[PATCH_FUNC_KEY][fname][f][REUNPATCH_HANDLER_KEY] = True
    return odict,alldatas

def output_patch_formats(args, odict,fname):
    rets = ''
    for f in odict[PATCH_FUNC_KEY][fname].keys():
        if len(rets) > 0:
            rets += format_line('',0)
        rets += odict[PATCH_FUNC_KEY][fname][f][FORMAT_FUNC_CODE_KEY]
    return rets

def call_object_parser(clsname,f):
    m = __import__(__name__)
    cls_ = getattr(m,objclsname)
    if cls_ is None:
        raise Exception('cannot find [%s]'%(objclsname))
    return cls_(f)


def obj_reunpatch_files(objclsname,args,odict,fnames):
    for fname in fnames:
        objparser = call_object_parser(objclsname, fname)
        alldatas = objparser.get_data()
        odict, alldatas = obj_reunpatch_one_file(objparser, alldatas,args,odict,fname)
        objparser.close()
        write_file_ints(alldatas, fname)
    return odict

def obj_reunpatch(objclsname,patchfuncname,args,odict,files):
    rets = ''
    odict = obj_reunpatch_files(objclsname,args,odict,files)
    # now formats
    rets += format_includes(args)
    rets += ''

    if  PATCH_FUNC_KEY in odict.keys() and GET_FUNC_ADDR in odict[PATCH_FUNC_KEY].keys() \
        and FUNC_ADDR_CODE in odict[PATCH_FUNC_KEY][GET_FUNC_ADDR].keys():
        rets += odict[PATCH_FUNC_KEY][GET_FUNC_ADDR][FUNC_ADDR_CODE]

    # now to give the coding
    for f in files:
        rets += format_line('',0)
        rets += output_patch_formats(args,odict,f)

    rets += format_line('',0)
    rets += output_patch_function(args,patchfuncname,odict,files)
    return rets,odict


def obj_repatch_one_file(objparser,alldatas,args,odict,f):
    if PATCH_FUNC_KEY not in odict.keys():
        raise Exception('[%s] not in json'%(PATCH_FUNC_KEY))
    if f not in odict[PATCH_FUNC_KEY].keys():
        raise Exception('[%s] not in [%s]'%(f,PATCH_FUNC_KEY))
    

def obj_repatch(clsname,args,odict,fnames):
    for f in fnames:
        objparser = call_object_parser(clsname, f)
        alldatas = objparser.get_data()
        odict,alldatas = obj_repatch_one_file(objparser,alldatas,args,odict,f)
        objparser.close()
        write_file_ints(alldatas,f)
    return odict


def obreunpatchelf_handler(args,parser):
    set_logging_level(args)
    odict = get_odict(args,False)
    jdict, args= get_jdict(args)
    files = []
    for f in jdict.keys():
        files.append(f)
    rets , odict = obj_reunpatch('PEParser',args.unpatchfunc,args,odict,files)
    write_patch_output(args,rets,odict)
    sys.exit(0)
    return

def obrepatchelf_handler(args,parser):
    set_logging_level(args)
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
        "unpatchfunc|U" : "unpatch_handler",
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
            "loglvl" : 3
        },
        "obpatchelf<obpatchelf_handler>##inputfile to patch elf functions##" : {
            "$" : "+"
        },
        "obunpatchcoff<obunpatchcoff_handler>##objfile:func1,func2 ... to format unpatch coff file with func1 func2##" : {
            "$" : "+",
            "loglvl" : 3
        },
        "obpatchpe<obpatchpe_handler>##inputfile to patch pe functions##" : {
            "$" : "+"
        },
        "obunfunc<obunfunc_handler>##funcs... to set obfuncs##" : {
            "$" : "+"
        },
        "obunpatchelfforge<obunpatchelfforge_handler>##objfilename:func1,func2 ... to format unpatch elf file with func1 func2##" : {
            "$" : "+",
            "loglvl" : 3
        },
        "obpatchelfforge<obpatchelfforge_handler>##inputfile to no handle##" : {
            "$" : "+"
        },
        "obreunpatchelf<obreunpatchelf_handler>##objfiles ... to replay unpatchelf##" : {
            "$" : "+"
        },
        "obrepatchelf<obrepatchelf_handler>##objfiles ... to replay patchelf##" : {
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
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'objparser.py')),r'REPLACE_OBJ_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'obpatchlib.py')),r'REPLACE_OB_PATCH_LIB=1')

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
