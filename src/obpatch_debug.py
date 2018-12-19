#! /usr/bin/env python

import logging
import sys
import os
import re
import extargsparse

##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from jsonhdl import *
from filehdl import *
from fmthdl import *
from extract_ob import *
from objparser import *
from elfparser import *
from coffparser import *
from peparser import *
from obpatchlib import *
##importdebugend


REPLACE_IMPORT_LIB=1

REPLACE_STR_PARSER=1
REPLACE_JSON_HDL=1
REPLACE_FILE_HDL=1
REPLACE_FMT_HDL=1
REPLACE_EXTRACT_OB=1
REPLACE_OBJ_PARSER=1
REPLACE_ELF_PARSER=1
REPLACE_COFF_PARSER=1
REPLACE_PE_PARSER=1
REPLACE_OB_PATCH_LIB=1


def main():
    commandline='''
    {
        "verbose|v" : "+",
        "version|V" : false,
        "objfile|O" : null,
        "output|o" : null,
        "input|i" : null,
        "times|T" : 0,
        "dump|D" : "obcode.json",
        "includes|I" : [],
        "includefiles" : [],
        "unpatchfunc|U" : "unpatch_handler",
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
        }
    }
    '''
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
    tofile= os.path.abspath(os.path.join(topdir,'obpatch.py'))
    curdir = os.path.abspath(os.path.dirname(__file__))
    rlfiles = ReleaseFiles(__file__)
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'strparser.py')),r'REPLACE_STR_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'filehdl.py')),r'REPLACE_FILE_HDL=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'fmthdl.py')),r'REPLACE_FMT_HDL=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'obpatchlib.py')),r'REPLACE_OB_PATCH_LIB=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'extract_ob.py')),r'REPLACE_EXTRACT_OB=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'objparser.py')),r'REPLACE_OBJ_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'elfparser.py')),r'REPLACE_ELF_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'coffparser.py')),r'REPLACE_COFF_PARSER=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'jsonhdl.py')),r'REPLACE_JSON_HDL=1')
    rlfiles.add_python_file(os.path.abspath(os.path.join(curdir,'peparser.py')),r'REPLACE_PE_PARSER=1')
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
