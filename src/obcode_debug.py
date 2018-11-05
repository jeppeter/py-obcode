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
from fmthdl import *
from cobattr import *
from cobfile import *
##importdebugend

REPLACE_IMPORT_LIB=1

REPLACE_STR_PARSER=1
REPLACE_FILE_HDL=1
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

def format_ob_patch_functions(objparser,jsondump,funcname,formatname,times,debuglevel=0):
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
            funcdata.append(1)
        else:
            funcdata.append(0)
            validbytes += 1
    if times == 0:
        # now to get the funcsize
        ftimes = int(validbytes / 2)
    if ftimes >= validbytes:
        ftimes = validbytes - 1

    rets += format_line('int %s()'%(formatname), 0)
    if funcname not in jsondump.keys():
        jsondump[funcname] = dict()
    if 'xors' not in jsondump[funcname].keys():
        jsondump[funcname]['xors'] = dict()
    jsondump[funcname]['formatfunc'] = formatfunc
    if ftimes > 0:
        i = 0
        rets += format_line('unsigned char* pbaseptr=(unsigned char*)&%s;'%(funcname),1)
        rets += format_line('unsigned char* pcurptr;',1)
        while i < ftimes:
            xornum = random.randint(0,255)
            xoroff = random.randint(0,funcsize - 1)
            if funcdata[xoroff] == 1:
                continue
            funcdata[xoroff] = 1
            rets += format_line('',1)
            rets += format_debug_line('%s[%d] = 0x%x ^ 0x%x = 0x%x'%(funcname, xoroff, data[funcoff + xoroff],xornum, (data[funcoff + xoroff]^xornum)), 1, debuglevel)
            rets += format_line('pcurptr = (pbaseptr + %d);'%(curoff),1)
            rets += format_line('*pcurptr ^= %d;'%(xornum),1)
            jsondump[funcname]['xors'][xoroff] = xornum
            i += 1
    rets += format_line('return 0;',1)
    rets += format_line('}',0)
    return rets

def obunpatchelf_handler(args,parser):
    set_logging_level(args)
    if len(args.subnargs) < 1:
        raise Exception('obunpackelf objectfile functions')
    ofile = args.subnargs[0]    
    elfparser = ElfParser(ofile)
    if args.dump is None:
        odict = dict()
    else:
        with open(args.dump) as fin:
            odict = json.load(fin)
    rets = ''
    for s in args.includes:
        rets += format_line('#include <%s>'%(s),0)

    for s in args.includefiles:
        rets += format_line('#include "%s"'%(s),0)


    for funcname in args.subnargs[1:]:
        nformatfunc = get_random_name(random.randint(5,20))
        rets += format_line('',0)
        rets += format_ob_patch_functions(elfparser,odict,funcname,nformatfunc,args.times,args.verbose)

    rets += format_line('',0)
    rets += format_line('int %s()'%(args.obunpatchelf_funcname),0)
    if len(args.subnargs) >= 2:
        rets += format_line('int ret;',1)
        for f in args.subnargs[1:]:
            rets += format_debug_line('format for %s'%(f),1,args.verbose)
            rets += format_line('ret = %s();'%(odict[f]['formatfunc']),1)
            rets += format_line('if (ret < 0) {', 1)
            rets += format_line('return ret;',2)
            rets += format_line('}',1)
    rets += format_line('return 0',1)
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
        "obunpatchelf<obunpatchelf_handler>##inputfile function... to format unpatch elf functions##" : {
            "$" : "+",
            "funcname" : "unpatch_handler"
        },
        "obpatchelf<obpatchelf_handler>##inputfile dumpfile to patch elf functions##" : {
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
        jdx = 0
        idx = 0
        while idx < len(ims) and not cont:
            while jdx < len(files) and not cont:
                if ims[idx].frommodule == files[jdx]:
                    cont = True
                    del ims[idx]
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
    allims = packed_import(allims)
    allims = make_filters_out(allims, files)
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
        logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    tofile= os.path.abspath(os.path.join(topdir,'obcode.py'))
    curdir = os.path.abspath(os.path.dirname(__file__))
    strparser = os.path.abspath(os.path.join(curdir,'strparser.py'))
    filehdl = os.path.abspath(os.path.join(curdir,'filehdl.py'))
    fmthdl =os.path.abspath(os.path.join(curdir,'fmthdl.py'))
    cobattr = os.path.abspath(os.path.join(curdir,'cobattr.py'))
    cobfile = os.path.abspath(os.path.join(curdir,'cobfile.py'))
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
