#! /usr/bin/env python

import sys
import os
import extargsparse

##importdebugstart
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from strparser import *
from filehdl import *
from fmthdl import *
from obmaklib import *
##importdebugend

REPLACE_IMPORT_LIB=1

REPLACE_STR_PARSER=1
REPLACE_FILE_HDL=1
REPLACE_FMT_HDL=1
REPLACE_OBMAK_LIB=1


def main():
    commandline='''
    {
        "verbose|v" : "+",
        "version|V" : false,
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
    tofile= os.path.abspath(os.path.join(topdir,'obmak.py'))
    curdir = os.path.abspath(os.path.dirname(__file__))
    allincludes = []
    strparser = os.path.abspath(os.path.join(curdir,'strparser.py'))
    allincludes.append(strparser)
    fmthdl = os.path.abspath(os.path.join(curdir,'fmthdl.py'))
    allincludes.append(fmthdl)
    filehdl = os.path.abspath(os.path.join(curdir,'filehdl.py'))
    allincludes.append(filehdl)
    obmaklib = os.path.abspath(os.path.join(curdir,'obmaklib.py'))
    allincludes.append(obmaklib)
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
    obmaklib_c = get_import_file(obmaklib)
    fmthdl_c = get_import_file(fmthdl)
    #logging.info('str_c\n%s'%(strparser_c))
    sarr = re.split('\.',vernum)
    if len(sarr) != 3:
        raise Exception('version (%s) not format x.x.x'%(vernum))
    VERSIONNUMBER = vernum
    import_rets = fromat_ext_import_files(__file__,allincludes)
    logging.info('import_rets\n%s'%(import_rets))
    repls = dict()
    repls[r'VERSION_RELACE_STRING'] = VERSIONNUMBER
    repls[r'debug_main'] = 'main'
    repls[r'REPLACE_STR_PARSER=1'] = make_string_slash_ok(strparser_c)
    repls[r'REPLACE_IMPORT_LIB=1'] = make_string_slash_ok(import_rets)
    repls[r'REPLACE_FILE_HDL=1'] = make_string_slash_ok(filehdl_c)
    repls[r'REPLACE_OBMAK_LIB=1'] = make_string_slash_ok(obmaklib_c)
    repls[r'REPLACE_FMT_HDL=1'] = make_string_slash_ok(fmthdl_c)
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
