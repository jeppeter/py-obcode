#! /usr/bin/env python

import logging
import sys
import os
import extargsparse
import re

##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from jsonhdl import *
from filehdl import *
from cobattr import *
from fmthdl import *
from cobfilebase import *
from elfparser import *
from coffparser import *
from peparser import *
from objparser import *
from obchkvallib import *
##importdebugend


REPLACE_IMPORT_LIB=1

REPLACE_STR_PARSER=1
REPLACE_JSON_HDL=1
REPLACE_FILE_HDL=1
REPLACE_COB_ATTR=1
REPLACE_FMT_HDL=1
REPLACE_COB_FILE_BASE=1
REPLACE_OBJ_PARSER=1
REPLACE_ELF_PARSER=1
REPLACE_COFF_PARSER=1
REPLACE_PE_PARSER=1
REPLACE_OB_CHKVAL_LIB=1


def main():
    commandline_fmt='''
    {
        "verbose|v" : "+",
        "version|V" : false,
        "win32|W" : false,
        "objfile|O" : null,
        "output|o" : null,
        "input|i" : null,
        "times|T" : 0,
        "chkval_times" : 5,
        "dump|D" : "obcode.json",
        "includes|I" : [],
        "includefiles" : [],
        "unpatchfunc|U" : "unpatch_handler",
        "failfunc" : "failfunc_handler",
        "fileprefix" : null,
        "appendpath" : "%s",
        "objsuffix" : "%s",
        "csuffix" : "%s",
        "objpattern" : null,
        "cpattern" : null,
        "obchkkey" : "obchkval",
        "with_quote" : false,
        "fmtchkval<fmtchkval_handler>##--obchkkey key objfile;func1,func2 ... to format chkval file##" : {
            "$" : "+"
        },
        "fmtchkvalforge<fmtchkvalforge_handler>##--obchkkey key objfile;func1,func2 ... to format chkval file forge##" : {
            "$" : "+"
        },
        "chkvalheader<chkvalheader_handler>##--obchkkey key to format chkval header file##" : {
            "$" : "*"
        },
        "chkvalheaderforge<chkvalheaderforge_handler>##--obchkkey key to format chkval header file forge##" : {
            "$" : "*"
        },
        "replchkval<replchkval_handler>##--obchkkey key  to replace chkval into new header##" : {
            "$" : "*"
        },
        "replchkvalforge<replchkvalforge_handler>##--obchkkey key  to replace chkval into new header forge##" : {
            "$" : "*"
        },
        "chkvaldumpfuncself<chkvaldumpfuncself_handler>##--obchkkey key to get the byte information for handler##" : {
            "$" : "*"
        },
        "chkvaldumpfuncsforge<chkvaldumpfuncsforge_handler>##--obchkkey key to get the byte information for handler forge##" : {
            "$" : "*"
        },
        "chkvalfillelf<chkvalfillelf_handler>##--obchkkey key  to filled real data into the structure##" : {
            "$" : "*"
        },
        "chkvalfillforge<chkvalfillforge_handler>##--obchkkey key  to filled real data into the structure forge##" : {
            "$" : "*"
        },
        "chkvalexitfmt<chkvalexitfmt_handler>##-i templatefile -o cfile --obchkkey key##" : {
            "$" : "*"
        },
        "chkvalexitfmtforge<chkvalexitfmtforge_handler>##-i templatefile -o cfile --obchkkey key##" : {
            "$" : "*"
        },
        "exitheaderfmt<exitheaderfmt_handler>##-o headerfile -D dumpjson --obchkkey key##" : {
            "$" : "*"
        },
        "exitheaderfmtforge<exitheaderfmtforge_handler>##-o headerfile -D dumpjson --obchkkey key forge##" : {
            "$" : "*"
        },
        "chkvalexitfiles<chkvalexitfiles_handler>##obchkkeys... to get the exit files list##" : {
            "$" : "+"
        },
        "chkvalexitobjs<chkvalexitobjs_handler>##obchkkey... to get  the exit objs list##" : {
            "$" : "+"
        },
        "chkvaldatafiles<chkvaldatafiles_handler>##obchkkey... to get the data files list##" : {
            "$" : "+"
        },
        "chkvaldataobjs<chkvaldataobjs_handler>##obchkkey... to get the data objs list##" : {
            "$" : "+"
        }
    }
    '''
    if sys.platform == 'win32':
        commandline=commandline_fmt%(os.getcwd(),'obj','cpp')
    else:
        commandline=commandline_fmt%(os.getcwd(),'o','c')
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
import re

def debug_release():
    if '-v' in sys.argv[1:]:
        #sys.stderr.write('will make verbose\n')
        loglvl =  logging.DEBUG
        if logging.root is not None and len(logging.root.handlers) > 0:
            logging.root.handlers = []
        logging.basicConfig(level=loglvl,format='%(asctime)s:%(filename)s:%(funcName)s:%(lineno)d\t%(message)s')
    topdir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    tofile= os.path.abspath(os.path.join(topdir,'obchkval.py'))
    curdir = os.path.abspath(os.path.dirname(__file__))
    rlfiles = ReleaseFiles(__file__)
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'strparser.py')),r'REPLACE_STR_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'jsonhdl.py')),r'REPLACE_JSON_HDL=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'obchkvallib.py')),r'REPLACE_OB_CHKVAL_LIB=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'cobfilebase.py')),r'REPLACE_COB_FILE_BASE=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'filehdl.py')),r'REPLACE_FILE_HDL=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'cobattr.py')),r'REPLACE_COB_ATTR=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'fmthdl.py')),r'REPLACE_FMT_HDL=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'elfparser.py')),r'REPLACE_ELF_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'coffparser.py')),r'REPLACE_COFF_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'peparser.py')),r'REPLACE_PE_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'objparser.py')),r'REPLACE_OBJ_PARSER=1')

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

def debug_main():
    if '--release' in sys.argv[1:]:
        debug_release()
        return
    main()
    return

##importdebugend

if __name__ == '__main__':
    debug_main()
